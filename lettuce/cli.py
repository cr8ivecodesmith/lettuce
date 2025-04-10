import argparse
from lettuce.core import run_sync, watch_sync


def main():
    parser = argparse.ArgumentParser(
        description="🥬 Lettuce: simple YAML-powered rsync wrapper")
    parser.add_argument(
        "command", choices=["sync", "watch"], help="Command to run")
    parser.add_argument(
        "--config", default="lettuce.yml", help="Path to lettuce YAML config")
    parser.add_argument(
        "--as-root", action="store_true",
        help="Create target directory as root if it does not exist")
    args = parser.parse_args()

    if args.command == "sync":
        run_sync(args.config, as_root=args.as_root)
    elif args.command == "watch":
        watch_sync(args.config, as_root=args.as_root)
