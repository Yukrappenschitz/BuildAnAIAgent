import os
import subprocess
from config import Py_File_Execution_Time_Limit  


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try: 
        abs_working_dir = os.path.abspath(working_directory)

        joined_file_path = os.path.join(abs_working_dir, file_path)

        norm_abs_file_path = os.path.normpath(joined_file_path)

        common_abs_path = os.path.commonpath([abs_working_dir, norm_abs_file_path])

        valid_file_path: bool = abs_working_dir == common_abs_path

        if valid_file_path == False:   # 2. If the file_path is outside the working_directory, return the error string 
    
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        
        is_file: bool = os.path.isfile(norm_abs_file_path)

        if is_file == False:     # 3. Make sure that file_path exists and points to a regular file (rather than, e.g., a directory). os.path.isfile() answers both questions at once. If this check fails, return an error string

            return f'Error: "{file_path}" does not exist or is not a regular file'

        # CHECKING IF GIVEN FILE_PATH IS A PYTHON FILE by chekcing extension
        sliced_file_path = file_path[-3:]  # just need to check last 3 chars of file_path str to see if its ".py" extension(file)

        if sliced_file_path != '.py':  # 4. If the file name doesn't end with .py, return an error string

            return f'Error: "{file_path}" is not a Python file'

        if valid_file_path == True and is_file == True and sliced_file_path == ".py":
                
                file_timeout = Py_File_Execution_Time_Limit # 30 seconds

                command = ["python", norm_abs_file_path]                  # 5. Assuming all those checks passed, we're going to use a subprocess to run the file. But first we need to build the command to run – in the form of a list of strings. Start with something like this:
                
                if args != None:
                    command.extend(args)         # 6. If any additional args were provided, add them to the command list. You can use the .extend() method to do this.
                                            
                                            # 7. Use the subprocess.run() function to run the command that you built. This will return a CompletedProcess object, which you'll want to assign to a variable
                result = subprocess.run(               
                    command, 
                    capture_output= True,     # 7.2 Capture output (i.e., stdout and stderr).
                    text= True,              # 7.3 Decode the output to strings, rather than bytes; this is done by setting text=True.
                    timeout= file_timeout        # 7.4 Set a timeout of 30 seconds to prevent infinite execution.
                )
            # CONSTRUCTING OUTPUT STRING FROM resulting CompletedProcess object from running subprocess.run()
                output_string = f''   # 8. Build an output string based on the CompletedProcess object

                return_code = result.returncode

                if return_code != 0:
                    output_string += f'Process exited with code {return_code}'  # 8.1 If the process exited with a non-zero returncode, include "Process exited with code X".

                std_out = result.stdout
                std_err = result.stderr

                if std_out == None and std_err == None:        # 8.2 If both stdout and stderr contained no output (both of which are attributes of CompletedProcess), add "No output produced".
                    output_string += f'No output produced'
                else:
                    output_string += f'STDOUT:{std_out}STDERR:{std_err}'    # 8.3 Otherwise, include any text in stdout prefixed with STDOUT:, and any text in stderr prefixed with STDERR:.

                return output_string                  # 9. Return the output string.
     
    except Exception as e:
        return f"Error: executing Python file: {e}"   # 10. As usual, if any exception is raised anywhere in this function, catch it and return an error string:


    

