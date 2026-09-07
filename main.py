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
    log_file = base_dir / "server.log"

    print("Starting server_loader.py (logging to server.log)...")

    with open(log_file, "a", encoding="utf-8") as f:
        server_process = subprocess.Popen(
            [python_exe, str(server_script)],
            stdout=f,
            stderr=f
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
        print("Done.")

if __name__ == "__main__":
    main()