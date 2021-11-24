"""Main loop for scheduler subsystem."""

from shared import config
from shared.controller import Controller
from scheduler.scheduler import Scheduler
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import threading
from shared.streamtologger import StreamToLogger
import logging
import sys

logging.basicConfig(
    filename=config.LOG_DIR + "scheduler.log",
    # encoding='utf-8',
    filemode='a', format='%(asctime)s %(levelname)s:%(message)s',
    level=config.LOG_LEVEL)
logger = logging.getLogger("scheduler")
logger.setLevel(config.LOG_LEVEL)
werklog = logging.getLogger('werkzeug')
werklog.setLevel(logging.ERROR)

# redirect stdout and stderr to log file - do this before production
sys.stdout = StreamToLogger(logger,logging.INFO)
sys.stderr = StreamToLogger(logger,logging.ERROR)

def init_controller_obj():
    # let's get this party started
    controller_obj = Scheduler()
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

whoami = "scheduler"
controller_obj = init_controller_obj()

# threaded program_loop(controller_obj)
#
thread_obj = threading.Thread(target=program_loop,  args=(controller_obj,), daemon=False)
thread_obj.start()

# flask controller
#
# Create the server object
app = Flask(__name__,
            static_url_path="",
            # static_folder="static",
            # template_folder="template"
            )
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

# @app.route("/<path:filename>")
# def upload1():
#     return send_static_file("json.html")

# @app.route('/json')
# def send_json():
#     filepath = "send-json/index.html"
#     logging.debug(f"looking for static file: {filepath}")
#     content = get_file(filepath)
#     return Response(content, mimetype="text/html")

app.run(host="0.0.0.0", port=config.CONTROLLERS[whoami]["port"],
        debug=config.DEBUG,use_reloader=False)
