import os
import openai
import json
import subprocess
import tempfile
import time

api_key = "sk-"

code_file_counter = 0


class Chatbot:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def chat_completion_api(self, conversation):
        openai.api_key = self.api_key

        messages = [{"role": message["role"], "content": message["content"]} for message in conversation.messages]

        while True:
            try:
                response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=messages
                                ##rest of model arguments
                )
                content = response['choices'][0]['message']['content']

                conversation.add_message("assistant", content)
                return {"response": content}
            except openai.error.RateLimitError:
                print("Rate limit error encountered. Waiting for 30 seconds before retrying...")
                time.sleep(30)



class Conversation:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def read_from_json(self, filename):
        try:
            with open(filename, "r") as f:
                conversation_json = json.load(f)
            self.messages = conversation_json["messages"]
        except:
            pass
       # print(self.messages)

    def write_to_json(self, filename):
        conversation_json = {"messages": self.messages}
        with open(filename, "w") as f:
            json.dump(conversation_json, f, indent=2)

    def get_conversation_format(self):
        return [{"role": message["role"], "content": message["content"]} for message in self.messages]




def get_multiline_input(prompt, end_word):
    lines = []
    print(prompt)
    while True:
        line = input()
        if line.strip() == end_word:
            break
        lines.append(line)
    print("Sent message to API...")
    return '\n'.join(lines)




def execute_code_and_get_output(code, file_counter):
    global code_file_counter
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py") as temp:
        temp.write(code)
        temp.flush()

        # Save the code to a file with a counter in the file name
        file_name = f"generated_code_{file_counter}.py"
        with open(file_name, "w") as f:
            f.write(code)

        try:
            output = subprocess.check_output(["python", temp.name], stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            output = e.output

    code_file_counter += 1
    return output


def autoprompt_v2(conversation, chatbot, filename, file_counter):
    last_message = conversation.messages[-1]["content"]
    print(last_message)

    # Extract Python code from the message
    code_start = last_message.find("```python")
    if code_start == -1:
        code_start = last_message.find("```")
        code_end = last_message.find("```", code_start + len("```"))
    else:
        code_end = last_message.find("```", code_start + len("```python"))

    if code_start != -1 and code_end != -1:
        python_code = last_message[code_start + (len("```python") if "```python" in last_message else len("```")):code_end].strip()
        print("---")
        print("Python code to execute:")
        print(python_code)

        # Execute the code and get the output
        code_output = execute_code_and_get_output(python_code, file_counter)
        print("---")
        print("Code output:")
        print(code_output)

        # Add the executed code to the message before the output
        code_output = f"Executed code:\n```\n{python_code}\n```\nOutput:\n{code_output}"

        # Add the code output to the conversation as a user message
        conversation.add_message("user", code_output)
        num_tokens = sum(len(msg["content"]) for msg in conversation.messages) // 4
        print(f"Number of tokens after response: {num_tokens}")
        
        # Get the response from the chatbot based on the code output
        response = chatbot.chat_completion_api(conversation)
        content = response["response"]

        # Save the conversation
        conversation.write_to_json(filename)

        return content
    else:
        print("---")
        print("No Python code found in the last message.")
        return None




def interact_chat(conversation, chatbot, filename, sys_message=None, auto_prompt=False, feedback_chatbot=None):
    try:
        if sys_message == '':
            sys_message = "You are a python programmer bot, you strive to give complete, coherent, printful verbose and bug free code. Always provide the complete code, not in parts, the entire thing, Make the code a single block"

        conversation.add_message("system", sys_message)
        while True:
            print("---")

            conversation.read_from_json(filename)

            user_input = get_multiline_input("Enter your message: ", "|")
            conversation.add_message("user", user_input)

            num_tokens = sum(len(msg["content"]) for msg in conversation.messages) // 4
            print(f"Number of tokens before response: {num_tokens}")

            response = chatbot.chat_completion_api(conversation)
            content = response["response"]

            if auto_prompt:
                while content:
                    content = autoprompt_v2(conversation, chatbot, filename, code_file_counter)
                    print(f"Bot: {content}")
                    print("---")
            else:
                print(f"Bot: {content}")
                print("---")

            num_tokens = sum(len(msg["content"]) for msg in conversation.messages) // 4
            print(f"Number of tokens after response: {num_tokens}")
            conversation.write_to_json(filename)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")




def main(api_key, code_file_counter):

    conversation_name = input("Enter conversation name: ")
    conversation_filename = f"{conversation_name}.json"

    if input("Do you want to create a new conversation or load an existing one? (c/l): ") == "c":
        conversation = Conversation()
    else:
        conversation = Conversation()
        conversation.read_from_json(conversation_filename)

   
    model = "gpt-3.5-turbo"

    chatbot = Chatbot(api_key, model)
    feedback_chatbot = Chatbot(api_key, model)
    sys_message = None
    sys_message = input("What is the system message? : ")

    auto_prompt = input("Would you like to risk your computer? (y/n): ").lower() == "y"
    auto_prompt_sys_message = None
    
        


            

    interact_chat(conversation, chatbot, conversation_filename, sys_message, auto_prompt, feedback_chatbot)

   

    conversation.write_to_json(conversation_filename)



if __name__ == "__main__":
    main(api_key, code_file_counter)