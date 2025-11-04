#!/usr/bin/env python3
"""
spookyappx.py - simple cross-platform test app

Usage:
  python spookyappx.py        # GUI mode if available (Tkinter)
  python spookyappx.py --headless   # prints to terminal instead of GUI
  python spookyappx.py --log-only   # write log entry and exit

What it does:
 - Writes a timestamped entry to a log file in the user's home directory.
 - If not headless, opens a small Tk window with "SpookyAppX running" and a Quit button.
"""

import sys
import os
import time
from datetime import datetime

LOGFILE_NAME = "spookyappx.log"

def get_log_path():
    home = os.path.expanduser("~")
    return os.path.join(home, LOGFILE_NAME)

def write_log(entry):
    path = get_log_path()
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()} UTC\t{entry}\n")
        return True, path
    except Exception as e:
        return False, str(e)

def run_headless():
    ok, info = write_log("spookyappx started (headless)")
    if ok:
        print("SpookyAppX (headless) ran. Log written to:", info)
    else:
        print("Failed to write log:", info)
    # Print some friendly info for quick checks
    print("Python:", sys.executable)
    print("Platform:", sys.platform)
    print("Exiting.")
    return 0

def run_log_only():
    ok, info = write_log("spookyappx log-only run")
    if ok:
        print("Log entry written to:", info)
        return 0
    else:
        print("Failed to write log:", info)
        return 2

def run_gui():
    # Try to import Tkinter; if not available, fall back to headless
    try:
        if sys.version_info[0] >= 3:
            import tkinter as tk
            from tkinter import messagebox
        else:
            import Tkinter as tk
            from Tkinter import messagebox
    except Exception as e:
        print("Tkinter not available, falling back to headless. Error:", e)
        return run_headless()

    ok, info = write_log("spookyappx started (gui)")
    if ok:
        print("GUI started; log:", info)
    else:
        print("GUI start: failed to write log:", info)

    root = tk.Tk()
    root.title("SpookyAppX")
    root.geometry("360x120")
    # Make the window always-on-top briefly so visible in tests
    try:
        root.attributes("-topmost", True)
        root.after(1000, lambda: root.attributes("-topmost", False))
    except:
        pass

    label = tk.Label(root, text="SpookyAppX running", font=("Segoe UI", 14))
    label.pack(pady=(18,6))

    info_label = tk.Label(root, text=f"Log: {get_log_path()}", font=("Segoe UI", 8))
    info_label.pack(pady=(0,8))

    def on_quit():
        ok, _ = write_log("spookyappx stopped (gui)")
        root.destroy()

    btn = tk.Button(root, text="Quit", command=on_quit, width=12)
    btn.pack(pady=(0,12))

    # Safe mainloop with exception catch
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_quit()
    return 0

def main(argv):
    headless = False
    logonly = False
    if "--headless" in argv:
        headless = True
    if "--log-only" in argv:
        logonly = True

    if logonly:
        return run_log_only()

    if headless:
        return run_headless()

    # Default: attempt GUI, fallback to headless
    return run_gui()

if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print("Unhandled error:", exc)
        write_log(f"spookyappx crashed: {exc}")
        sys.exit(1)
