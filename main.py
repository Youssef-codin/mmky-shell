# main.py
import os
import sys
import getpass
import socket
from parser import parse_input
from shell_builtins import handle_builtin_commands
from command_handler import handle_background_process, handle_pipe, handle_redirection
from executor import execute_external_command, execute_pipeline
from signals import setup_signal_handlers


def main():
    setup_signal_handlers()
    while True:
        try:
            # Handle Ctrl+C on input line
            try:
                # Build a colored prompt when enabled via SHELL_COLOR (default: on)
                color_enabled = os.environ.get('SHELL_COLOR', '1') != '0'
                if color_enabled:
                    USER = getpass.getuser()
                    HOST = socket.gethostname().split('.')[0]
                    CWD = os.getcwd()
                    BLUE = '\x1b[34m'
                    CYAN = '\x1b[36m'
                    GREEN = '\x1b[32m'
                    RESET = '\x1b[0m'
                    prompt = f"{BLUE}{
                        USER}@{HOST}{RESET}:{CYAN}{CWD}{RESET} {GREEN}$ {RESET}"
                else:
                    prompt = f"{os.getcwd()} $ "
                input_str = input(prompt)
            except KeyboardInterrupt:
                print()
                continue

            if not input_str.strip():
                continue

            command = parse_input(input_str)
            if not command:
                continue

            # Handle background and pipeline tokens first
            command, background = handle_background_process(command)
            left_pipeline, right_pipeline = handle_pipe(command)

            if right_pipeline:
                execute_pipeline(left_pipeline, right_pipeline)
            else:
                # Parse and remove any redirection tokens so builtins don't see them
                cmd, stdin_file, stdout_file = handle_redirection(command)

                # If parsing failed or there is no command, skip
                if not cmd:
                    continue

                # If it's a builtin, execute it in the parent but honor redirection
                if stdout_file or stdin_file:
                    # Temporarily replace sys.stdout / sys.stdin for builtin execution
                    orig_stdout = sys.stdout
                    orig_stdin = sys.stdin
                    f_out = None
                    f_in = None
                    try:
                        if stdout_file:
                            try:
                                f_out = open(stdout_file, 'w')
                                sys.stdout = f_out
                            except OSError as e:
                                print(f"Error opening output file '{
                                      stdout_file}': {e}", file=sys.stderr)
                                continue
                        if stdin_file:
                            try:
                                f_in = open(stdin_file, 'r')
                                sys.stdin = f_in
                            except FileNotFoundError:
                                print(f"Error: Input file '{
                                      stdin_file}' not found.", file=sys.stderr)
                                continue

                        if handle_builtin_commands(cmd):
                            continue
                    finally:
                        if f_out:
                            f_out.close()
                        if f_in:
                            f_in.close()
                        sys.stdout = orig_stdout
                        sys.stdin = orig_stdin

                # Not a builtin (or no redirection), execute external command
                if handle_builtin_commands(cmd):
                    continue

                execute_external_command(
                    cmd,
                    stdin_file=stdin_file,
                    stdout_file=stdout_file,
                    background=background
                )

        except EOFError:
            print("\nExiting shell.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
