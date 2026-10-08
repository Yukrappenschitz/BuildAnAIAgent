import json
from collections.abc import Callable

#CONSTANT CONFIG IMPORT
from config import WORKING_DIR

# SCHEMA IMPORT
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

# Will be passed as `tools` to LLM Model during response creation of client.chat.completions.create() object
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

# 4. We'll need to determine which of the four functions to call (if any). To make this ergonomic, define a mapping of function names to actual functions
function_map: dict[str, Callable[...,str] ] = {    
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file" : write_file,
    }

def call_function(tool_call, verbose: bool = False) -> dict:
     #  parse the arguments from their JSON-string form into a real dictionary (import json):
    
    function_name = tool_call.function.name   # tool_call.function.name: the name of the function (a string)

    function_args = json.loads(tool_call.function.arguments or "{}") # tool_call.function.arguments: the arguments, as a JSON string, parse the arguments from their JSON-string form into a real dictionary 

    tool_call_id = tool_call.id                  # tool_call.id: a unique ID for this call (we'll need it when we send the result back)

    if verbose == True:                    # 3. If verbose is specified, print the function name and args:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # HANDINLING UNKNOWN FUNCTION NAME
    if function_name not in function_map:       # 5. If the provided function name is not found in your mapping, return a tool message describing the error:
        err_tool_message = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": f"Error: Unknown function: {function_name}",
        }
        return err_tool_message
    
    else:
    # PASSING working_directory to LLM MODEL (the LLM doesn't know about it)
        function_args["working_directory"] = WORKING_DIR  # hardcored for now      # 6. Assuming the function name is valid, we need to inject the working_directory argument (the LLM doesn't know about it). Set "working_directory" to "./calculator" in the function_args dictionary.

    # ACTUALLY CALLING FUNCTIONS
                        # RESULT OF CALLING FUNCTIONS (all the functions return strings)                                            
        result = function_map[function_name](**function_args) # 7. calling function_name function from function_map dict with given function_args (**function_args)

        tool_message = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result,
        }

        return tool_message             # 8. Return a tool message containing the result:
    


#### EXAMPLE SCHEMA FOR OPEN AI SDK LLM MODEL FUNCTION CALL
"""
schema_example_function = {
    "type": "function",              # specifying type to LLM model
    "function": {                       # specifying properties of type
        "name": "",              # name of function
        "description": "",            # description of what func does
        "parameters": {              # parameters to allow model to understand the args of the functions
            "type": "object",
            "properties": {                 # dictionary of desciptions of arguments, their name + type + description of args
                "args_name_1": {           # name of each args
                    "type": "",              # type of specified args
                    "description": "",        # description of specified args
                },
                "arg_name_2": {
                    "type": "",
                    "description": "",
                },
            },
        "required" : [""],               # if function has required arguments, add them as a parameter with key "required" = ["list of required args"]
        }
    }

}

"""
