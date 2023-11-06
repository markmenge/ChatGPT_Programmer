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

helpstr = """
Description
This is ChatGPT Automated Programming

ChatGPT Programmer: The main interface for the user to interact with the system. It uses the OpenAI API to generate code and test cases based on user input and project requirements.
Python Patcher (PP): A tool for modifying and patching existing Python code based on AI-generated instructions. It adds more functionality to handle complex code transformations.
Project Files: The generated code is stored in separate project files, which are then used by the test runner to verify the correctness of the code.
Test Runner: A tool that runs the test cases against the project files to verify the correctness of the code.

Python Patcher (PP) commands:
addfunc <function definition> - add function (multi-line, finish with ###)
delfunc <function name> - delete a function
addimport <import statement> - add a line in the imports
delimport <import statement> - delete import
setmain <function definition> - set main body of code (multi-line, finish with ###). Must be code for the main body, do not define functions in setmain code!
printcode - print all current code 
run - run the python program to get the output.


Examples:
setmain
if __name__ == "__main__":
    print(10)
###
addfunc
def sum(a, b):
    return a + b
###
delfunc foo
addimport import numpy
delimport import numpy
printcode
run

Here's how ChatGPT Programmer works. The python main body always starts with # MAIN. In a loop:
Step    Description
1.  I enter a request for a change.
2.  An array of request and responses are sent to ChatGPT via the API, with the new request.
3.  ChatGPT responds with PP commands to change the python program. For example, you respond with:
    setmain
    if __name__ == "__main__":
        print(10)
    ###
4.  I run the program.
5.  Goto step 1.

"""

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
    messages = [{"role": "system", "content": "You are a Automated Programmer using Python You write and run python code with PP (python programmer) commands."}]
    messages.append({"role": "user", "content": helpstr})
    messages.append({"role": "system", "content": "Got it! Awaiting your instructions."})
    messages.append({"role": "user", "content": """
Using PP commands, write python code that calls function guess_number(number) in guess_number.py to guess a number between 1 and 50.
So you might write your code with:
addimport import guess_number
setmain
guess_number.guess_number(10)
###
Then run it:
run
You guessed 25 which is too low!
Then ChatGPT, use setmain PP comand to guess higher:
setmain
guess_number.guess_number(20)
###
So on and so on, until you guess correctly, at which time the guess_number function will print:
You guessed it! The number was 32!
and the program will exit.
                     
Remember ChatGPT you are guessing the number. Use PP commands to modify the python code and use run to run it!
No explanations please. If I need to talk to you, {I will talk in curly braces like this}"""})
    
    while True:
        
        # Ask ChatGPT for a response
        response = chat_gpt_session(messages)
        print("ChatGPT: ", response)

        # Append response to messages history
        messages.append({"role": "assistant", "content": response})

        # Using PP, process the response
        code.process_chatgpt_response(response)

        # code.output contains the PP output. Append to messages the output from the PP commands.
        if (len(code.output) > 0):
            messages.append({"role": "user", "content": code.output})

        # Ask user for any input to add
        message_for_chatgpt = get_multi_line_input(prompt="User: ")
        if (len(message_for_chatgpt) > 0):
            messages.append({"role": "user", "content": message_for_chatgpt})

if __name__ == "__main__":
    main()