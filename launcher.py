"""
Launcher script for ATE Operator Helper
This script starts the Streamlit app and opens it in the default browser
"""

import os
import sys
import subprocess
import time
import webbrowser
import socket
from threading import Thread

# You can update this path if Streamlit is installed elsewhere
STREAMLIT_PATH = r"C:\Users\Admin\AppData\Roaming\Python\Python39\Scripts"
STREAMLIT_EXE = os.path.join(STREAMLIT_PATH, "streamlit.exe")

def find_free_port():
    """Find an open port on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def read_output(pipe, name):
    """Read output from a subprocess pipe and print it"""
    try:
        for line in iter(pipe.readline, ''):
            if not line:
                break
            print(f"[{name}] {line.strip()}")
    finally:
        pipe.close()

def start_streamlit(port):
    """Start the Streamlit server"""
    if not os.path.isfile(STREAMLIT_EXE):
        print(f"Error: Streamlit executable not found at {STREAMLIT_EXE}")
        sys.exit(1)

    # Add Streamlit folder to PATH for subprocess
    os.environ["PATH"] += os.pathsep + STREAMLIT_PATH

    # Determine app.py path
    if getattr(sys, 'frozen', False):
        # When frozen by PyInstaller, app.py should be extracted to _MEIPASS
        app_path = os.path.join(sys._MEIPASS, "app.py")
    else:
        # Running normally: expect app.py in the same folder as launcher.py
        launcher_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(launcher_dir, "app.py")

    if not os.path.isfile(app_path):
        print(f"Error: app.py not found at {app_path}")
        sys.exit(1)

    cmd = [
        STREAMLIT_EXE,
        "run",
        app_path,
        "--server.port", str(port),
        "--server.headless", "true",
        "--browser.serverAddress", "localhost",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Start threads to read stdout and stderr asynchronously
    Thread(target=read_output, args=(process.stdout, "STDOUT"), daemon=True).start()
    Thread(target=read_output, args=(process.stderr, "STDERR"), daemon=True).start()

    return process

def main():
    print("Starting ATE Operator Helper...")

    port = find_free_port()
    streamlit_process = start_streamlit(port)

    time.sleep(3)  # Wait a bit for Streamlit to start

    url = f"http://localhost:{port}"
    print(f"Opening browser at {url}")
    webbrowser.open(url)

    try:
        while True:
            time.sleep(1)
            # Check if Streamlit process exited unexpectedly
            if streamlit_process.poll() is not None:
                print("Streamlit process ended unexpectedly.")
                break
    except KeyboardInterrupt:
        print("Shutting down...")
        if streamlit_process.poll() is None:
            streamlit_process.terminate()
            streamlit_process.wait()
        sys.exit(0)

if __name__ == "__main__":
    main()
