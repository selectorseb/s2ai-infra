import json
from openai import OpenAI
import pytest_check as check

model = "andy006/s2-oracle-trained"
openai_api_key = "EMPTY"
openai_api_base = "http://ml-infra.selector.ai:8000/v1/"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# Import tools (a list of function metadata) and dynamically import functions
with open('../tools.json', 'r') as file:
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

def is_present(test_arg, test_arg_value, result_args):
    return result_args.get(test_arg, '') == test_arg_value  

def execute_questions(questions):
    max_length = 2048
    top_p = 0.95
    temperature = 0.01
   
    for q in questions:
        history = []
        question = q['phrase']
        function = q['function']
        filters = q.get('filters', {})
        result = predict(question, max_length, top_p, temperature, history)
        print("-----------")
        print(f"\n\nQuestion: {question}")
        print(f"Answer: {result}")
        print("-----------")
        jresult = json.loads(result)
        result_function_name = jresult['name']
        function_impute_status = function in result_function_name

        filter_status = True
        for f in filters:
            if jresult['arguments'].get(f) != filters[f]:
                filter_status = False
        
        return function_impute_status, filter_status
        
