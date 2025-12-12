# parser.py
import shlex
import os
import re

def expand_variables(input_str):
    pattern = r'\$\{([A-Za-z0-9_]+)\}|\$([A-Za-z0-9_]+)'
    def replace_match(match):
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, '')
    return re.sub(pattern, replace_match, input_str)

def parse_input(input_str):
    expanded_str = expand_variables(input_str)
    try:
        # posix=True ensures proper handling of quotes
        return shlex.split(expanded_str, posix=True)
    except ValueError as e:
        print(f"Error parsing input: {e}")
        return []
