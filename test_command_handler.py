import unittest
from command_handler import handle_redirection, handle_pipe, handle_background_process


class TestCommandHandler(unittest.TestCase):

    def test_handle_redirection(self):
        """
        Tests that the redirection handler correctly extracts the output file
        and removes the redirection symbols from the command.
        """
        command = ["echo", "hello", ">", "output.txt"]
        # The function SHOULD remove the '>' and 'output.txt' from the command
        # and return 'output.txt' as the stdout redirect file.
        result_command, stdin_redirect, stdout_redirect = handle_redirection(
            command)

        # Expected Input: ["echo", "hello", ">", "output.txt"]
        # Expected Output: (["echo", "hello"], None, "output.txt")
        self.assertEqual(result_command, ["echo", "hello"])
        self.assertIsNone(stdin_redirect)
        self.assertEqual(stdout_redirect, "output.txt")

    def test_handle_redirection_input(self):
        """
        Tests that the redirection handler correctly extracts the input file
        and removes the redirection symbols from the command.
        """
        command = ["sort", "<", "input.txt"]
        # The function SHOULD remove the '<' and 'input.txt' from the command
        # and return 'input.txt' as the stdin redirect file.
        result_command, stdin_redirect, stdout_redirect = handle_redirection(
            command)

        # Expected Input: ["sort", "<", "input.txt"]
        # Expected Output: (["sort"], "input.txt", None)
        self.assertEqual(result_command, ["sort"])
        self.assertEqual(stdin_redirect, "input.txt")
        self.assertIsNone(stdout_redirect)

    def test_handle_pipe_with_pipe(self):
        """
        Tests the pipe handler splits the command correctly.
        """
        command = ["ls", "-l", "|", "grep", "test"]
        # The handler should split the command into two lists.
        lhs, rhs = handle_pipe(command)

        # Expected Input: ["ls", "-l", "|", "grep", "test"]
        # Expected Output: (['ls', '-l'], ['grep', 'test'])
        self.assertEqual(lhs, ["ls", "-l"])
        self.assertEqual(rhs, ["grep", "test"])

    def test_handle_pipe_no_pipe(self):
        """
        Tests the pipe handler returns None for the rhs when no pipe exists.
        """
        command = ["ls", "-l"]
        # The handler should return the original command
        # and None for the right-hand side.
        lhs, rhs = handle_pipe(command)

        # Expected Input: ["ls", "-l"]
        # Expected Output: (['ls', '-l'], None)
        self.assertEqual(lhs, command)
        self.assertIsNone(rhs)

    def test_handle_background_process_with_ampersand(self):
        """
        Tests the background process handler with an ampersand.
        """
        command = ["sleep", "5", "&"]
        # The handler should remove the '&' and return True.
        result_command, background = handle_background_process(command)

        # Input: ["sleep", "5", "&"]
        # Output: (["sleep", "5"], True)
        self.assertEqual(result_command, ["sleep", "5"])
        self.assertTrue(background)

    def test_handle_background_process_no_ampersand(self):
        """
        Tests the background process handler without an ampersand.
        """
        command = ["ls", "-l"]
        # The handler should not modify the command and return False.
        result_command, background = handle_background_process(command)

        # Input: ["ls", "-l"]
        # Output: (["ls", "-l"], False)
        self.assertEqual(result_command, command)
        self.assertFalse(background)


    def test_handle_pipe_with_multiple_pipes(self):
        """
        Tests the pipe handler with multiple pipes present, assuming it only splits at the first.
        """
        command = ["ls", "-l", "|", "grep", "test", "|", "wc", "-l"]
        # The handler should split the command at the first pipe.
        lhs, rhs = handle_pipe(command)

        # Expected Input: ["ls", "-l", "|", "grep", "test", "|", "wc", "-l"]
        # Expected Output: (["ls", "-l"], ["grep", "test", "|", "wc", "-l"])
        self.assertEqual(lhs, ["ls", "-l"])
        self.assertEqual(rhs, ["grep", "test", "|", "wc", "-l"])

if __name__ == '__main__':
    unittest.main()