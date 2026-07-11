import requests
import ollama 

# Function 1: Use Ollama REST API (localhost)
def call_via_rest(prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen3.5:0.8b",
        "prompt": prompt,
        "stream": False,
        # "keep_alive": -1
    }

    response = requests.post(url, json=payload)
    data = response.json()
    return data.get("response", "No response received.")


# Function 2: Use Ollama Python Library
def call_via_lib(prompt: str) -> str:
    response = ollama.chat(
        model="qwen3.5:0.8b", #"qwen3:4b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


if __name__ == "__main__":
    prompt = "Explain in one line: What is AI?"

    print("Using REST API:")
    print(call_via_rest(prompt))
    print("\nUsing Ollama Python Library:")
    print(call_via_lib(prompt))
