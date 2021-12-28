"""Main loop for announce subsystem."""

from shared import config
from shared.controller import Controller
from announce.announce import Announce
from flask import Flask, request, jsonify
from flask_htpasswd import HtPasswdAuth
# from flask_cors import CORS
import threading
from shared.streamtologger import StreamToLogger
import logging
import sys

logging.basicConfig(
    filename=config.LOG_DIR + "announce.log",
    # encoding='utf-8',
    filemode='a', format='%(asctime)s %(levelname)s:%(message)s',
    level=config.LOG_LEVEL)
logger = logging.getLogger("announce")
werklog = logging.getLogger('werkzeug')
werklog.setLevel(logging.ERROR)

# redirect stdout and stderr to log file - do this before production
sys.stdout = StreamToLogger(logger,logging.INFO)
sys.stderr = StreamToLogger(logger,logging.ERROR)

def init_controller_obj():
    # let's get this party started
    controller_obj = Announce()
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

whoami = "announce"
controller_obj = init_controller_obj()

# threaded program_loop(controller_obj)
#
thread_obj = threading.Thread(target=program_loop,  args=(controller_obj,), daemon=True)
thread_obj.start()

# Flask controller
#
# Create the server object
app = Flask(__name__)
#
# Configure basic auth with htpasswd file
app.config['FLASK_HTPASSWD_PATH'] = config.HTPASSWD_FILE
app.config['FLASK_SECRET'] = 'SECRETSECRETSECRET'
app.config['FLASK_AUTH_ALL']=True
htpasswd = HtPasswdAuth(app)
#
# Serve CORS header
domain_list = []
for host in config.CONTROLLERS.values():
    domain_list.append("http://" + host["server"] + ':' + str(host["port"]))
    domain_list.append("http://" + host["altserv"] + ':' + str(host["port"]))
print(domain_list)
CORS(app, supports_credentials=True, origins=domain_list)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/cmd",methods = ['POST', 'GET'])
def cmd():
    if request.method == 'GET':
        order_obj = request.args.to_dict(flat=True)
    else:
        order_obj = request.get_json(force=True)
    response = jsonify(controller_obj.act_on_order(order_obj))
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

app.run(host="0.0.0.0", port=config.CONTROLLERS[whoami]["port"],
        debug=config.DEBUG, use_reloader=False)
