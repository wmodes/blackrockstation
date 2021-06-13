"""Starter system for all controllers."""

from shared import config

# from shared.streamtologger import StreamToLogger

import sys
import importlib
import logging

controllers = [
    "announce", "crossing", "lights", "radio", "scheduler", "signal",
    "train", "television"
]


def help():
    """Provide help to user."""
    print("Available controllers:")
    for controller in controllers:
        print(f"\t%s" % controller)


def main():
    """Get everything going."""
    # handle args
    if len(sys.argv) < 2:
        help()
        return
    elif sys.argv[1] not in controllers:
        print(f"Error: Unknown controller: {sys.argv[1]}.")
        help()
        return
    controller = sys.argv[1]

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
    import_main = importlib.import_module(main_module)

    # start main loop of controller
    try:
        import_main.main()
    except KeyboardInterrupt:
        logging.info("Interrupt received")
        logging.info("Finishing")
    except:
        logging.exception('Got exception on main handler')
        raise



if __name__ == '__main__':
    main()
