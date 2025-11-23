## Team Roles

1.  **Execution & Process Lead:**
    *   **Focus:** `executor.py`, `signals.py`.
    *   **Responsibilities:** Command execution (`fork`, `exec`, `wait`), signal handling, job control.

2.  **Parser & Input Specialist:**
    *   **Focus:** `parser.py`.
    *   **Responsibilities:** Advanced command line parsing (quotes, escapes, variables), converting raw input to structured commands.

3.  **Pipeline & Redirection Handler:**
    *   **Focus:** `command_handler.py`, `main.py`.
    *   **Responsibilities:** Implementing I/O redirection (`<`, `>`, `>>`), setting up command pipelines (`|`), overall shell loop management.

4.  **User Features & Built-ins Developer:**
    *   **Focus:** `builtins.py`, new feature files.
    *   **Responsibilities:** Implementing internal shell commands (`cd`, `exit`, etc.)

## Workflow

1.  **Input (P3):** User provides command.
2.  **Parsing (P2):** Input parsed into structured command.
3.  **Built-in Check (P4):** If command is built-in, P4 executes it.
4.  **Command Setup (P3):** Sets up pipes/redirection for external commands.
5.  **Execution (P1):** Runs the external command.
