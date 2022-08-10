
const statusInterval = 5 * 1000;

const url = "http://localhost:8080/cmd";
const url_pre = "http://"
const url_post = "/cmd"

const CONTROLLERS = {
	"scheduler":  {"port": 8080,
                   "server": "localhost"},
	"announce":   {"port": 8081,
                   "server": "localhost"},
	"bridge":     {"port": 8082,
                   "server": "localhost"},
	"crossing":   {"port": 8083,
                   "server": "localhost"},
	"lights":     {"port": 8084,
                   "server": "localhost"},
	"radio":      {"port": 8085,
                   "server": "localhost"},
	"train":      {"port": 8086,
                   "server": "localhost"},
	"television": {"port": 8087,
                   "server": "localhost"}
}
const HTUSER = "brs";
const HTPASS = "bl@ckr0ck";

const COMMANDS = {
	"help": 				{'cmd': 'help'},
	"reqStatus": 		{'cmd': 'reqStatus'},
	"reqLog": 			{'cmd': 'reqLog',
				 				   'qty': '10'},
	"setOff":				{'cmd': 'setOff'},
	"setOn":				{'cmd': 'setOn'},
	"setAuto":			{'cmd': 'setAuto'},
	"setGlitch":		{'cmd': 'setGlitch'},
	"setYear":			{'cmd': 'setYear',
									 'year': 1938},
	"setGo":				{'cmd': 'setGo',
						       'direction': 'westbound'},
	"stateOff":			{'cmd': 'stateOff'},
	"stateOn":			{'cmd': 'stateOn'},
	"order":				{'cmd': 'order',
									 'controller': 'radio',
								   'relay': {'cmd': 'reqstatus'}},
	"reqTrains":		{'cmd': 'reqTrains',
									 'qty': '5'},
	"reqAllTrains": {'cmd': 'reqAllTrains'},
	"setAnnounce":	{'cmd': 'setAnnounce',
						 			 'announceid': 'city-of-san-francisco-california-zephyr-chicago-to-sf-announce-arrival',
						 		 	 'year': 1938},
	"setGo":				{"cmd": "setGo",
      						 "direction": "westbound"},
	"setStop":			{"cmd": "setStop"},
	"setTrain":			{"cmd": "setTrain",
      						 "direction": "westbound",
      			 			 "traintype": "freight-through",
									 "year": "1938",
								   "index": 6,
								   "note": "Scheduler requires only index, while train subsystem requires all others except index"}
}

const YEARS = [1858, 1888, 1938, 1959, 1982, 2014, 2066, 2110]
