from openai import OpenAI

api_key = "your-api-key"
client = OpenAI(api_key=api_key)

messages= [
    {"role":"system", "content":"You are a helpful assistant."},
]


def get_response(messages):
    stream=client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages,
        stream=True
    )
    reply=""
    print("Assistant:")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            content=chunk.choices[0].delta.content
            print(content,end="",flush=True)
            reply+=content
    print("\n")
    return reply



while True:
    user_input=input("You:")

    if user_input.lower()=="exit":
        print(messages)
        break
    
    messages.append({"role":"user", "content":user_input})
    
    reply=get_response(messages)

    messages.append({"role":"assistant", "content":reply})

    # print(f"Assistant:{reply}\n")