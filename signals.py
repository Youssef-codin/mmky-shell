import signal
import os

def handle_sigint(sig,frame):
    """
    Signal handler for SIGINT (Ctrl+C).
    """
    print("\nCaught Ctrl+C. Use 'exit' to quit the shell.")

def handle_sigchld(sig,frame):
    """
    Signal handler for SIGCHLD.
    Reaps zombie processes created by background jobs.
    WNOHANG ensures we don't block if no child has exited.
    """
    try:
        while True:
            # MS- '-1' means wait for any child process
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
    except ChildProcessError: # MS- whn no exited child
        pass
    except OSError:
        pass

def setup_signal_handlers():
    """
    Sets up the signal handlers for the shell.
    """
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGCHLD, handle_sigchld)
