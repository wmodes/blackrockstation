"""Main loop for bridge subsystem."""

from shared import config
from shared.controller import Controller
from bridge.bridge import Bridge
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import threading
from shared.streamtologger import StreamToLogger
import logging
import sys

logging.basicConfig(
    filename=config.LOG_DIR + "bridge.log",
    # encoding='utf-8',
    filemode='a', format='%(asctime)s %(levelname)s:%(message)s',
    level=config.LOG_LEVEL)
logger = logging.getLogger("bridge")
werklog = logging.getLogger('werkzeug')
werklog.setLevel(logging.ERROR)

# redirect stdout and stderr to log file - do this before production
sys.stdout = StreamToLogger(logger,logging.DEBUG)
sys.stderr = StreamToLogger(logger,logging.ERROR)

def init_controller_obj():
    # let's get this party started
    controller_obj = Bridge()
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

whoami = "bridge"
controller_obj = init_controller_obj()

# threaded program_loop(controller_obj)
#
thread_obj = threading.Thread(target=program_loop,  args=(controller_obj,), daemon=True)
thread_obj.start()

# flask controller
#
app = Flask(__name__) # Create the server object
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/cmd",methods = ['POST', 'GET'])
def cmd():
    if request.method == 'GET':
        order_obj = request.args.to_dict(flat=True)
    else:
        order_obj = request.get_json(force=True)
    response = jsonify(controller_obj.act_on_order(order_obj))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run(host="0.0.0.0", port=config.CONTROLLERS[whoami]["port"],
        debug=config.DEBUG, use_reloader=False)
