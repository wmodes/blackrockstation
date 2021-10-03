"""Main loop for television subsystem."""

from shared import config
from shared.controller import Controller
from television.television import Television
from flask import Flask, request, jsonify
import threading
from shared.streamtologger import StreamToLogger
import logging

logging.basicConfig(
    filename=config.LOG_FILENAME,
    # encoding='utf-8',
    filemode='a', format='%(asctime)s %(levelname)s:%(message)s',
    level=config.LOG_LEVEL)
logger = logging.getLogger("television")

# redirect stdout and stderr to log file - do this before production
# sys.stdout = StreamToLogger(logger,logging.INFO)
# sys.stderr = StreamToLogger(logger,logging.ERROR)

def init_controller_obj():
    # let's get this party started
    controller_obj = Television()
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

whoami = "Television"
controller_obj = init_controller_obj()

# threaded program_loop(controller_obj)
#
thread_obj = threading.Thread(target=program_loop,  args=(controller_obj,), daemon=True)
thread_obj.start()

# flask controller
#
app = Flask(__name__) # Create the server object

@app.route("/cmd")
def cmd():
    order_obj = request.args.to_dict(flat=True)
    response = jsonify(controller_obj.act_on_order(order_obj))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run(debug=True)
