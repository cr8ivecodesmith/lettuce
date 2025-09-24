# lettuce/core.py

import subprocess
import time
from lettuce.utils import load_yaml_config, expand_path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def run_sync(config_path, as_root=False):
    """
    Run rsync based on the provided configuration.

    :param config_path: Path to the YAML configuration file.
    :param as_root: Whether to run rsync with sudo.

    """
    config = load_yaml_config(config_path)
    source = expand_path(config.get("source", "."))
    target = config.get("target")

    if not target:
        raise ValueError("Missing 'target' in config")

    # Ensure target directory exists (optional sudo)
    if ":" in target:
        user_host, remote_path = target.split(":", 1)
        mkdir_cmd = f"{'sudo ' if as_root else ''}mkdir -p {remote_path}"
        try:
            subprocess.run(["ssh", user_host, mkdir_cmd], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create remote directory: {e}")
            return

    rsync_cmd = ["rsync", "-avz", "--delete"]
    if as_root:
        rsync_cmd.extend(["-e", "ssh", "--rsync-path=sudo rsync"])

    # Add ignore patterns
    for ignore in config.get("ignore", []):
        rsync_cmd.append(f"--exclude={ignore}")

    # Add allowlist (optional)
    if "allow" in config:
        for allow in config["allow"]:
            rsync_cmd.append(f"--include={allow}")
        rsync_cmd.append("--exclude=*")

    rsync_cmd.extend([source + "/", target])

    print("Running:", " ".join(rsync_cmd))
    try:
        subprocess.run(rsync_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ rsync failed: {e}")
        return


class LettuceEventHandler(FileSystemEventHandler):
    """
    Event handler for filesystem changes to trigger rsync.

    :param config_path: Path to the YAML configuration file.
    :param as_root: Whether to run rsync with sudo.

    """
    def __init__(self, config_path, as_root=False):
        self.config_path = config_path
        self.as_root = as_root

    def on_any_event(self, event):
        print("🔁 Change detected, syncing...")
        try:
            run_sync(self.config_path, self.as_root)
        except Exception as e:
            print("❌ Sync failed:", e)


def watch_sync(config_path, as_root=False):
    """
    Watch the source directory for changes and sync on any event.

    :param config_path: Path to the YAML configuration file.
    :param as_root: Whether to run rsync with sudo.

    """
    config = load_yaml_config(config_path)
    source = expand_path(config.get("source", "."))
    event_handler = LettuceEventHandler(config_path, as_root)
    observer = Observer()
    observer.schedule(event_handler, source, recursive=True)
    print(f"👀 Watching '{source}' for changes...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Stopping watcher...")
        observer.stop()
    observer.join()
