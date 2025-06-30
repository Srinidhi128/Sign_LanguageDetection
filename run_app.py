import subprocess
import webbrowser
import os
import time
import sys
from threading import Thread

def run_flask_app(app_path, cwd):
    """Run a Flask application in a subprocess"""
    python_executable = sys.executable  # Get the current Python executable path
    subprocess.Popen([python_executable, app_path], cwd=cwd)

def main():
    # Get the root directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Start the main words recognition server
    print("Starting Words Recognition Server...")
    run_flask_app('app.py', root_dir)
    
    # Start the alphabets and numbers recognition server
    print("Starting Alphabets & Numbers Recognition Server...")
    alphanumeric_dir = os.path.join(root_dir, 'alphabets-and-numbers')
    run_flask_app('app.py', alphanumeric_dir)
    
    # Wait for servers to start
    print("Waiting for servers to start...")
    time.sleep(3)
    
    # Open the web application
    print("Opening web application...")
    web_path = os.path.join(root_dir, 'new3.html')
    webbrowser.open('file://' + web_path)
    
    print("\nApplication is running!")
    print("- Words Recognition Server: http://localhost:5000")
    print("- Alphabets & Numbers Server: http://localhost:5001")
    print("\nPress Ctrl+C to stop the servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)

if __name__ == '__main__':
    main()
