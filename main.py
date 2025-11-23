import os
import sys

from parser import parse_input
from builtins import handle_builtin_commands
from command_handler import handle_background_process, handle_pipe, handle_redirection
from executor import execute_external_command, execute_pipeline
from signals import setup_signal_handlers


def main():
    """Main loop of the shell."""
    setup_signal_handlers()
    while True:
        try:
            prompt = f"{os.getcwd()} $ "
            input_str = input(prompt)
            if not input_str:
                continue

            command = parse_input(input_str)

            if handle_builtin_commands(command):
                continue

            command, background = handle_background_process(command)

            left_pipeline, right_pipeline = handle_pipe(command)

            if right_pipeline:
                execute_pipeline(left_pipeline[0], right_pipeline[0])
            else:
                cmd, stdin_fd, stdout_fd = handle_redirection(command)
                execute_external_command(cmd, stdin_fd, stdout_fd, background)

        except EOFError:
            print("\nExiting shell.")
            break
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
