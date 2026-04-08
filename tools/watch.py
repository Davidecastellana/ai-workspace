#!/usr/bin/env python3
"""
Cross-platform file watcher for ai-workspace.
Works on macOS, Linux, and Windows.
Watches context/ and pipelines/ — on any change, auto-commits and pushes to GitHub.

Usage:
    python3 tools/watch.py
"""

import subprocess
import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Root of the repo (parent of tools/)
REPO_ROOT = Path(__file__).parent.parent
WATCH_DIRS = ["context", "pipelines"]
DEBOUNCE_SECONDS = 2.0  # wait this long after last change before committing


class AutoPushHandler(FileSystemEventHandler):
    def __init__(self):
        self._pending = False
        self._last_event = 0

    def on_any_event(self, event):
        # Ignore directory events and hidden files
        if event.is_directory:
            return
        if "/.git/" in event.src_path or event.src_path.endswith(".DS_Store"):
            return

        self._pending = True
        self._last_event = time.time()
        print(f"  Change detected: {event.src_path}")

    def flush_if_pending(self):
        if not self._pending:
            return
        if time.time() - self._last_event < DEBOUNCE_SECONDS:
            return

        self._pending = False
        print("\nCommitting and pushing changes...")

        result = subprocess.run(
            ["git", "add", "."],
            cwd=REPO_ROOT
        )
        if result.returncode != 0:
            print("  ERROR: git add failed")
            return

        # Check if there's anything to commit
        status = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            cwd=REPO_ROOT
        )
        if status.returncode == 0:
            print("  No changes to commit.")
            return

        result = subprocess.run(
            ["git", "commit", "-m", "auto: content update"],
            cwd=REPO_ROOT
        )
        if result.returncode != 0:
            print("  ERROR: git commit failed")
            return

        result = subprocess.run(
            ["git", "push"],
            cwd=REPO_ROOT
        )
        if result.returncode != 0:
            print("  ERROR: git push failed")
            return

        print("  Pushed. Pipeline will trigger shortly.\n")


def main():
    handler = AutoPushHandler()
    observer = Observer()

    for watch_dir in WATCH_DIRS:
        path = REPO_ROOT / watch_dir
        path.mkdir(exist_ok=True)
        observer.schedule(handler, str(path), recursive=True)
        print(f"Watching: {path}")

    observer.start()
    print("\nAuto-push active. Save any file in context/ or pipelines/ to trigger pipeline.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            handler.flush_if_pending()
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
        print("\nWatcher stopped.")

    observer.join()


if __name__ == "__main__":
    main()
