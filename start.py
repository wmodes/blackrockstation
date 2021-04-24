"""Starter system for all controllers."""

from shared import config

import sys
import importlib
import logging

controllers = [
    "announce",
    "crossing",
    "lights",
    "radio",
    "scheduler",
    "signal",
    "trainaudio",
    "television"
]

controller = sys.argv[1]
if controller in controllers:
    class_module = f"%s.%s" % (controller, controller.title())
    main_module = f"%s.main" % controller
    #import_class = importlib.import_module(class_module)
    import_main = importlib.import_module(main_module)
    import_main.main()
else:
    print (f"Error: Unknown controller: %s." % controller)
    print ("Available controllers:")
    for controller in controllers:
        print (f"\t%s" % controller)
