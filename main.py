import os
import json
from dotenv import load_dotenv
from openai import OpenAI # OPEN AI library
import argparse  # Built in Python Module to hande user inputs

# VAR import
from prompts import system_prompt
# FUNCTION IMPORTING
from call_function import available_functions, call_function

# OpenRouter API Key Importing
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key == None:
    raise RuntimeError("No Openrouter API key environment found. Check intructions to make OpenRouter API key and add to environment file.")

# OpenAI client creation to point base_url to OpenRouter and send OpenRouter API key as API Key

client = OpenAI (
    base_url = "https://openrouter.ai/api/v1", 
    api_key = api_key,
)

# GETTING RESPONSE FROM MODEL
"""
Use the client.chat.completions.create() method to get a response from the model. You'll need two named parameters:

model: the model ID, openrouter/free
messages: a list of message objects. For now, just a single user message. Each message is a dictionary with a role and content. Hard-code the prompt exactly like this:
"""

# MODEL RESPONSE
"""
The method returns a chat completion object. The model's text answer lives at response.choices[0].message.content. Print it to see the model's answer.
"""

def generate_content(client: OpenAI, messages:list, verbose_flag:bool):
    response = client.chat.completions.create(
    model ="openrouter/free",
    messages = messages,
    tools = available_functions, 
)
    
    if response.usage == None:  # You should also verify that the response's usage property is not None before trying to access its own properties. If it is None, that would likely indicate a failed API request, and you could raise a RuntimeError with a helpful message.
        raise RuntimeError("API response appears to be malformed. Failed to access Usage Propert since it is `None`. Likely, a failed API request.")

    if verbose_flag == True:

    # MODEL USAGE, TOKEN METADATA
        Prompt_Tokens = response.usage.prompt_tokens

        Response_Tokens = response.usage.completion_tokens

        Total_Tokens = response.usage.total_tokens

        user_prompt = messages[1]["content"] # need to access dict from list index, then call that dict with key

    # MODEL USAGE TOKENS PRINTING
        print(f'User prompt: {user_prompt}')    
        print(f'Prompt tokens: {Prompt_Tokens}')
        print(f'Response tokens: {Response_Tokens}')
        print(f'Total tokens: {Total_Tokens}')

    # MODEL FUNCTION CALLs
    
    # CAPTURING MESSAGE
    message = response.choices[0].message # capturing message with message.tool_calls  property if the model made any function calls

    if message.tool_calls != None:  # calling function and returing a `tool` message that has function result, ALSO PRINTING THE RESULT # printing function name and args if any function calls were made

        for tool_call in message.tool_calls: # iterating over all the function calls made

                                    #function_args = json.loads(tool_call.function.arguments or "{}") # using python standard library json.laods() to turn JSON string into a dict

                                    #print(f"Calling function: {tool_call.function.name}({function_args})") # printing function name with its corresponding arguments
        # CATCHING tool_call message
            result_message = call_function(tool_call, verbose_flag)

            if result_message.get("content") == None:
                raise RuntimeError(f'Error: Empty function response for {tool_call.function.name}. In tool message dict return, "content" is empty')

            if verbose_flag == True:
                print(f"-> {result_message['content']}")

    else:
    # MODEL RESPONSE PRINTING
        print("Response:")
        print(message.content)
        

# Main Function

def main(): 
    # HANDLING USER INPUT Using Python Built in Module `argparse`
    """
    The way argparse works is that we create a parser object, define the arguments we want to accept, and then parse whatever arguments the user actually provided when they ran the script. See the example code below; you may want to customize the description, argument name, help message, etc. But the idea is that we're telling the argument parser to expect a single positional argument, i.e., the user-provided prompt.
    """
    parser = argparse.ArgumentParser(description="AIAgent User Input")

    # argparse User_Prompt
    parser.add_argument("user_prompt", type=str, help="User prompt to send to LLM")

    # argparse Verbose Output
    parser.add_argument("--verbose", action ="store_true", help="Enable verbose output")

    args = parser.parse_args() # Naming our parsed arguments `args`
                                # !!! Now we can access `args.user_prompt`

    
#Setting up Messages
    # getting response from model
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt}
    ]


# Setting up Verbose flags

    verbose_flag = args.verbose

# HELPER FUNCTION TO GENERATE AND PRINT RESPONSE
    generate_content(client, messages, verbose_flag)


if __name__ == "__main__":
    main()
