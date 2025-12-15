import unittest
import subprocess
import os
import sys

class TestShellIntegration(unittest.TestCase):
    # Path to the shell script we are testing
    SHELL_SCRIPT = os.path.join(os.getcwd(), "main_simplified.py")

    def run_shell(self, input_str):
        """Helper to run the shell with specific input."""
        process = subprocess.Popen(
            [sys.executable, self.SHELL_SCRIPT],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd() 
        )
        stdout, stderr = process.communicate(input=input_str)
        return stdout, stderr

    def test_pwd(self):
        """Test that 'pwd' returns the current working directory."""
        stdout, stderr = self.run_shell("pwd\nexit\n")
        self.assertIn(os.getcwd(), stdout)

    def test_builtin_redirection(self):
        """Test executing a builtin (echo) with output redirection."""
        test_file = "test_builtin_redir.txt"
        if os.path.exists(test_file):
            os.remove(test_file)
        
        try:
            # Input: echo 'hello world' > test_builtin_redir.txt
            self.run_shell(f"echo 'hello world' > {test_file}\nexit\n")
            
            self.assertTrue(os.path.exists(test_file), "Output file was not created by builtin redirection")
            with open(test_file, 'r') as f:
                content = f.read().strip()
            self.assertEqual(content, "hello world")
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_external_redirection(self):
        """Test executing an external command (ls) with output redirection."""
        test_file = "test_external_redir.txt"
        if os.path.exists(test_file):
            os.remove(test_file)
            
        try:
            # Input: ls > test_external_redir.txt
            self.run_shell(f"ls > {test_file}\nexit\n")
            
            self.assertTrue(os.path.exists(test_file), "Output file was not created by external redirection")
            with open(test_file, 'r') as f:
                content = f.read()
            # The output of ls should contain the script itself
            self.assertIn("main_simplified.py", content)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_pipeline_basic(self):
        """Test a simple pipeline: echo 'pipeline' | cat"""
        # Note: This shell's pipeline implementation might print output cleanly or with prompts mixed in.
        # We just check if the text appears in the final output.
        stdout, stderr = self.run_shell("echo 'pipeline test' | cat\nexit\n")
        self.assertIn("pipeline test", stdout)

if __name__ == '__main__':
    unittest.main()
