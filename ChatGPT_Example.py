import os
import requests

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.environ.get("OPENAI_API_KEY")

if API_KEY is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

def chat_gpt_session(messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
    }
    response = requests.post(API_ENDPOINT, json=data, headers=headers)
    if response.status_code != 200:
        print(f"API call failed with status code {response.status_code}. Response text: {response.text}")
        return "Sorry, there was an error processing your request."
    try:
        chat_gpt_response = response.json()['choices'][0]['message']['content']
        return chat_gpt_response
    except KeyError:
        print("Error extracting response from API's returned JSON. Here's the full response for debugging:")
        print(response.json())
        return "Sorry, there was an error processing your response."

def main():
    prompts = [
        "Write a Python program to print 'Hello, World!'",
        "Also print 'Hello, Mars'",
        "Also print 'Hello, Jupiter'",
    ]
    messages = [{"role": "system", "content": "You are ChatGPT, a helpful assistant."}]
    for prompt in prompts:
        messages.append({"role": "user", "content": prompt})
        response = chat_gpt_session(messages)
        print("ChatGPT: ", response)
        messages.append({"role": "assistant", "content": response})
        
if __name__ == "__main__":
    main()