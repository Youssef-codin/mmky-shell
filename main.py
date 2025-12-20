import os
import sys
import getpass
import socket

from parser import parse_input
from shell_builtins import handle_builtin_commands
from command_handler import handle_background_process, handle_pipe, handle_redirection
from executor import execute_external_command, execute_pipeline
from signals import setup_signal_handlers


def get_prompt():
    try:
        if os.environ.get('SHELL_COLOR', '1') == '0':
            return f"{os.getcwd()} $ "

        # Colored prompt
        user = getpass.getuser()
        host = socket.gethostname().split('.')[0]
        cwd = os.getcwd()
        return f"\x1b[34m{user}@{host}\x1b[0m:\x1b[36m{cwd}\x1b[0m \x1b[32m$ \x1b[0m"
    except Exception:
        return "$ "


def execute_command(cmd, stdin_file, stdout_file, bg):
    """
    Attempts to execute a command as a builtin first.
    If not a builtin, executes it as an external command.
    """

    # 1. Try Builtin
    # We must handle redirection manually for builtins because they run in-process.
    builtin_handled = False

    # Save original streams
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
                print(f"Redirection error (stdout): {e}", file=sys.stderr)
                return

        if stdin_file:
            try:
                f_in = open(stdin_file, 'r')
                sys.stdin = f_in
            except FileNotFoundError:
                print(f"Redirection error (stdin): {
                      stdin_file} not found", file=sys.stderr)
                return

        # Attempt execution
        if handle_builtin_commands(cmd):
            builtin_handled = True

    except Exception as e:
        print(f"Error executing builtin: {e}", file=sys.stderr)
    finally:
        # Restore streams
        sys.stdout = orig_stdout
        sys.stdin = orig_stdin
        if f_out:
            f_out.close()
        if f_in:
            f_in.close()

    # 2. External Command
    # If it wasn't a builtin, run it externally.
    # Note: execute_external_command handles its own redirection opening using the file paths.
    if not builtin_handled:
        execute_external_command(
            cmd, stdin_file=stdin_file, stdout_file=stdout_file, background=bg)


def process_input(input_str):
    if not input_str.strip():
        return

    cmd = parse_input(input_str)
    if not cmd:
        return

    # 1. Background Process
    cmd, bg = handle_background_process(cmd)

    # 2. Pipelines
    left, right = handle_pipe(cmd)
    if right:
        execute_pipeline(left, right)
        return

    # 3. Standard Command (Builtin or External)
    cmd, stdin, stdout = handle_redirection(cmd)
    if cmd:
        execute_command(cmd, stdin, stdout, bg)


def main():
    setup_signal_handlers()

    while True:
        try:
            prompt = get_prompt()
            cmd_input = input(prompt)
            process_input(cmd_input)

        except KeyboardInterrupt:
            print()  # Handle Ctrl+C gracefully
        except EOFError:
            print("\nExiting MMKY shell.")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
