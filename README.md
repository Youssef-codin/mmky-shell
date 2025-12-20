# 🐚 Basic Shell Implementation — MMKY Shell

**MMKY Shell (Marwan, Moataz, Kareem, Youssef)** is a complete, modular, and POSIX-inspired Unix-like shell implemented in Python.  
*It supports command execution, pipelines, I/O redirection, background jobs, environment variable expansion, and full signal handling.*

---

# 📖 Overview

This project is a fully functional **Unix-like shell**, built from scratch in Python as part of an advanced Operating Systems course. It recreates many behaviors of real shells like `bash`, including:

* Managing processes with `fork()`, `exec()`, and `wait()`
* Handling pipes, redirections, and background jobs
* Running internal shell built-ins (`cd`, `exit`, `pwd`, `echo`, etc.)
* Expanding variables and parsing quoted strings correctly
* Capturing system signals (`SIGINT`, `SIGCHLD`)

The shell is designed with **clear modular separation**, making it easy to understand, extend, and debug.

---

# ✨ Features

## 🚀 Command Execution & Processes

* Executes external commands using `os.fork()` + `os.execvp()`
* Supports **foreground** and **background** processes (`&`)
* Implements automatic **zombie reaping** using `SIGCHLD`
* Properly handles `stdin`/`stdout` duplication using `os.dup2()`

---

## 🔀 I/O Redirection

* **Input redirection:** `command < file`
* **Output redirection:** `command > file`
* Safely handles missing file errors & permission issues

---

## 🔗 Pipelines (`|`)

* Allows chaining multiple commands:

  ```bash
  ls -l | grep py
  ```
* Uses pipes + forked children for true parallel command execution

---

## 🛠️ Built-In Commands

Internal commands run **without creating new processes**, directly modifying shell state:

| Built-in  | Description                                                 |
| --------- | ----------------------------------------------------------- |
| `cd`      | Change directory (supports `cd -`, `$HOME`, relative paths) |
| `pwd`     | Print current working directory                             |
| `exit`    | Exit the shell with optional status code                    |
| `echo`    | Print text to output                                        |
| `history` | Show command history                                        |
| `help`    | Display available built-ins                                 |

---

## 🧠 Advanced Parser

`parser.py` handles:

* POSIX-compliant tokenization using `shlex`
* Environment variable expansion: `$USER`, `${HOME}`
* Correct handling of quotes (`"text"`, `'text'`)

---

## 🧵 Signal Handling

Implemented in `signals.py`:

* **SIGINT (Ctrl + C):** Prevents shell from exiting accidentally
* **SIGCHLD:** Cleans zombie processes created by background jobs

---

# 🧱 Architecture Overview

The project is divided into clean, logical modules:

| Component             | File(s)                         | Description                                        |
| --------------------- | ------------------------------- | -------------------------------------------------- |
| **Input Parsing**     | `parser.py`                     | Splits commands, expands variables, handles quotes |
| **Command Logic**     | `command_handler.py`, `main.py` | Detects pipes, redirections, background jobs       |
| **Execution Engine**  | `executor.py`, `signals.py`     | Creates child processes, manages pipes & signals   |
| **Built-in Commands** | `shell_builtins.py`             | Runs shell-native commands without forking         |

---

# 👥 Team Roles

Each team member contributed to a core subsystem:

| Member     | Role                                | Responsibilities                                          |
| ---------- | ----------------------------------- | --------------------------------------------------------- |
| **Moataz** | Execution & Process Lead            | `executor.py`, `signals.py` — forking, exec, job control  |
| **Marwan** | Parser & Input Specialist           | `parser.py` — variable expansion, quoting, parsing engine |
| **Yousef** | Pipeline & Redirection Handler      | `command_handler.py`, shell flow in `main.py`             |
| **Kareem** | User Features & Built-ins Developer | `shell_builtins.py`, new user-facing features             |

---

# 📂 How It Works (Technical Flow)

```graph TD;
    A[User Input] --> B[Parser]
    B --> C{Built-in?}
    C -- Yes --> D[Execute Built-in]
    C -- No --> E[Check for pipes, redirection, background]
    E --> F[Set up redirections and pipelines]
    F --> G[Executor]
    G --> H[Child process via fork()]
    H --> I[execvp()]
    G --> J[Parent (wait or return)]
```
<p align="center"> <img src="https://github.com/user-attachments/assets/0874157f-78b8-4685-bfdf-f2f512f643a9" width="800" alt="Shell Workflow Diagram"/> </p>

---

# 🧪 Example Usage

### 1️⃣ Basic Command

```bash
echo "Hello Shell"
```

### 2️⃣ Redirection

```bash
echo "Hi" > out.txt
cat out.txt
```

### 3️⃣ Pipeline

```bash
ls -l | grep .py
```

### 4️⃣ Background Process

```bash
sleep 5 &
```

### 5️⃣ Navigation

```bash
cd /usr/bin
pwd
```

---

# ▶️ Installation & Running

### Requirements

* Python 3.6+
* Linux / Unix-based OS (or WSL on Windows)

### Run the Shell

```bash
python3 main.py
```

---

# 🛠️ Possible Future Improvements

* Full job control (`fg`, `bg`, job listing)
* Command autocompletion using `readline`
* Arrow-key history navigation
* Persistent history saved to disk
* Support for `>>` (append redirection)

---

## 👥 Contributors

- **Marwan** — Parsing & variable expansion  
- **Moataz** — Process execution & signal handling  
- **Kareem** — Built-in commands & user features  
- **Youssef** — Pipelines, redirection & shell control flow

---

# 📜 License

This project is created for educational purposes under the **Operating Systems course**.


---

# 🙌 Final Notes

This project demonstrates deep understanding of OS internals and shell architecture. Each module is tested, structured, and ready for extension.
