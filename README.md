# Shell Built-in Commands Module

## 📋 Overview

This module implements built-in shell commands for a custom Unix-like shell. Built-in commands are executed directly by the shell without forking a new process, making them faster and allowing them to modify the shell's internal state.

## 👥 Team Role: User Features & Built-ins Developer (Person 4)

**Responsibilities:**
- Implementing internal shell commands (cd, exit, pwd, echo, etc.)
- Managing shell environment variables
- Providing user-friendly command interfaces
- Error handling for built-in operations

## 🚀 Features

### Implemented Built-in Commands

| Command | Description | Usage Examples |
|---------|-------------|----------------|
| `cd` | Change directory | `cd`, `cd /path`, `cd -`, `cd ~` |
| `pwd` | Print working directory | `pwd`, `pwd -P` |
| `echo` | Display text | `echo Hello`, `echo -n text`, `echo $VAR` |
| `exit` | Exit the shell | `exit`, `exit 0` |
| `export` | Set environment variables | `export VAR=value` |
| `unset` | Remove environment variables | `unset VAR` |
| `env` | Display all environment variables | `env` |
| `help` | Show help information | `help`, `help cd` |
| `type` | Show command type | `type cd`, `type ls` |
| `history` | Command history (placeholder) | `history` |

## 📦 Installation & Integration

### File Structure
```
project/
├── builtins.py          # This module (Person 4)
├── parser.py            # Command parsing (Person 2)
├── executor.py          # Command execution (Person 1)
├── command_handler.py   # I/O & pipes (Person 3)
└── main.py             # Main shell loop (Person 3)
```

### Integration Example

```python
from builtins import handle_builtin_commands

# In your main shell loop:
while True:
    user_input = input("$ ")
    parsed_command = parse(user_input)  # Person 2's parser
    
    # Check if it's a built-in command
    if handle_builtin_commands(parsed_command):
        continue  # Built-in was handled, skip external execution
    
    # Otherwise, execute as external command
    execute_external(parsed_command)  # Person 1's executor
```

## 💻 Usage Guide

### Basic Commands

#### Change Directory (`cd`)
```bash
$ cd /home/user/documents    # Go to specific directory
$ cd                         # Go to home directory
$ cd ~                       # Go to home directory
$ cd ..                      # Go to parent directory
$ cd -                       # Go to previous directory
```

#### Print Working Directory (`pwd`)
```bash
$ pwd                        # Show current directory
$ pwd -P                     # Show physical path (resolve symlinks)
```

#### Echo Text (`echo`)
```bash
$ echo Hello World           # Print text
$ echo -n "No newline"       # Print without newline
$ echo $HOME                 # Print environment variable
$ echo "User: $USER"         # Expand variables in text
```

#### Environment Variables
```bash
$ export PATH=/usr/bin       # Set environment variable
$ export MY_VAR=hello        # Create new variable
$ env                        # Show all variables
$ unset MY_VAR               # Remove variable
```

#### Get Help
```bash
$ help                       # Show all built-in commands
$ help cd                    # Show help for specific command
$ type cd                    # Check if command is built-in
$ type ls                    # Check if command is external
```

#### Exit Shell
```bash
$ exit                       # Exit with status 0
$ exit 1                     # Exit with custom status code
```

## 🏗️ Architecture

### Class Design

```python
class ShellBuiltins:
    """Main class handling all built-in commands"""
    
    def __init__(self):
        self.previous_dir = None      # For 'cd -' functionality
        self.shell_vars = {}           # Shell variables storage
    
    def handle_builtin_commands(command):
        """Main entry point - routes commands to handlers"""
        # Returns True if handled, False if external command
```

### Command Flow

```
User Input → Parser (P2) → Built-in Check (P4)
                              ↓
                         Is Built-in?
                         ↙          ↘
                      YES            NO
                       ↓              ↓
                 Execute Here    Return False
                   (P4)          (P1 handles)
                       ↓
                  Return True
```

## 🔧 Advanced Features

### Environment Variable Expansion
The `echo` command supports variable expansion:
```bash
$ export NAME="Alice"
$ echo Hello $NAME           # Output: Hello Alice
$ echo Path: ${PATH}         # Output: Path: /usr/bin:/bin:...
```

### Directory Navigation History
The `cd -` command remembers your previous directory:
```bash
$ pwd                        # /home/user
$ cd /tmp
$ pwd                        # /tmp
$ cd -                       # Returns to /home/user
/home/user
```

### Error Handling
All commands include comprehensive error handling:
```bash
$ cd /nonexistent
cd: /nonexistent: No such file or directory

$ exit abc
exit: abc: numeric argument required

$ unset
unset: not enough arguments
```

## 🧪 Testing

### Test the Module Directly
```bash
python3 builtins.py
```

### Unit Testing Example
```python
from builtins import ShellBuiltins

def test_cd_command():
    handler = ShellBuiltins()
    handler.cmd_cd(['cd', '/tmp'])
    assert os.getcwd() == '/tmp'

def test_echo_with_variable():
    handler = ShellBuiltins()
    os.environ['TEST'] = 'value'
    # Test echo $TEST
    handler.cmd_echo(['echo', '$TEST'])
```

## 🔄 Integration with Other Modules

### With Parser (Person 2)
```python
# Parser provides structured command
parsed = parse_input("cd /home")
# Returns: ['cd', '/home']

# Builtins processes it
handle_builtin_commands(parsed)
```

### With Executor (Person 1)
```python
# Only called if NOT a built-in
if not handle_builtin_commands(command):
    executor.execute_external(command)  # Person 1's code
```

### With Command Handler (Person 3)
```python
# Built-ins don't need pipes/redirection setup
if handle_builtin_commands(command):
    continue  # Skip pipe/redirection logic

# Setup pipes only for external commands
setup_pipes(command)
```

## 📚 API Reference

### Main Function

#### `handle_builtin_commands(command)`
**Parameters:**
- `command` (list): Command and arguments as list of strings
  - Example: `['cd', '/home']`, `['echo', 'hello']`

**Returns:**
- `True`: Command was a built-in and was handled
- `False`: Command is external, needs execution by Person 1

**Example:**
```python
if handle_builtin_commands(['cd', '/tmp']):
    print("Built-in executed")
else:
    print("External command")
```

## 🐛 Known Limitations

1. **History Command**: Currently a placeholder - needs integration with main shell loop for full implementation
2. **Job Control**: Not implemented in built-ins (handled by Person 1)
3. **Aliases**: Not yet supported
4. **Advanced Globbing**: Variable expansion is basic (no wildcards in echo)

## 🤝 Contributing

This module is part of a team project. Integration points:

- **Person 1 (Moataz):** Use the return value to decide whether to fork/exec
- **Person 2 (Marwan):** Ensure commands are returned as lists
- **Person 3 (Youssef):** Skip pipe setup for built-in commands
- **Person 4 (Kareem):** Extend this module with additional built-ins

## 📄 License

This is an educational project for Operating Systems coursework.

## 👨‍💻 Author

**Person 4 - Kareem Diaa** - User Features & Built-ins Developer

---

## Quick Reference Card

```
╔════════════════════════════════════════════════╗
║          BUILT-IN COMMANDS REFERENCE           ║
╠════════════════════════════════════════════════╣
║ cd [dir]      │ Change directory               ║
║ pwd [-P]      │ Print working directory        ║
║ echo [args]   │ Display text                   ║
║ exit [n]      │ Exit shell (status n)          ║
║ export VAR=x  │ Set environment variable       ║
║ unset VAR     │ Remove environment variable    ║
║ env           │ Show all environment vars      ║
║ help [cmd]    │ Show help information          ║
║ type cmd      │ Show command type              ║
║ history       │ Show command history           ║
╚════════════════════════════════════════════════╝
```

## 📞 Support

For issues or questions:
1. Check the `help` command: `help [command]`
2. Review error messages - they're descriptive
3. Consult team members for integration issues

---

**Project:** Basic Shell Implementation  
**Course:** Operating Systems  
**Module:** Built-in Commands (builtins.py)
