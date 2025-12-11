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
        (result_command, stdin_redirect, stdout_redirect) = handle_redirection(
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
        This test serves as a reminder that the current handle_pipe implementation
        is invalid for a real shell, as it leaves a pipe symbol in the result.
        """
        command = ["ls", "-l", "|", "grep", "test", "|", "wc", "-l"]
        lhs, rhs = handle_pipe(command)

        # The 'rhs' is [['grep', 'test', '|', 'wc', '-l']]. This is not a valid
        # single command for our executor. This assertion is designed to fail.
        try:
            self.assertNotIn('|', rhs)
        except AssertionError:
            print(("\n\nSUCCESS (Test Failed as Expected): `handle_pipe` is not"
                   " equipped to handle multiple pipes for the executor."
                   "\nThe right-hand-side command should not contain a pipe, but it does.\n"))
            raise


if __name__ == '__main__':
    # Discover all test methods in the TestCommandHandler class
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCommandHandler)
    test_cases = [test.id().split('.')[-1] for test in suite]

    while True:
        print("\nAvailable tests:")
        for i, test_name in enumerate(test_cases, 1):
            print(f"  {i}. {test_name}")
        print("  all. Run all tests")
        print("  exit. Exit the test runner")

        choice = input(
            "\nEnter the number of the test to run, 'all', or 'exit': ").strip().lower()

        if choice == 'exit':
            break

        runner = unittest.TextTestRunner()
        suite_to_run = unittest.TestSuite()

        if choice == 'all':
            suite_to_run = loader.loadTestsFromTestCase(TestCommandHandler)
        elif choice.isdigit() and 1 <= int(choice) <= len(test_cases):
            test_name_to_run = test_cases[int(choice) - 1]
            suite_to_run.addTest(TestCommandHandler(test_name_to_run))
        else:
            print(
                "\n[Invalid choice. Please enter a valid number, 'all', or 'exit'.]")
            continue

        print(f"\n--- Running {'all tests' if choice ==
              'all' else test_name_to_run} ---")
        runner.run(suite_to_run)
        print("--- Test run finished ---")
