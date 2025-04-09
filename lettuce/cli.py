import argparse
from lettuce.core import run_sync, watch_sync


def main():
    parser = argparse.ArgumentParser(description="🥬 Lettuce: simple YAML-powered rsync wrapper")
    parser.add_argument("command", choices=["sync", "watch"], help="Command to run")
    parser.add_argument("--config", default="lettuce.yml", help="Path to lettuce YAML config")
    args = parser.parse_args()

    if args.command == "sync":
        run_sync(args.config)
    elif args.command == "watch":
        watch_sync(args.config)
