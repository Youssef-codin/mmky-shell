def parse_input(input_str):
    """
    Parses the raw input string from the user into a list of tokens.

    Args:
        input_str: The raw string from the user.

    Returns:
        A list of strings, representing the command and its arguments.
        For example, "ls -l /tmp" becomes ["ls", "-l", "/tmp"].
    """
    # This is a simple parser. It will be replaced by a more robust one.
    return input_str.strip().split()
