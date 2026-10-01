import os

"""
The key idea is that the directory parameter will be treated as a relative path within the working_directory. 
We'll allow the LLM agent to specify which directory it wants to scan, but the working_directory will be set by us. 
This means we can limit the scope of directories and files that the LLM is able to view.
"""

def get_files_info( working_directory: str, directory: str = ".") -> str:

    try:
        abs_working_directory: str = os.path.abspath(working_directory)

        joined_directory: str = os.path.join(abs_working_directory, directory) # remember `directory` is a relative path so we need to join to the absolute path from the given working directory

        norm_target_directory: str = os.path.normpath(joined_directory)  # need to normalize the dir path. is will handle things like ".."

        common_path: str = os.path.commonpath([abs_working_directory, norm_target_directory]) # need this to find the common path between working_directory and target_directory

        valid_target_dir: bool = common_path == abs_working_directory  # boolean to see if common_path matches the absoluter path of the working directory

        if valid_target_dir == False:     # Now our LLM agent has some guardrails: we never want it to be able to perform any work outside the working_directory that we give it. 
            
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        """
        Without this restriction, the LLM might run amok anywhere on the machine, reading sensitive files or overwriting important data. This is a very important step that we'll bake into every function the LLM can call.
        """
        
        is_directory = os.path.isdir(directory)  # seeing if directory is a directory

        if is_directory == False:  # If the directory argument is not a directory, again, return an error string:
            
            return f'Error: "{directory}" is not a directory' 

        if valid_target_dir == True and is_directory == True: # not necessary arguments to run them again but doing it for clarity purposes 
                                                                # but the success return string is required
            return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f'Error: {type(e).__name__} - {e}'
