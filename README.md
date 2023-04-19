# GPT-3.5-turbo Chatbot with Code Execution
This Python program demonstrates how to interact with OpenAI's GPT-3.5-turbo model using the Chat API and execute the generated Python code on your local machine. The program can generate Python code based on user inputs and execute it, potentially improving the chatbot's functionality.
However, executing unverified code can be dangerous, so use this program with caution.

Tested in:

Python 3.10.10+
Requirements:

OpenAI Python Library: Install it with `pip install openai`


How the program works:

The program simulates a conversation between the user and the chatbot.
The user inputs a message, and the chatbot processes it and generates a response
If the response contains Python code, the program can execute that code and incorporate the output into the conversation, allowing the chatbot to run code and correct its own errors.


How to Use the Program:

Clone the repository and navigate to the project folder.

Ensure that the required packages are installed by running `pip install openai`.

Open the main Python file (`dangerous-ai.py`) in a text editor and set the api_key variable at the top to your OpenAI API key in string format.
Run the program with `python dangerous-ai.py`.




Key components of the program:

`Chatbot`: A class that represents a chatbot, with methods for interacting with the OpenAI API and handling the conversation.

`Conversation`: A class that manages the conversation, keeping track of messages and their roles (user, assistant, or system).

`execute_code_and_get_output`: A function that takes Python code as input, executes it, and returns the output.

`autoprompt_v2`: A function that handles code execution and incorporates the output into the conversation.



`User Inputs`:

The program will prompt users for various inputs to customize their interaction with the chatbot:

`Conversation name`: Provide a name for the conversation. The program will save the conversation history to a JSON file with this name.
New or existing conversation: Choose whether to create a new conversation or load an existing one from a JSON file.

`System message`: Enter a system message, which is a prompt that helps set the context for the conversation with the chatbot. Leave empty for default (Default is You are a python programmer bot, you strive to give complete, coherent, printful verbose and bug free code. Always provide the complete code, not in parts, the entire thing, Make the code a single block)

`Risk your computer`: Choose whether to enable code execution feature by responding with "y" or "n".
To stop the program, press `CTRL + C` in the terminal.

`Example inputs`
Inputs like these produce good results because it allows the AI to have feedback on the code's success.
        "make a simple calculator and a test function that will test it and print the results"

Also, `input()` causes problems

Note:

WARNING: This program can potentially execute harmful code. Please use it with caution and review the generated code before execution.
When the token count reaches 4k, the program will halt. A feature to forget past messages will be implemented at some point.

Enjoy interacting with the chatbot and exploring the power of code execution!
