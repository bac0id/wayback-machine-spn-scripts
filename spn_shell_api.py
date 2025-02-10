import subprocess
import shlex

class SpnShellAPI:
    """API class to call spn.sh script with various options.

    This class provides a safe and convenient way to call the spn.sh script
    with different parameters from a Python application.
    """

    def __init__(self):
        self.base_command = "bash spn.sh"

    def start(self, url, *, auth=None, curl_args=None, data=None, folder=None,
            suffix=None, no_errors=False, outlinks_pattern=None,
            parallel_jobs=None, discard_json=False, resume_folder=None,
            use_https=False, update_wait=None, capture_wait=None,
            exclude_pattern=None):
        """Runs spn.sh script with specified parameters.

        Args:
            url (str): Required. The URL to capture.
            auth (str, optional): S3 API keys in the format 'accesskey:secret'.
            curl_args (str, optional): Additional arguments to pass to curl.
            data (str, optional): Capture request options or other POST data.
            folder (str, optional): Custom location for the data folder.
            suffix (str, optional): Suffix to add to the data folder name.
            no_errors (bool, optional): Don't save errors to the Wayback Machine.
            outlinks_pattern (str, optional): Regex pattern to match capture outlinks.
            parallel_jobs (int, optional): Maximum number of capture jobs to run in parallel.
            discard_json (bool, optional): Discard JSON for completed jobs.
            resume_folder (str, optional): Resume with URLs from an aborted session.
            use_https (bool, optional): Use HTTPS for all captures and change HTTP URLs to HTTPS.
            update_wait (int, optional): Minimum wait time before updating the main URL list.
            capture_wait (float, optional): Minimum wait time before starting another capture job.
            exclude_pattern (str, optional): Regex pattern to exclude capture outlinks.

        Returns:
            int: The return code of the spn.sh script (0 for success).

        Raises:
            subprocess.CalledProcessError: If the script execution fails.
        """
        command = self.build_command(url, auth=auth, curl_args=curl_args, data=data, folder=folder,
            suffix=suffix, no_errors=no_errors, outlinks_pattern=outlinks_pattern,
            parallel_jobs=parallel_jobs, discard_json=discard_json, resume_folder=resume_folder,
            use_https=use_https, update_wait=update_wait, capture_wait=capture_wait,
            exclude_pattern=exclude_pattern)

        # Run the command and capture the return code
        try:
            return subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            raise
    
    def build_command(self, url, *, auth=None, curl_args=None, data=None, folder=None,
            suffix=None, no_errors=False, outlinks_pattern=None,
            parallel_jobs=None, discard_json=False, resume_folder=None,
            use_https=False, update_wait=None, capture_wait=None,
            exclude_pattern=None):

        # Build the command string with arguments
        command = shlex.split(self.base_command)  # Split safely
        if auth:
            command.append("-a")
            command.append(auth)
        if curl_args:
            command.append("-c")
            command.append(curl_args)
        if data:
            command.append("-d")
            command.append(data)
        if folder:
            command.append("-f")
            command.append(folder)
        if suffix:
            command.append("-i")
            command.append(suffix)
        if no_errors:
            command.append("-n")
        if outlinks_pattern:
            command.append("-o")
            command.append(outlinks_pattern)
        if parallel_jobs:
            command.append("-p")
            command.append(str(parallel_jobs))
        if discard_json:
            command.append("-q")
        if resume_folder:
            command.append("-r")
            command.append(resume_folder)
        if use_https:
            command.append("-s")
        if update_wait:
            command.append("-t")
            command.append(str(update_wait))
        if capture_wait:
            command.append("-w")
            command.append(str(capture_wait))
        if exclude_pattern:
            command.append("-x")
            command.append(exclude_pattern)
        command.append(url)  # Required URL at the end

        return command
