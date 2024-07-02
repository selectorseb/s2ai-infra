import os
import importlib
import json
from termcolor import colored
from openai import OpenAI
import gradio as gr

from function_utils import prepare_function_tools
prepare_function_tools()

demo_mode = False
model = "andy006/s2-oracle-trained"

openai_api_key = "EMPTY"
openai_api_base = "http://ml-infra.selector.ai:8000/v1/"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Import tools (a list of function metadata) and dynamically import functions
with open('./functions/tools.json', 'r') as file:
    tools = json.load(file)

functions = {
    tool["function"]["name"]: importlib.import_module(f"functions.{tool['function']['name']}").__dict__[tool["function"]["name"]]
    for tool in tools if tool["type"] == "function"
}

def execute_function_call(func_json, functions_dict):
    func_name = func_json.get("name")
    func_arguments = func_json.get("arguments", {})

    if func_name in functions_dict:
        if isinstance(func_arguments, dict):
            results = functions_dict[func_name](**func_arguments)
        else:
            results = "Error: Invalid arguments format"
    else:
        results = f"Error: function {func_name} does not exist"

    return results


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "cyan",
        "function_call": "magenta",
        "function_response": "yellow",
    }

    print(colored("-----------------------------------------", "blue"))
    for message in messages:
        if message["role"] in role_to_color:
            print(colored(f"{message['role']}: {message['content']}\n", role_to_color[message["role"]]))

def predict(user_input, max_length, top_p, temperature, history=[]):

    if demo_mode:
        history = []

    history.append({"role": "user", "content": user_input})

    conversation = [
        {
            "role": "function_metadata",
            "content": json.dumps(tools, indent=4)
        }
    ]
    conversation.extend(history)
    try:
        chat_response = client.chat.completions.create(
            model=model,
            messages=conversation,
            temperature=temperature,
            max_tokens=max_length,
            stream=False,
        )
        if chat_response.choices:
            completion_text = chat_response.choices[0].message.content
        else:
            completion_text = None

        function_call_json = None
        try:
            function_call_json = json.loads(completion_text)
        except json.JSONDecodeError as e:
            if not isinstance(completion_text, str):
                completion_text = json.dumps(completion_text, indent=4)

        if isinstance(function_call_json, dict) and function_call_json.get("name") is not None:
            history.append({"role": "function_call", "content": json.dumps(function_call_json, indent=4)})
            if demo_mode:
                completion_text = json.dumps(function_call_json, indent=4)
            else:
                results = execute_function_call(function_call_json, functions)
                if not isinstance(results, str):
                    results = json.dumps(results, indent=4)
                history.append({"role": "function_response", "content": results})
                #history.append({"role": "user", "content": "Summarize the following output in 100 words: \n" + results})
                response = client.chat.completions.create(
                    model=model,
                    messages=history,
                    temperature=temperature,
                    max_tokens=max_length,
                    stream=False,
                )
                completion_text = response.choices[0].message.content
    except Exception as e:
        completion_text = f"Error in generating response from the server: {e}"

    history.append({"role": "assistant", "content": completion_text})
    filer_messages = []
    i = 0
    while i < len(history):
        if history[i]["role"] == "user" or history[i]["role"] == "assistant":
            filer_messages.append(history[i]["content"])
            i = i + 1
        # elif history[i]["role"] == "function_call":
        #     i = i + 2
        else:
            i = i + 1
    messages = [(filer_messages[i], filer_messages[i+1]) for i in range(0, len(filer_messages)-1, 2)]
    pretty_print_conversation(history)


    return messages, history

# Clear chat history function
def clear_chat():
    return [], []


# Create the Gradio interface
with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">Selector LLM ChatBot</h1>""")
    chatbot_history = gr.State([])
    chatbox = gr.Chatbot(height=700)
    with gr.Row():
        with gr.Column(scale=4):
            user_input = gr.Textbox(show_label=False, placeholder="Ask me a question", scale=10, lines=10,container=False)
            send_button = gr.Button("Send")
        with gr.Column(scale=1):
            clear_button = gr.Button("Clear")
            max_length = gr.Slider(0, 8192, value=2048, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.8, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0.01, 1, value=0.01, step=0.01, label="Temperature", interactive=True)

    # Define the interaction logic
    send_button.click(predict, inputs=[user_input, max_length, top_p, temperature, chatbot_history], outputs=[chatbox, chatbot_history])
    user_input.submit(predict, inputs=[user_input, max_length, top_p, temperature, chatbot_history], outputs=[chatbox, chatbot_history])
    send_button.click(lambda x: gr.update(value=''), [],[user_input])
    user_input.submit(lambda x: gr.update(value=''), [],[user_input])
    clear_button.click(clear_chat, inputs=[], outputs=[chatbox, chatbot_history])
# Launch the app
demo.queue().launch(
    debug=True,
    server_name="0.0.0.0",
    server_port=3000,
)
