# command_handler.py
def handle_redirection(command):
    """
    Detects < and > operators. Returns the cleaned command and filenames.
    """
    stdin_file = None
    stdout_file = None
    clean_command = []
    
    i = 0
    while i < len(command):
        if command[i] == '<':
            if i + 1 < len(command):
                stdin_file = command[i+1]
                i += 2 # Skip operator and filename
            else:
                print("Syntax error: no file after <")
                return [], None, None
        elif command[i] == '>':
            if i + 1 < len(command):
                stdout_file = command[i+1]
                i += 2 # Skip operator and filename
            else:
                print("Syntax error: no file after >")
                return [], None, None
        else:
            clean_command.append(command[i])
            i += 1

    return clean_command, stdin_file, stdout_file


def handle_pipe(command):
    if "|" in command:
        try:
            pipe_index = command.index("|")
            return command[:pipe_index], command[pipe_index+1:]
        except ValueError:
            pass
    return command, None


def handle_background_process(command):
    if command and command[-1] == "&":
        return command[:-1], True
    return command, False
