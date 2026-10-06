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
            
            return f'Result for "{directory}" directory:\nCannot list "{directory}" as it is outside the permitted working directory'

        """
        Without this restriction, the LLM might run amok anywhere on the machine, reading sensitive files or overwriting important data. This is a very important step that we'll bake into every function the LLM can call.
        """
        
        is_directory = os.path.isdir(norm_target_directory)  # seeing if directory is a directory ### !!! IMPORTANT TO PASS ABSOLUTE PATH OF TARGET DIR

        if is_directory == False:  # If the directory argument is not a directory, again, return an error string:
            
            return f'Result for "{directory}" directory:\nError: "{directory}" is not a directory' 

        if valid_target_dir == True and is_directory == True: # not necessary arguments to run them again but doing it for clarity purposes 
                                                                # but the success return string is required
            dir_content = os.listdir(norm_target_directory)                ### !!! IMPORTANT TO PASS ABSOLUTE PATH OF TARGET DIR

            list_content = [f'Result for "{directory}" directory:']   # initializing of list to store file info, also has the directory name string for output at index [0]
            
            for item in dir_content:
                item_abs_path = os.path.join(norm_target_directory, item) # CREATING ABSOLUTE PATHS FOR EACH ITEM using STANDARD LIBRARY os.path.join() method  ### !!! IMPORTANT TO PASS ABSOLUTE PATH OF TARGET DIR

                file_name = item                           # want the individual name of item, not absolute path of item
                file_size = os.path.getsize(item_abs_path)  # using STANDARD LIBRARY os.path.size() method in bytes
                file_is_dir = os.path.isdir(item_abs_path)  # using STANDARD LIBRARY os.path.is() method, results in a Bool

                file_info_str = f'  - {file_name}: file_size={file_size} bytes, is_dir={file_is_dir}'  # creating the f string to include all info from item

                list_content.append(file_info_str)   # appending the item info into list_content to concatenate later using .join() method

            dir_content_str = "\n".join(list_content) # can just "\n" as the seprater using the .join method to get desired format for str output

            return dir_content_str

            
            #return f'Success: "{directory}" is within the working directory' # no longer need, as we need to return directory content info instead since if an error is not raised, means it is a valid directory

    except Exception as e:
        return f'Error: {type(e).__name__} - {e}'
                        