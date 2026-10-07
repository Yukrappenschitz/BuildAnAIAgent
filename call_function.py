from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]


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
