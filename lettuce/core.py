import subprocess
import time
from lettuce.utils import load_yaml_config, expand_path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def run_sync(config_path):
    config = load_yaml_config(config_path)
    source = expand_path(config.get("source", "."))
    target = config.get("target")

    if not target:
        raise ValueError("Missing 'target' in config")

    rsync_cmd = [
        "rsync", "-avz", "--delete"
    ]

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
    subprocess.run(rsync_cmd, check=True)


class LettuceEventHandler(FileSystemEventHandler):
    def __init__(self, config_path):
        self.config_path = config_path

    def on_any_event(self, event):
        print("🔁 Change detected, syncing...")
        try:
            run_sync(self.config_path)
        except Exception as e:
            print("❌ Sync failed:", e)


def watch_sync(config_path):
    config = load_yaml_config(config_path)
    source = expand_path(config.get("source", "."))
    event_handler = LettuceEventHandler(config_path)
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
