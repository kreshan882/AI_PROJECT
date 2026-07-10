from openai import OpenAI
from data import sample_data
from helper import get_top_k_similar

api_key = "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"
client = OpenAI(api_key=api_key)

messages= [
    {"role":"system", "content":"You are a helpful assistant."},
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
    context=get_top_k_similar(user_input, sample_data, 2)

    messages_with_context=messages+[{"role":"user", "content":
                                     "context:\n"+context+
                                     user_input}]
    
    # print("message with context :\n",context)
    
    reply=get_response(messages_with_context)

    messages.append({"role":"user", "content":user_input})

    messages.append({"role":"assistant", "content":reply})

    print(f"Assistant:{reply}\n")



