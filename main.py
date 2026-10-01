import os
from dotenv import load_dotenv

from openai import OpenAI # OPEN AI library

import argparse  # Built in Python Module to hande user inputs

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

# Main Function

def main(): 
    # HANDLING USER INPUT Using Python Built in Module `argparse`
    """
    The way argparse works is that we create a parser object, define the arguments we want to accept, and then parse whatever arguments the user actually provided when they ran the script. See the example code below; you may want to customize the description, argument name, help message, etc. But the idea is that we're telling the argument parser to expect a single positional argument, i.e., the user-provided prompt.
    """
    parser = argparse.ArgumentParser(description="AIAgent User Input")

    parser.add_argument("user_prompt", type=str, help="User prompt")

    args = parser.parse_args() # !!! Now we can access `args.user_prompt`

#Setting up Messages
    # getting response from model
    
    messages = [
        {"role": "user", "content": args.user_prompt}
    ]

# HELPER FUNCTION TO GENERATE AND PRINT RESPONSE
    generate_content(client, messages)









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

def generate_content(client: OpenAI, messages):
    response = client.chat.completions.create(
    model ="openrouter/free",
    messages = messages,
)
    
    if not response.usage:  # You should also verify that the response's usage property is not None before trying to access its own properties. If it is None, that would likely indicate a failed API request, and you could raise a RuntimeError with a helpful message.
        raise RuntimeError("API response appears to be malformed. Failed to access Usage Propert since it is `None`. Likely, a failed API request.")

# MODEL USAGE, TOKEN METADATA
    Prompt_Tokens = response.usage.prompt_tokens

    Response_Tokens = response.usage.completion_tokens

    Total_Tokens = response.usage.total_tokens

# MODEL USAGE TOKENS PRINTING    
    print(f'Prompt tokens: {Prompt_Tokens}')
    print(f'Response tokens: {Response_Tokens}')
    print(f'Total tokens: {Total_Tokens}')

# MODEL RESPONSE PRINTING
    print(response.choices[0].message.content)





if __name__ == "__main__":
    main()
