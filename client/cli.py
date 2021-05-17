__version__ = "0.1"
__author__ = "T K Sourab <sourabhtk37@gmail.com>"

import argparse
import logging
import logging.config
import time

from http_client import get_key, put_key

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

DEFAULT_API_URL = "http://127.0.0.1:8000/api/v1/keys"
WATCH_INTERVAL = 1


def args_handler(args):
    """Handle cli arguments

    watch segment of this function polls the get_key api caller in specified
    interval(configurable from cli)

    :params args: Namespace object from parsing cli options (argparse)
    :returns None
    """
    if args.get:
        kv_dict = get_key(args.url, args.get)
        if kv_dict:
            print(kv_dict)

    if args.put:
        key, value = args.put
        put_key(args.url, key, value)

    if args.watch:
        kv_dict = None
        logging.info(
            f"Watching for changes by polling API endpoint at {args.interval} seconds interval"
        )
        print("Press Ctrl+c to interrupt watch")
        try:
            while True:
                current_kv_dict = get_key(args.url, args.watch)
                if kv_dict != current_kv_dict:
                    kv_dict = current_kv_dict
                    print(kv_dict)
                    
                time.sleep(int(args.interval))
        except KeyboardInterrupt:
            print("Watch Interrupted!")
            logging.info(f"Watch Stopped")


def main():
    """Parse args from cli

    Calls args_handler with parsed arguments from cli
    """

    parser = argparse.ArgumentParser(
        prog="http client",
        description="Call HTTP endpoints for a key value store service",
    )
    parser.add_argument(
        "-url", metavar="http_api_url", help="Api server url", default=DEFAULT_API_URL
    )
    parser.add_argument(
        "-get", metavar="Key", help="Retreive key from server, eg: -get a"
    )
    parser.add_argument(
        "-put",
        metavar=("Key", "Value"),
        help="Add key:value to server, eg: -put a b",
        nargs=2,
    )
    parser.add_argument(
        "-watch", metavar="Key", help="Watch key for changes, eg: -watch a"
    )
    parser.add_argument(
        "-interval",
        metavar="seconds",
        help="Set watch/poll interval for watch option",
        default=WATCH_INTERVAL,
    )

    parser.set_defaults(func=args_handler)
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("Too few arguments")

    func(args)


if __name__ == "__main__":
    main()
