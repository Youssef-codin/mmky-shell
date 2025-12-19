# executor.py
import os
import sys

def execute_external_command(command, stdin_file=None, stdout_file=None, stdin_fd=None, stdout_fd=None, background=False, wait=True):
    try:
        pid = os.fork()
    except OSError as e:
        print(f"Fork failed: {e}", file=sys.stderr)
        return

    if pid == 0:
        # --- Child Process ---
        try:
            # 1. Handle Input Redirection (File)
            if stdin_file:
                try:
                    fd_in = os.open(stdin_file, os.O_RDONLY)
                    os.dup2(fd_in, sys.stdin.fileno())
                    os.close(fd_in)
                except FileNotFoundError:
                    print(f"Error: Input file '{stdin_file}' not found.", file=sys.stderr)
                    sys.exit(1)
                except PermissionError:
                    print(f"Error: Permission denied for input '{stdin_file}'.", file=sys.stderr)
                    sys.exit(1)

            # 2. Handle Output Redirection (File)
            if stdout_file:
                try:
                    # Open file for writing, create if not exists, truncate
                    fd_out = os.open(stdout_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    os.dup2(fd_out, sys.stdout.fileno())
                    os.close(fd_out)
                except OSError as e:
                    print(f"Error opening output file '{stdout_file}': {e}", file=sys.stderr)
                    sys.exit(1)

            # 3. Handle Pipe Redirection (FDs)
            if stdin_fd is not None:
                os.dup2(stdin_fd, sys.stdin.fileno())
                if stdin_fd != sys.stdin.fileno():
                    os.close(stdin_fd)

            if stdout_fd is not None:
                os.dup2(stdout_fd, sys.stdout.fileno())
                if stdout_fd != sys.stdout.fileno():
                    os.close(stdout_fd)

            # 4. Execute Command
            os.execvp(command[0], command)

        except FileNotFoundError:
            # This specific error is now ONLY for the command itself
            print(f"{command[0]}: command not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # --- Parent Process ---
        if stdin_fd is not None:
            os.close(stdin_fd)
        if stdout_fd is not None:
            os.close(stdout_fd)

        if not background and wait:
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass

def execute_pipeline(left_command, right_command):
    r, w = os.pipe()
    execute_external_command(left_command, stdout_fd=w, wait=False)
    execute_external_command(right_command, stdin_fd=r, wait=True)
