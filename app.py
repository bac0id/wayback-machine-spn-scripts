from flask import Flask, render_template, request
import subprocess
import time
import os
import shlex
from urllib.parse import urlparse

from nohup_shell_api import NohupShellAPI
from spn_shell_api import SpnShellAPI

app = Flask(__name__)
spn_logs_directory = "./spn_logs/"

def get_new_spn_log_filename(url):
    time_str = time.strftime("%Y%m%d_%H%M%S")
    if url.startswith("http"):
        parsed_url = urlparse(url)
        output_filename = f"{time_str}_{parsed_url.hostname}.out"
        print(url, output_filename)
    else:
        output_filename = f"{time_str}_.out"
        print(url, output_filename)
    return output_filename

def ensure_spn_log_directory_exists():
    """
    Ensures that the SPN log directory exists. Creates it if it doesn't.
    """
    os.makedirs(spn_logs_directory, exist_ok=True)


@app.route('/start', methods=['GET', 'POST'])
def page_start_spn():
    nohup_spn_command = []
    output = None
    if request.method == 'POST':
        url = request.form.get('url', '')
        auth = request.form.get('auth', '')
        curl_args = request.form.get('curl_args', '')
        data = request.form.get('data', '')
        folder = request.form.get('folder', '')
        suffix = request.form.get('suffix', '')
        no_errors = 'no_errors' in request.form
        outlinks_pattern = request.form.get('outlinks_pattern', '')
        parallel_jobs = request.form.get('parallel_jobs', '')
        discard_json = 'discard_json' in request.form
        resume_folder = request.form.get('resume_folder', '')
        use_https = 'use_https' in request.form
        update_wait = request.form.get('update_wait', '')
        capture_wait = request.form.get('capture_wait', '')
        exclude_pattern = request.form.get('exclude_pattern', '')

        spn_command = SpnShellAPI().build_command(url, auth=auth, curl_args=curl_args, data=data, folder=folder,
            suffix=suffix, no_errors=no_errors, outlinks_pattern=outlinks_pattern,
            parallel_jobs=parallel_jobs, discard_json=discard_json, resume_folder=resume_folder,
            use_https=use_https, update_wait=update_wait, capture_wait=capture_wait,
            exclude_pattern=exclude_pattern)

        spn_command_log_filename = get_new_spn_log_filename(url)
        spn_command_log_filename = spn_logs_directory + spn_command_log_filename
        nohup_spn_command = NohupShellAPI().build_command(spn_command, log_filename=spn_command_log_filename)
        nohup_spn_command = " ".join(nohup_spn_command)

        ensure_spn_log_directory_exists()
        try:
            output = subprocess.check_call(nohup_spn_command, shell=True)
        except Exception as e:
            output = f"Error: {e}"

    return render_template('start_spn.html', command=nohup_spn_command, output=output)

def get_existing_log_filename(directory):
    log_filenames = []
    try:
        for filename in os.listdir(directory):
            if filename.endswith(".out"):
                log_filenames.append(filename)
    except FileNotFoundError:
        # Handle the case where the log directory doesn't exist
        print(f"Error: Log directory '{directory}' not found.")

    log_filenames.sort()
    return log_filenames

@app.route('/log/<filename>')
def page_log_content(filename):
    full_filename = spn_logs_directory + filename
    try:
        with open(full_filename, 'r') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"Error: Log file '{log_dir}' not found.")
        return "Log file not found.", 404 # Return a 404 error
    return render_template('log_content.html', filename=filename, file_content=file_content)

@app.route('/log')
def page_logs_list():
    log_filenames = get_existing_log_filename(spn_logs_directory)
    return render_template('log_list.html', log_filenames=log_filenames)

@app.route('/about')
def page_about():
    return render_template('about.html')

@app.route('/')
def page_index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
