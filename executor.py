import os
import sys


def execute_external_command(command, stdin_fd=None, stdout_fd=None, background=False):
    """
    Executes an external command.
    - Forks the current process to create a child process.
    - In the child process, it redirects stdin/stdout if needed and then executes the command.
    - In the parent process, it waits for the child to complete, unless it's a background process.
    """
    # Fork the process to create a child process.
    # pid will be 0 in the child, and the child's PID in the parent.
    pid = os.fork()

    if pid == 0:
        # --- Child Process ---
        # This code runs in the new child process.

        # Redirect standard input if a file descriptor is provided.
        if stdin_fd is not None:
            # os.dup2 duplicates the file descriptor, making stdin_fd the new standard input.
            os.dup2(stdin_fd, sys.stdin.fileno())
            os.close(stdin_fd)  # Close the original file descriptor.

        # Redirect standard output if a file descriptor is provided.
        if stdout_fd is not None:
            os.dup2(stdout_fd, sys.stdout.fileno())
            os.close(stdout_fd)

        try:
            # os.execvp replaces the current process with the new command.
            # It searches for the executable in the system's PATH.
            os.execvp(command[0], command)
        except FileNotFoundError:
            # If the command is not found, print an error and exit the child process.
            print(f"{command[0]}: command not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            # Handle other potential errors during execution.
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # --- Parent Process ---
        # This code runs in the original shell process.

        # If the command is not a background process, wait for the child to finish.
        if not background:
            # os.waitpid waits for the child process with the given PID to terminate.
            os.waitpid(pid, 0)


def execute_pipeline(left_command, right_command):
    """
    Executes a pipeline of two commands.
    - Creates a pipe, which is a one-way communication channel.
    - Forks two child processes, one for each command in the pipeline.
    - The first command's stdout is redirected to the pipe's write end.
    - The second command's stdin is redirected from the pipe's read end.
    """
    # Create a pipe. r is the read-end file descriptor, w is the write-end.
    r, w = os.pipe()

    # Execute the left-hand command of the pipeline.
    # Its standard output is redirected to the write-end of the pipe.
    execute_external_command(left_command, stdout_fd=w)
    # The parent process must close the write-end of the pipe.
    # This is crucial so that the right-hand command can receive an EOF (end-of-file)
    # when the left-hand command finishes writing.
    os.close(w)

    # Execute the right-hand command of the pipeline.
    # Its standard input is redirected from the read-end of the pipe.
    execute_external_command(right_command, stdin_fd=r)
    # The parent process closes the read-end of the pipe as it's no longer needed.
    os.close(r)
