import subprocess
import shlex

class NohupShellAPI:
    
    def start(self, command, log_filename):
        """
        Starts the given command with nohup, redirecting output to a log file.

        Args:
            command: A list of strings representing the command (e.g., the output of shlex.split).
            log_filename: The name of the log file.

        Returns:
            The return code of the command.
        """

        # Build the nohup command
        nohup_command = self.build_command(command, log_filename)

        # Run the command and capture the return code
        try:
            return subprocess.check_call(nohup_command)
        except subprocess.CalledProcessError as e:
            raise

    def build_command(self, command, log_filename):
        """
        Generates a command string to execute the given command with nohup,
        redirecting output to a log file.

        Args:
            command: A list of strings representing the command (e.g., the output of shlex.split).
            log_filename: The name of the log file.

        Returns:
            A string representing the nohup command.
        """

        # Ensure command is a list
        if not isinstance(command, list):
            raise TypeError("Command must be a list.")

        # Escape special characters in command arguments for shell safety
        escaped_command = [shlex.quote(arg) for arg in command]

        # Construct the nohup command
        nohup_command = ["nohup"] + escaped_command + [f"1>>{log_filename}", "2>&1", "&"]
        return nohup_command
