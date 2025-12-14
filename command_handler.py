def handle_redirection(command: list[str]) -> tuple[list[str], str | None, str | None]:
# command_handler.py
def handle_redirection(command):
    """
    Detects < and > operators. Returns the cleaned command and filenames.
    """

    # Handles I/O redirection (<, >).
    # Placeholder for redirection logic
    # This function will identify redirection operators and file names,
    # modify the command list, and set up file descriptors.
    try:
        outputDirection = command.index(">")
    except ValueError:
        outputDirection = None

    try:
        inputDirection = command.index("<")
    except ValueError:
        inputDirection = None

    if outputDirection != None:
        return command[:outputDirection], None, command[outputDirection + 1]
    elif inputDirection != None:
        return command[:inputDirection], command[inputDirection + 1], None

    return command, None, None  # command, stdin_fd, stdout_fd


def handle_pipe(command: list[str]) -> tuple[list[str], list[str] | None]:
    """
    Splits a command list into two parts if a pipe "|" is present.

    Args:
        command: A list of strings representing the command and arguments.

    Returns:
        A tuple containing:
        - A list representing the left-hand side of the pipe.
        - A list representing the right-hand side of the pipe, or None if no pipe exists.
    """
    # Handles piping between commands.
    # Placeholder for piping logic
    # This function will split the command into parts based on the pipe operator '|'.
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
                print("Syntax error: no file after <")
                return [], None, None
        elif command[i] == '>':
            if i + 1 < len(command):
                stdout_file = command[i+1]
                i += 2
            else:
                print("Syntax error: no file after >")
                return [], None, None
        else:
            clean_command.append(command[i])
            i += 1

    return clean_command, stdin_file, stdout_file


def handle_pipe(command):
    if "|" in command:
        pipe_index = command.index("|")
        return command[:pipe_index], command[pipe_index+1:]
    return command, None


def handle_background_process(command: list[str]) -> tuple[list[str], bool]:
    """
    Checks for a background operator "&" and removes it from the command.

    Args:
        command: A list of strings representing the command and arguments.

    Returns:
        A tuple containing:
        - The command list with the "&" operator removed.
        - A boolean indicating if the process should run in the background.
    """
    # Handles background processes (using &).
    background = False
    if "&" in command:
        background = True
        command.remove("&")
    return command, background
def handle_background_process(command):
    if command and command[-1] == "&":
        return command[:-1], True
    return command, False
