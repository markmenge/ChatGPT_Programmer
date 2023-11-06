# File: code_patcher.py - This file is a higher-level code patcher.
import subprocess
from redbaron import RedBaron

class python_patcher:

    def __init__(self, filename, source_code: str):
        if source_code is None or source_code.strip() == "":
            source_code = "# MAIN\n"
        self.red = RedBaron(source_code)
        self.filename = filename
        self.output = None

        # Ensure that the #MAIN anchor exists
        if "# MAIN" not in self.red.dumps():
            self.red.insert(0, "# MAIN\n")

    # unused I think
    def has_function(self, func_name: str) -> bool:
        """
        Checks if a function with the given name exists in the code.
        :param func_name: The name of the function to check for.
        :return: True if the function exists, False otherwise.
        """
        for node in self.red.find_all('def'):
            if node.name == func_name:
                return True
        return False

    def add_function(self, function_code: str, after: str = None, before: str = None):
        """
        Adds a function to the source code. If the function already exists, removes the original.
        :param function_code: The full function code to add.
        :param after: (Optional) The name of an existing function to add the new function after.
        :param before: (Optional) The name of an existing function to add the new function before.
        """
        function_node = RedBaron(function_code.strip())[0]
        
        # If the function already exists, remove it.
        func_name = function_node.name
        existing_functions = self.red.find_all('def', name=func_name)
        for func in existing_functions:
            self.red.remove(func)
    
        # Check if the source code is empty.
        if not str(self.red).strip():
            self.red = RedBaron(function_code)
            return

        if after:
            functions = self.red.find_all('def', name=after)
            if functions:
                functions[-1].insert_after(function_node)
                return

        if before:
            functions = self.red.find_all('def', name=before)
            if functions:
                functions[0].insert_before(function_node)
                return

        # If neither after nor before are specified, append at the end.
        self.red.append(function_node)

    def get_patched_code(self):
        return self.red.dumps()

    def find_imports(self) -> list:
        """
        Returns a list of all import statements in the source code.
        """
        return [str(node) for node in self.red.find_all('Import')]

    def add_import(self, import_line: str):
        """
        Adds an import statement to the source code.
        :param module: The name of the module to import.
        """
        import_node = RedBaron(f"{import_line}\n")[0]
        imports = self.red.find_all('Import')
        if imports:
            # Add after the last import
            imports[-1].insert_after(import_node)
        else:
            # If no imports are found, add at the beginning
            self.red.insert(0, import_node)

    def delete_import(self, import_line: str):
        """
        Deletes an import statement from the source code.
        :param module: The name of the module to remove.
        """
        for node in self.red.find_all('Import'):
            if node.dumps().strip() == f"{import_line}":
                node.parent.remove(node)

    def find_functions(self) -> list:
        """
        Returns a list of all function (def) names in the source code.
        """
        return [node.name for node in self.red.find_all('Def')]

    def delete_function(self, function_name: str):
        """
        Deletes a function from the source code.
        :param function_name: The name of the function to delete.
        """
        functions = self.red.find_all('Def', name=function_name)
        for func in functions:
            func.parent.remove(func)

    def find_classes(self) -> list:
        """
        Returns a list of all class names in the source code.
        """
        pass

    def add_class(self, class_code: str, after: str = None, before: str = None):
        """
        Adds a class to the source code.
        :param class_code: The full class code to add.
        :param after: (Optional) The name of an existing class to add the new class after.
        :param before: (Optional) The name of an existing class to add the new class before.
        """
        pass

    def delete_class(self, class_name: str):
        """
        Deletes a class from the source code.
        :param class_name: The name of the class to delete.
        """
        pass

    def add_to_main_body(self, code_block: str, after: bool = True):
        """
        Adds a code block to the main body of the source code.
        :param code_block: The code block to add.
        :param after: Whether to add the code block after the existing main body (True) or before (False).
        """
        pass

    def print_code(self):
        """
        Prints the current state of the source code.
        """
        print(self.get_patched_code())

    def find_classes(self) -> list:
        """
        Returns a list of all class names in the source code.
        """
        return [node.name for node in self.red.find_all('Class')]

    def add_class(self, class_code: str, after: str = None, before: str = None):
        """
        Adds a class to the source code.
        :param class_code: The full class code to add.
        :param after: (Optional) The name of an existing class to add the new class after.
        :param before: (Optional) The name of an existing class to add the new class before.
        """
        class_node = RedBaron(class_code)[0]

        if after:
            classes = self.red.find_all('Class', name=after)
            if classes:
                classes[-1].insert_after(class_node)
                return

        if before:
            classes = self.red.find_all('Class', name=before)
            if classes:
                classes[0].insert_before(class_node)
                return

        # If neither after nor before are specified, append at the end.
        self.red.append(class_node)

    def delete_class(self, class_name: str):
        """
        Deletes a class from the source code.
        :param class_name: The name of the class to delete.
        """
        classes = self.red.find_all('Class', name=class_name)
        for cls in classes:
            cls.remove()

    def find_main_body(self) -> str:
        """
        Returns the main body of the source code (i.e., code outside functions and classes).
        """
        body = [str(node) for node in self.red if node.type not in ["Class", "Def", "Import"]]
        return '\n'.join(body)

    def set_main_body(self, code_block: str):
        """
        Sets the main body of the source code.
        :param code_block: The code block to set as the main body.
        """
        # Collect nodes to keep
        nodes_to_keep = [node for node in self.red if node.type in ["class", "def", "import"] or "# MAIN" in node.dumps()]

        # Ensure that the code block doesn't start with unnecessary whitespaces
        code_block = '\n'.join(line.rstrip() for line in code_block.splitlines())

        # Create a new RedBaron object with the code block
        new_red = RedBaron(code_block)

        # Remove existing main body content, preserving Class, Def, Import, and "# MAIN" anchor
        nodes_to_remove = [node for node in self.red if node not in nodes_to_keep]
        for node in nodes_to_remove:
            self.red.remove(node)

        # Insert the new main body content at the end of the RedBaron object
        self.red.extend(new_red)

    def rearrange_code(self):
        """
        Rearranges the code to ensure import statements, class and function definitions come before the main body.
        """
        # Collect import statements and their positions
        imports = [node for node in self.red if node.type == "import" or node.type == "from_import"]

        # Sort imports by their original positions
        # imports.sort(key=lambda x: x[0])

        # Collect class definitions
        classes = [node for node in self.red if node.type == "class"]
        
        # Collect function definitions
        functions = [node for node in self.red if node.type == "def"]

        # Collect the main body content
        main_body = [node for node in self.red if node not in imports and node not in classes and node not in functions]

        # Create a new RedBaron object with the imports, classes, functions, and main body content in order
        final_code = '\n'.join([str(node).rstrip() for node in (imports + classes + functions + main_body)])
        self.red = RedBaron(final_code)

    # text_commands executes a commands from an array of strings in commands_list e.g.
    # 0: "run"s
    # 1: "printcode"
    def text_commands(self, commands_list):
        self.output = ""
        i = 0
        while i < len(commands_list):
            command = commands_list[i].strip()
            if command in {'setmain', 'addfunc'}:
                i += 1
                arg_str = ''
                while i < len(commands_list) and commands_list[i].strip() != '###':
                    arg_str += commands_list[i] + '\n'
                    i += 1
                self.text_command(command, arg_str)
            else:
                args = command.split(maxsplit=1)
                if len(args) == 1:
                    self.text_command(args[0], '')
                elif len(args) == 2:
                    self.text_command(args[0], args[1])
            i += 1

    # ChatGPT gives us a lot of noise. Try to get the meaningful commands out of it.
    def process_chatgpt_response(self, text_and_commands: str):
        pp_commands = {"addfunc", "delfunc", "addimport", "delimport", "setmain", "printcode", "run"}

        # Remove text before triple backticks and after triple backticks
        if '```' in text_and_commands:
            start = text_and_commands.find('```') + 3
            end = text_and_commands.rfind('```')
            text_and_commands = text_and_commands[start:end]

        # Replace addfunc def with addfunc\ndef
        text_and_commands = text_and_commands.replace("addfunc def", "addfunc\ndef")
        
        commands_list = text_and_commands.split('\n')

        # First skip ChatGPT's explanation, look for a command to start with
        i = 0
        while i < len(commands_list):
            command = commands_list[i].strip().split(' ', 1)[0]  # Use ' ' as the delimiter and 1 as the maxsplit value
            if command in pp_commands:
                break
            i += 1

        commands_list = commands_list[i:len(commands_list)]
        self.text_commands(commands_list)

    def run_python_script(self, filename):
        try:
            # Run the Python script and capture the output and error
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True
            )
            # Combine stdout and stderr for complete output
            run_python_output = "*** Program output ***\n" + result.stdout + "\n" + (result.stderr or "")
            print(run_python_output)
            self.output = self.output + run_python_output
            
            # Raise an error if the process returned a non-zero exit status
            if result.returncode != 0:
                print(f"Script exited with code {result.returncode}")
                # Handle the exit according to your application's logic, e.g., by exiting the main program
                exit(1)  # Uncomment this if you want to exit the main program
            
        except subprocess.CalledProcessError as e:
            # An error occurred, capture the output from stdout and stderr
             run_python_output = f"An error occurred: Exit code {e.returncode}\n{e.stdout}\n{e.stderr}"
             print(run_python_output)
             self.output = self.output + run_python_output

    def text_command(self, cmd, str):
        the_code = self.get_patched_code()
        if cmd == "run":
            self.run_python_script("test.py")
        elif cmd == "addfunc":
            self.add_function(str)
        elif cmd == "delfunc":
            self.delete_function(str)
        elif cmd == "addimport":
            self.add_import(str)
        elif cmd == "delimport":
            self.delete_import(str)
        elif cmd == "setmain":
            self.set_main_body(str)            
        elif cmd == "printcode":
            pass
        self.rearrange_code()
        if cmd == "printcode":
            print(self.get_patched_code())
            self.output = self.output + "*** Program listing ***\n" + self.get_patched_code()
        
        # setting the_code for debugging purposes
        the_code = self.get_patched_code()
        with open(self.filename, 'w') as file:
            file.write(self.get_patched_code())            
