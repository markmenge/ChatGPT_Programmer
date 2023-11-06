import os
import requests
import keyboard
from python_patcher import python_patcher

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.environ.get("OPENAI_API_KEY")
code = None

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

def read_messages(filename):
    messages = []
    current_role = None
    current_content = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip()  # Remove trailing whitespace and newlines
            if line.lower().startswith('system:') or line.lower().startswith('user:'):
                if current_role and current_content:
                    # Join the content lines and strip leading/trailing whitespace
                    full_content = '\n'.join(current_content).strip()
                    messages.append({"role": current_role, "content": full_content})
                # Update the current role and reset content
                current_role = line.lower().replace(':', '').strip()
                current_content = []
            else:
                # Collect lines of content for the current role
                current_content.append(line)

        # Don't forget to add the last message if the file doesn't end with a new role
        if current_role and current_content:
            full_content = '\n'.join(current_content).strip()
            messages.append({"role": current_role, "content": full_content})

    return messages

def get_multi_line_input(prompt="Input (press shift to enter multi-line input)):\n"):
    print(prompt, end='')  # Print the prompt without moving to a new line
    lines = []
    while True:
        line = input()
        if not keyboard.is_pressed('shift'):
            break
        lines.append(line)

    return '\n'.join(lines)

def main():
    global help
    code = python_patcher("Test.py", "")
    messages = read_messages('messages.txt')
    
    while True:
        
        # Send ChatGPT the messages, get a response
        response = chat_gpt_session(messages)
        print("ChatGPT: ", response)

        # Append response to messages history
        messages.append({"role": "assistant", "content": response})

        # Process ChatGPT response, hoepfully it has some good python patcher (PP) commands
        code.process_chatgpt_response(response)

        # code.output contains the PP output. Append to messages the output from the PP commands.
        if (len(code.output) > 0):
            messages.append({"role": "user", "content": code.output})

        # Ask user for any input
        message_for_chatgpt = get_multi_line_input(prompt="User: ")
        if (len(message_for_chatgpt) > 0):
            if message_for_chatgpt == "quit":
                exit(0)
            messages.append({"role": "user", "content": message_for_chatgpt})

if __name__ == "__main__":
    main()