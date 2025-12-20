import os # MS- for system calls
import sys # MS- Access to stdin, stdout & exit

def execute_external_command(command, stdin_file=None, stdout_file=None, stdin_fd=None, stdout_fd=None, background=False, wait=True):
    try:
        pid = os.fork()
    except OSError as e:
        print(f"Fork failed: {e}", file=sys.stderr)
        return

    if pid == 0: # MS- Child Process
        try:
            if stdin_file:
                try:
                    fd_in = os.open(stdin_file, os.O_RDONLY)
                    os.dup2(fd_in, sys.stdin.fileno()) # MS- to ready from the 'inputfile' not the keyboard (with FD no = 0)
                    os.close(fd_in) # MS- to remove duplicates as both (fd_in + stdin 0) : pointing to 'inputfile'
                except FileNotFoundError:
                    print(f"Error: Input file '{stdin_file}' not found.", file=sys.stderr)
                    sys.exit(1)
                except PermissionError:
                    print(f"Error: Permission denied for input '{stdin_file}'.", file=sys.stderr)
                    sys.exit(1)

            if stdout_file:
                try:
                    # MS- Open file for writing, create if not exists, truncate
                    fd_out = os.open(stdout_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
                    os.dup2(fd_out, sys.stdout.fileno())
                    os.close(fd_out)
                except OSError as e:
                    print(f"Error opening output file '{stdout_file}': {e}", file=sys.stderr)
                    sys.exit(1)

            # MS- Handle Pipe Redirection (FDs) FOIITS
            if stdin_fd is not None:
                os.dup2(stdin_fd, sys.stdin.fileno()) # MS- to prevent closing stdin (i compare the NOs here not the pointers)
                if stdin_fd != sys.stdin.fileno():
                    os.close(stdin_fd)

            if stdout_fd is not None:
                os.dup2(stdout_fd, sys.stdout.fileno())
                if stdout_fd != sys.stdout.fileno():
                    os.close(stdout_fd)

            # MS- Execute Command
            os.execvp(command[0], command)

        except FileNotFoundError:
            print(f"{command[0]}: command not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # MS- Parent Process
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
