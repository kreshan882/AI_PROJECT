import requests
import json
# Conversation memory
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
]

def get_chat_response(messages):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "qwen3:4b",
        "messages": messages, # Pass the whole message history
        "stream": True
    }

    print("Assistant:", end=" ", flush=True)
    reply = ""

    with requests.post(url, json=payload, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    event = json.loads(line)
                    delta = event.get("message", {}).get("content", "")
                    print(delta, end="", flush=True)
                    reply += delta
                    if event.get("done"):
                        break
                except json.JSONDecodeError:
                    continue
    print("\n")
    return reply

# Chat loop
while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print(messages)
        break

    messages.append({"role": "user", "content": user_input})

    reply = get_chat_response(messages)

    messages.append({"role": "assistant", "content": reply})
