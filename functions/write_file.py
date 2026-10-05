import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:

        abs_working_dir:str = os.path.abspath(working_directory)

        joined_file_path:str = os.path.join( abs_working_dir, file_path)

        norm_abs_file_path:str = os.path.normcase(joined_file_path)     # normalized ABSOLUTE of given File_path

        common_abs_path: str = os.path.commonpath([abs_working_dir, norm_abs_file_path])   # finding common path to see if given file_path is under working_dir if commonpath between them is working_dir

        valid_file_path: bool = common_abs_path == abs_working_dir    # Bool to store valid_file_path

        if valid_file_path == False:               # 2. If the file_path is outside the working_directory, return an error string like the one below

            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        is_dir: bool = os.path.isdir(norm_abs_file_path)  # Bool to store is_dir

        if is_dir == True:                   # 3. If the file_path points to an existing directory (this is what os.path.isdir() checks for), return an error string:

            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(norm_abs_file_path)  # os.path.dirname(): Get the parent directory of a given path, need to be pass it to os.makedir(parent_directory) otherwise will bug out and make the given file name as directory

        os.makedirs(parent_dir, exist_ok=True)  # 4. Make sure that all parent directories of the file_path exist. 
                                                        # os.makedirs() with the exist_ok=True argument to create any missing directories. If the necessary directory structure already exists, this will do nothing – which is what we want.
               
        if valid_file_path == True and is_dir == False:

            with open(norm_abs_file_path,"w") as f:  # 5. Open the file at file_path in write mode ("w") and overwrite its contents with the content argument.

                f.write(content)
                                                    # !!! It's important to return a success string so that our LLM knows that the action it took actually worked. Feedback loops, feedback loops!
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {type(e).__name__} - {e}'