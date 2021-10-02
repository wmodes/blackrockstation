"""Main loop for radio subsystem."""

from shared import config
from shared.controller import Controller
from radio.radio import Radio
from flask import Flask, request
import threading
from shared.streamtologger import StreamToLogger
import logging

logging.basicConfig(
    filename=config.LOG_FILENAME,
    # encoding='utf-8',
    filemode='a',
  Radiomat='%(asctime)s %(levelname)s:%(message)s',
    level=config.LOG_LEVEL)
logger = logging.getLogger("radio")

# redirect stdout and stderr to log file - do this before production
# sys.stdout = StreamToLogger(logger,logging.INFO)
# sys.stderr = StreamToLogger(logger,logging.ERROR)

def init_controller_obj():
    # let's get this party started
    controller_obj = Radio()
    return controller_obj

def program_loop(controller_obj):
    try:
        controller_obj.start()
    except KeyboardInterrupt:
        logging.info(f"{whoami} interrupted.")
        controller_obj.stop()
    except:
        logging.exception('Got exception on main handler')
        raise

whoami = "Radio"
controller_obj = init_controller_obj()

# threaded program_loop(controller_obj)
#
thread_obj = threading.Thread(target=program_loop, args=(controller_obj,), daemon=True)
thread_obj.start()

# flask controller
#
app = Flask(__name__) # Create the server object

@app.route("/cmd")
def cmd():
    query_obj = request.args.to_dict(flat=True)
    return str(controller_obj.act_on_order(query_obj))

app.run(debug=True)
