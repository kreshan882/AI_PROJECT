from openai import OpenAI
# https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/tree/main
# https://platform.openai.com/api-keys
# settings->org Settings-> billing
# api_keykk = ""
api_key = "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"

client = OpenAI(api_key=api_key)

messages= [
    {"role":"system", "content":"You are a helpful assistant."},
    {"role":"user", "content":"Context : salman is from karur"}
]


def get_response(messages):
    response=client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages
    )
    return response.choices[0].message.content

while True:
    user_input=input("You:")

    if user_input.lower()=="exit":
        print(messages)
        break
    
    messages.append({"role":"user", "content":user_input})
    
    reply=get_response(messages)

    messages.append({"role":"assistant", "content":reply})

    print(f"Assistant:{reply}\n")



# [{'role': 'system', 'content': 'You are a helpful assistant. tell me answer always using less than 5 words'}, 
#  {'role': 'user', 'content': 'hello'},
#    {'role': 'assistant', 'content': 'Hello!'}, 
#  {'role': 'user', 'content': 'how are you'}, 
#  {'role': 'assistant', 'content': "I'm doing well."},
# {'role': 'user', 'content': 'what is data'},
# {'role': 'assistant', 'content': 'Facts, figures, or information.'}, 
# {'role': 'user', 'content': 'okay'}, 
# {'role': 'assistant', 'content': 'Glad to help.'}]