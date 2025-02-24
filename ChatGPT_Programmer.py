import os
import requests
import keyboard
from python_patcher import python_patcher

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
    try:
        response = requests.post(API_ENDPOINT, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get('choices', [{}])[0].get('message', {}).get('content', "No response received.")
    except requests.RequestException as e:
        print(f"API call error: {e}")
        return "Sorry, there was an error processing your request."

def read_messages(filename):
    messages = []
    try:
        with open(filename, 'r') as file:
            current_role, current_content = None, []
            for line in file:
                line = line.strip()
                if line.lower().startswith(('system:', 'user:')):
                    if current_role and current_content:
                        messages.append({"role": current_role, "content": '\n'.join(current_content).strip()})
                    current_role = line.lower().replace(':', '').strip()
                    current_content = []
                else:
                    current_content.append(line)
            if current_role and current_content:
                messages.append({"role": current_role, "content": '\n'.join(current_content).strip()})
    except FileNotFoundError:
        print("Warning: messages.txt not found. Starting with an empty conversation.")
    return messages

def get_multi_line_input(prompt="User (type 'END' to finish input):\n"):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return '\n'.join(lines)

def main():
    code = python_patcher("Test.py", "")
    messages = read_messages('messages.txt')
    
    while True:
        response = chat_gpt_session(messages)
        print("ChatGPT: ", response)
        messages.append({"role": "assistant", "content": response})
        
        code.process_chatgpt_response(response)
        
        if code.output:
            messages.append({"role": "user", "content": code.output})
        
        user_input = get_multi_line_input()
        if user_input:
            if user_input.lower() == "quit":
                exit(0)
            messages.append({"role": "user", "content": user_input})

if __name__ == "__main__":
    main()
