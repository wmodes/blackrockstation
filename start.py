"""Starter system for all controllers."""

from shared import config

import sys
import importlib
import logging

controllers = [
    "announce", "crossing", "lights", "radio", "scheduler", "signal",
    "trainaudio", "television"
]


def help():
    print("Available controllers:")
    for controller in controllers:
        print(f"\t%s" % controller)


def main():
    if len(sys.argv) < 2:
        help()
    elif sys.argv[1] not in controllers:
        print(f"Error: Unknown controller: %s." % sys.argv[1])
        help()
    else:
        controller = sys.argv[1]
        class_module = f"%s.%s" % (controller, controller.title())
        main_module = f"%s.main" % controller
        #import_class = importlib.import_module(class_module)
        import_main = importlib.import_module(main_module)
        import_main.main()


if __name__ == '__main__':
    main()
