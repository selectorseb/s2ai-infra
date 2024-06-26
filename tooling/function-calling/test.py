import json
from openai import OpenAI

model = "andy006/s2-oracle-trained"

questions = [
    "What is the s2ap infra health status?",
    "Who are you?",
    "packet loss seen by device d8 in arizone?"
]

openai_api_key = "EMPTY"
openai_api_base = "http://ml-infra.selector.ai:8000/v1/"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Import tools (a list of function metadata) and dynamically import functions
with open('./functions/tools.json', 'r') as file:
    tools = json.load(file)

def predict(user_input, max_length, top_p, temperature, history=[]):

    history.append({"role": "user", "content": user_input})

    conversation = [
        {
            "role": "function_metadata",
            "content": json.dumps(tools, indent=4)
        }
    ]
    conversation.extend(history)
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

    return completion_text

# main
def main():
    max_length = 2048
    top_p = 0.95
    temperature = 0.01
    history = []

    for question in questions:
        print(f"\n\nQuestion: {question}")
        result = predict(question, max_length, top_p, temperature, history)
        print(f"Answer: {result}")

if __name__=="__main__": 
    main()
