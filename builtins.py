import os
import sys

class ShellBuiltins:  
    def __init__(self):
        """Initialize shell builtins with environment and state."""
        self.previous_dir = None  # For 'cd -' functionality
        self.shell_vars = {}  # Store shell variables
        
    def handle_builtin_commands(self, command):
        """
        Checks for and handles built-in shell commands.
        
        Args:
            command: A list of strings representing the command and arguments.
        
        Returns:
            True if the command was a built-in and was handled.
            False otherwise, indicating that the command should be executed externally.
        """
        if not command or len(command) == 0:
            return False
            
        cmd = command[0].lower()
        
        # Map commands to their handler methods
        builtin_commands = {
            'cd': self.cmd_cd,
            'exit': self.cmd_exit,
            'pwd': self.cmd_pwd,
            'echo': self.cmd_echo,
            'export': self.cmd_export,
            'unset': self.cmd_unset,
            'env': self.cmd_env,
            'help': self.cmd_help,
            'history': self.cmd_history,
            'type': self.cmd_type,
        }
        
        if cmd in builtin_commands:
            try:
                builtin_commands[cmd](command)
                return True
            except Exception as e:
                print(f"Error executing '{cmd}': {e}", file=sys.stderr)
                return True  # Still a built-in, just failed
        
        return False
    
    def cmd_cd(self, command):
        """
        Change the current working directory.
        
        Usage:
            cd [directory]
            cd          - Go to home directory
            cd -        - Go to previous directory
            cd ~        - Go to home directory
            cd ..       - Go to parent directory
        """
        if len(command) == 1:
            # No argument - go to home directory
            target_dir = os.path.expanduser('~')
        elif command[1] == '-':
            # Go to previous directory
            if self.previous_dir is None:
                print("cd: OLDPWD not set", file=sys.stderr)
                return
            target_dir = self.previous_dir
            print(target_dir)  # Print the directory we're changing to
        else:
            # Expand ~ and handle the path
            target_dir = os.path.expanduser(command[1])
        
        try:
            # Store current directory before changing
            current_dir = os.getcwd()
            
            # Change directory
            os.chdir(target_dir)
            
            # Update previous directory
            self.previous_dir = current_dir
            
            # Update PWD environment variable
            os.environ['PWD'] = os.getcwd()
            
        except FileNotFoundError:
            print(f"cd: {target_dir}: No such file or directory", file=sys.stderr)
        except NotADirectoryError:
            print(f"cd: {target_dir}: Not a directory", file=sys.stderr)
        except PermissionError:
            print(f"cd: {target_dir}: Permission denied", file=sys.stderr)
    
    def cmd_exit(self, command):
        """
        Exit the shell.
        
        Usage:
            exit [n]    - Exit with status code n (default: 0)
        """
        exit_code = 0
        
        if len(command) > 1:
            try:
                exit_code = int(command[1])
            except ValueError:
                print(f"exit: {command[1]}: numeric argument required", file=sys.stderr)
                exit_code = 2
        
        print("Exiting shell...")
        sys.exit(exit_code)
    
    def cmd_pwd(self, command):
        """
        Print the current working directory.
        
        Usage:
            pwd [-L | -P]
            -L: Logical path (default, follows symlinks)
            -P: Physical path (resolves symlinks)
        """
        try:
            if len(command) > 1 and command[1] == '-P':
                # Physical path - resolve symlinks
                print(os.path.realpath(os.getcwd()))
            else:
                # Logical path
                print(os.getcwd())
        except Exception as e:
            print(f"pwd: error: {e}", file=sys.stderr)
    
    def cmd_echo(self, command):
        """
        Display a line of text.
        
        Usage:
            echo [string ...]
            echo -n [string ...]  - Don't output trailing newline
        """
        no_newline = False
        start_index = 1
        
        # Check for -n flag
        if len(command) > 1 and command[1] == '-n':
            no_newline = True
            start_index = 2
        
        # Join arguments with spaces
        output = ' '.join(command[start_index:])
        
        # Expand environment variables (basic $VAR expansion)
        output = self._expand_variables(output)
        
        # Print with or without newline
        if no_newline:
            print(output, end='')
        else:
            print(output)
    
    def cmd_export(self, command):
        """
        Set environment variables.
        
        Usage:
            export VAR=value
            export VAR           - Mark variable for export
        """
        if len(command) == 1:
            # No arguments - display all exported variables
            for key, value in os.environ.items():
                print(f"export {key}=\"{value}\"")
            return
        
        for arg in command[1:]:
            if '=' in arg:
                # VAR=value format
                var, value = arg.split('=', 1)
                os.environ[var] = value
                self.shell_vars[var] = value
            else:
                # Just VAR - export existing variable if it exists
                if arg in self.shell_vars:
                    os.environ[arg] = self.shell_vars[arg]
                else:
                    print(f"export: {arg}: not found", file=sys.stderr)
    
    def cmd_unset(self, command):
        """
        Unset environment variables.
        
        Usage:
            unset VAR [VAR2 ...]
        """
        if len(command) == 1:
            print("unset: not enough arguments", file=sys.stderr)
            return
        
        for var in command[1:]:
            if var in os.environ:
                del os.environ[var]
            if var in self.shell_vars:
                del self.shell_vars[var]
    
    def cmd_env(self, command):
        """
        Display all environment variables.
        
        Usage:
            env
        """
        for key, value in sorted(os.environ.items()):
            print(f"{key}={value}")
    
    def cmd_help(self, command):
        """
        Display help information about built-in commands.
        
        Usage:
            help [command]
        """
        if len(command) == 1:
            # General help
            print("Shell Built-in Commands:")
            print("  cd [dir]       - Change directory")
            print("  pwd            - Print working directory")
            print("  echo [args]    - Display text")
            print("  exit [n]       - Exit shell with status n")
            print("  export VAR=val - Set environment variable")
            print("  unset VAR      - Unset environment variable")
            print("  env            - Display environment variables")
            print("  help [cmd]     - Show help for command")
            print("  history        - Show command history")
            print("  type cmd       - Show command type")
            print("\nType 'help <command>' for more information on a specific command.")
        else:
            # Help for specific command
            cmd = command[1]
            methods = {
                'cd': self.cmd_cd,
                'pwd': self.cmd_pwd,
                'echo': self.cmd_echo,
                'exit': self.cmd_exit,
                'export': self.cmd_export,
                'unset': self.cmd_unset,
                'env': self.cmd_env,
                'help': self.cmd_help,
                'history': self.cmd_history,
                'type': self.cmd_type,
            }
            
            if cmd in methods:
                print(f"\n{cmd}: {methods[cmd].__doc__}")
            else:
                print(f"help: no help topics match '{cmd}'", file=sys.stderr)
    
    def cmd_history(self, command):
        """
        Display command history.
        
        Usage:
            history
            
        Note: This is a placeholder. Actual history management
        should be implemented in the main shell loop.
        """
        print("history: command history feature not yet implemented")
        print("(This should be integrated with the main shell loop)")
    
    def cmd_type(self, command):
        """
        Display information about command type.
        
        Usage:
            type command [command2 ...]
        """
        if len(command) == 1:
            print("type: not enough arguments", file=sys.stderr)
            return
        
        builtins = ['cd', 'pwd', 'echo', 'exit', 'export', 'unset', 
                   'env', 'help', 'history', 'type']
        
        for cmd in command[1:]:
            if cmd in builtins:
                print(f"{cmd} is a shell builtin")
            else:
                # Check if it's in PATH
                path = self._find_in_path(cmd)
                if path:
                    print(f"{cmd} is {path}")
                else:
                    print(f"{cmd}: not found")
    
    def _expand_variables(self, text):
        """
        Expand environment variables in text.
        Handles $VAR and ${VAR} syntax.
        """
        import re
        
        # Handle ${VAR} syntax
        def replace_braced(match):
            var = match.group(1)
            return os.environ.get(var, '')
        
        text = re.sub(r'\$\{([^}]+)\}', replace_braced, text)
        
        # Handle $VAR syntax
        def replace_simple(match):
            var = match.group(1)
            return os.environ.get(var, '')
        
        text = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace_simple, text)
        
        return text
    
    def _find_in_path(self, command):
        """
        Search for command in PATH directories.
        Returns full path if found, None otherwise.
        """
        path_dirs = os.environ.get('PATH', '').split(os.pathsep)
        
        for directory in path_dirs:
            full_path = os.path.join(directory, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path
        
        return None


# Create a global instance for easy importing
_builtin_handler = ShellBuiltins()

def handle_builtin_commands(command):
    """
    Global function to handle built-in commands.
    This maintains backward compatibility with the original interface.
    
    Args:
        command: A list of strings representing the command and arguments.
    
    Returns:
        True if the command was a built-in and was handled.
        False otherwise, indicating that the command should be executed externally.
    """
    return _builtin_handler.handle_builtin_commands(command)


# For direct module usage
if __name__ == "__main__":
    print("Shell Built-ins Module")
    print("This module should be imported by the main shell.")
    print("\nAvailable built-in commands:")
    test_handler = ShellBuiltins()
    test_handler.cmd_help(['help'])