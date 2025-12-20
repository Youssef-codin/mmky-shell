import os
import sys

# Shell state
_PREVIOUS_DIR = None
_HISTORY = []

def handle_builtin_commands(command):
    """
    Checks for and handles built-in shell commands.
    Returns True if handled, False otherwise.
    """
    global _PREVIOUS_DIR, _HISTORY

    if not command:
        return False

    # Track History
    _HISTORY.append(' '.join(command))
    
    cmd = command[0]

    if cmd == 'cd':
        if len(command) == 1:
            target_dir = os.path.expanduser('~')
        elif command[1] == '-':
            if _PREVIOUS_DIR is None:
                print("cd: OLDPWD not set", file=sys.stderr)
                return True
            target_dir = _PREVIOUS_DIR
            print(target_dir)
        else:
            target_dir = command[1]

        try:
            current = os.getcwd()
            os.chdir(target_dir)
            _PREVIOUS_DIR = current
        except FileNotFoundError:
            print(f"cd: {target_dir}: No such file or directory", file=sys.stderr)
        except NotADirectoryError:
            print(f"cd: {target_dir}: Not a directory", file=sys.stderr)
        except PermissionError:
            print(f"cd: {target_dir}: Permission denied", file=sys.stderr)
        return True

    elif cmd == 'exit':
        try:
            status = int(command[1]) if len(command) > 1 else 0
        except ValueError:
            status = 0
        print("Exiting shell...")
        sys.exit(status)

    elif cmd == 'pwd':
        print(os.getcwd())
        return True

    elif cmd == 'echo':
        print(' '.join(command[1:]))
        return True

    elif cmd == 'history':
        for i, entry in enumerate(_HISTORY, 1):
            print(f"{i}  {entry}")
        return True

    elif cmd == 'help':
        print("Shell Built-ins: cd, pwd, echo, exit, history, help")
        return True

    return False
