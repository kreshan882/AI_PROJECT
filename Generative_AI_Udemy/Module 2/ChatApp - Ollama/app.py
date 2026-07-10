import ollama

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Context: Salman is from Karur."}
]

def get_response(messages):
    response = ollama.chat(
        model="qwen3.5:0.8b",
        messages=messages,
    )
    return response["message"]["content"]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print(messages)
        break

    messages.append({"role": "user", "content": user_input})

    reply = get_response(messages)

    messages.append({"role": "assistant", "content": reply})

    print(f"Assistant: {reply}\n")



# [{'role': 'system', 'content': 'You are a helpful assistant. tell me answer always using less than 5 words'}, 
#  {'role': 'user', 'content': 'hello'},
#    {'role': 'assistant', 'content': 'Hello!'}, 
#  {'role': 'user', 'content': 'how are you'}, 
#  {'role': 'assistant', 'content': "I'm doing well."},
# {'role': 'user', 'content': 'what is data'},
# {'role': 'assistant', 'content': 'Facts, figures, or information.'}, 
# {'role': 'user', 'content': 'okay'}, 
# {'role': 'assistant', 'content': 'Glad to help.'}]