def handle_redirection(command):
    """
    Detects < and > operators. Returns the cleaned command, input file, and output file.
    """
    stdin_file = None
    stdout_file = None
    clean_command = []

    i = 0
    while i < len(command):
        if command[i] == '<':
            if i + 1 < len(command):
                stdin_file = command[i+1]
                i += 2
            else:
                # Syntax error, ignore for now
                i += 1
        elif command[i] == '>':
            if i + 1 < len(command):
                stdout_file = command[i+1]
                i += 2
            else:
                i += 1
        else:
            clean_command.append(command[i])
            i += 1

    return clean_command, stdin_file, stdout_file


def handle_pipe(command):
    """
    Splits a command list into two parts if a pipe "|" is present.
    Returns (left_command, right_command) or (command, None).
    """
    if "|" in command:
        pipe_index = command.index("|")
        return command[:pipe_index], command[pipe_index+1:]
    return command, None


def handle_background_process(command):
    """
    Checks for a background operator "&" at the end of the command.
    Returns (command, is_background).
    """
    if command and command[-1] == "&":
        return command[:-1], True
    return command, False