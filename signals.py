import signal
import sys


def handle_sigint(sig, frame):
    """
    Signal handler for SIGINT (Ctrl+C).
    """
    print("\nCaught Ctrl+C. Exiting gracefully.")
    sys.exit(0)


def setup_signal_handlers():
    """
    Sets up the signal handlers for the shell.
    """
    signal.signal(signal.SIGINT, handle_sigint)
