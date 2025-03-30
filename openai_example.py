from openai import OpenAI
import os
from dotenv import load_dotenv
from extract_info import query_database
import json
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tool = {
    "type": "function",
    "function": {
        "name": "query_database",
        "description": "Query the database for information, accepts only sqlite queries",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute"
                }
            },
            "required": ["query"]
        }
    }
}

# messages = [{
#                 "role": "system",
#                 "content": "You are a helpful assistant that ONLY answers questions regarding sqlite database. The databse in use is personal_info.db and the table is personal_info. It contains the following columns: name, surname, email. Convert the user input to sqlite query before passing it to the tool."
#             },
#     {"role": "user", "content": "What is the name of the person with the email 'john.doe@example.com'?"}]

# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=messages,
#     tools=[tool],
# )

# print(completion.choices[0].message.tool_calls)
# tool_call = completion.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)
# print(tool_call, args)
# result = query_database(args["query"])
# print(result)


context = ""
while True:
    user_input = input("You: ")
    #context += user_input + "\n"
    messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that ONLY answers questions regarding sqlite database. The databse in use is personal_info.db and the table is personal_info. It contains the following columns: name, surname, email. Convert the user input to sqlite query before passing it to the tool."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=[tool]
    )
    tool_call = completion.choices[0].message.tool_calls[0]
    print("Tool call: ", tool_call)
    args = json.loads(tool_call.function.arguments)
    result = query_database(args["query"])

    # append the results
    messages.append(completion.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    })
    completion_2 = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=[tool]
    )
    print("Completion 2: ", completion_2.choices[0].message.content)
    # context += str(completion.choices[0].message.content) + "\n"
    # print("AI: ", completion.choices[0].message.content)
    # print("Context: ", context)
    # print("--------------------------------\n\n")
    # print("Result: ", result)

# print(completion)
# print("--------------------------------\n\n")
# print(completion.choices[0].message.content)