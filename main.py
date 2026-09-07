import sys
import time
import webbrowser
import subprocess
from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    python_exe = sys.executable

    editor_script = base_dir / "editor.py"
    server_script = base_dir / "website_details" / "server_loader.py"

    print("Starting server_loader.py in a detached process...")
    # CREATE_NEW_CONSOLE opens server in its own clean window on Windows,
    # preventing main process stream-locking completely.
    server_process = subprocess.Popen(
        [python_exe, str(server_script)],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    print("Starting editor.py...")
    editor_process = subprocess.Popen([python_exe, str(editor_script)])

    time.sleep(1.5)
    webbrowser.open("http://localhost:5500")

    try:
        server_process.wait()
        editor_process.wait()
    except KeyboardInterrupt:
        print("\nStopping processes...")
        server_process.terminate()
        editor_process.terminate()

if __name__ == "__main__":
    main()