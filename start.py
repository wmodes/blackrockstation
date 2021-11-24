"""Starter system for all controllers."""

from shared import config

# from shared.streamtologger import StreamToLogger

import sys
import os
import importlib
import logging

controllers = [
    "announce", "console", "crossing", "lights", "radio", "scheduler", "bridge", "train", "television"
]


def help():
    """Provide help to user."""
    print("Available controllers:")
    for controller in controllers:
        print(f"\t%s" % controller)
    print("Once a controller is specified the same identity will be assumed next time (saved in .identity) unless a new controller is specified.")

def get_identity():
    """Get identity from file."""
    identity = None
    if os.path.exists(config.ID_FILE):
        with open(config.ID_FILE) as file:
            file_contents = file.read()
            identity = file_contents.split('\n')[0]
    return identity

def write_identity(identity):
    """Write identity to file."""
    with open(config.ID_FILE, "w") as file:
        file.write(identity)
    return

def main():
    """Get everything going."""
    # handle args
    # if controller is specified
    if len(sys.argv) >= 2:
        controller_candidate = sys.argv[1]
    # if no controller specified
    else:
        controller_candidate = get_identity()
        # if no saved identity
        if not controller_candidate:
            help()
            return
    if controller_candidate not in controllers:
        print(f"Error: Unknown controller: {sys.argv[1]}.")
        help()
        return
    controller = controller_candidate
    write_identity(controller)
    # handle logging
    logging.basicConfig(filename=config.LOG_FILENAME,
                        format=f"%(asctime)s {controller}: %(levelname)s: %(message)s",
                        level=logging.DEBUG)
    # logger = logging.getLogger()
    # redirect stdout and stderr to log file
    # sys.stdout = StreamToLogger(logger,logging.INFO)
    # sys.stderr = StreamToLogger(logger,logging.ERROR)
    #
    # load appropriate controller module
    # class_module = f"{controller}.{controller.title()}"
    main_module = f"{controller}.main"
    # import module and start main loop and web server
    import_main = importlib.import_module(main_module)

if __name__ == '__main__':
    main()
