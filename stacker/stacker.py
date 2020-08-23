#!/usr/bin/python3

import argparse
from .stack import *


def main():
    parser = argparse.ArgumentParser(
        description="Docker stack management cli tool.")
    parser.add_argument("subcommand", type=str,
                        help="Valid subcommands: up, down, restart, ls, stop, start, logs")
    parser.add_argument(
        "arg1", type=str, help="Subcommand argument (optional)", nargs="?")
    parser.add_argument("-f", "--file", type=str,
                        help="file name or path of the main stack.json5 file.")
    parser.add_argument("-d", "--detach", action='store_true',
                        help="Runs in detached mode - similar to docker-compose up -d. ")
    args = parser.parse_args()

    file_path = args.file or "stack.json5"
    stack = create_stack_from_file(file_path, None)

    if args.subcommand == "up":
        start_stack(stack, detach=args.detach)
    elif args.subcommand == "down":
        stop_stack(stack)
    elif args.subcommand == "restart" and not args.arg1:
        restart_stack(stack)
    elif args.subcommand == "ls":
        print("List of stack containers: ")
        print(str(list_containers(stack)))
    elif args.subcommand == "stop" and args.arg1:
        stop_container(args.arg1)
    elif args.subcommand == "start" and args.arg1:
        start_container(args.arg1)
    elif args.subcommand == "restart" and args.arg1:
        restart_container(args.arg1)
    elif args.subcommand == "logs" and not args.arg1:
        for line in get_logs(stack).split("\n"):
            print(line)
    elif args.subcommand == "logs" and args.arg1:
        for line in get_container_logs(args.arg1).split("\n"):
            print(line)
    else:
        print("Invalid command.")
