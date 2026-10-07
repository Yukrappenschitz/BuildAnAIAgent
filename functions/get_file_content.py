import os

from config import LLM_Read_Characater_Limit  # 10,000 character Limit

# SCHEMA FOR get_file_content

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Prints the contents of a specified file upto a configureable MAX_CHARACTER limit into a string, truncates file if over MAX_CHARS limit and adds to end of the string that file is truncated at that limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get file contents from, relative to the working directory",
                }
            },
            "required": ["file_path"], 
        }
    }

}



def get_file_content(working_directory: str, file_path: str) -> str:

    try:

        abs_working_directory:str = os.path.abspath(working_directory)  # getting absolute path of working_directory to create abs path for file_path later

        abs_file_path: str = os.path.join(abs_working_directory, file_path)

        norm_abs_file_path: str = os.path.normpath(abs_file_path)   # NORMALIZED ABSOLUTE file path for given file path

        common_file_path: str = os.path.commonpath([abs_working_directory, norm_abs_file_path])   # getting common path between abs working directory and abs file path to check if its under working_directory

        valid_file_path: bool = abs_working_directory == common_file_path   # BOOLEAN To store whether given file_path is under given working_directory # !!!! IMPORTANT TO LIMIT LLM ACCESSS

        if valid_file_path == False:         # ERROR: to return when file path is not valid and not under working directory
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        is_file = os.path.isfile(norm_abs_file_path)

        if is_file == False:         # ERROR: TO return when given file_path is not a directory
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # READING FILE if file_path is valid

        if valid_file_path == True and is_file == True: 
            MAX_CHARS = LLM_Read_Characater_Limit   # settomg local MAX_CHARS to imported LLM_Read_Character_Limit
                                                    # We don't want to accidentally read a gigantic file and send all that data to the LLM... that's a good way to burn through our token limits.
            with open(norm_abs_file_path, "r") as f:  # with statement automatically closes the file for us when the block finishes.
                                                     # !!!!! IMPORTANT TO USE ABSOLUTE FILE PATH OF GIVEN file path 
                
                file_content:str = f.read(MAX_CHARS)  # using built in read() function to read given file upto MAX_CHARS characters

                if f.read(1) != "":   # Check if the file was larger than the limit. A simple way of doing this is to try to read one more character after reading the initial chunk. 
                                      # If you get an empty string, you know that you already reached the end of the file. If you get a character back, then the file still had more data. In that case, add a message to the contents string to indicate that it was truncated
                    file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content 
             
    except Exception as e:
        return f'Error: {type(e).__name__} - {e}'

