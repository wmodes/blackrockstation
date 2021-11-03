
url = "http://localhost:8080/cmd";
url_pre = "http://"
url_post = "/cmd"
CONTROLLERS = {
	"scheduler":  {"port": 8080,
                   "server": "brs-scheduler.local"},
	"announce":   {"port": 8081,
                   "server": "brs-announce.local"},
	"bridge":     {"port": 8082,
                   "server": "brs-bridge.local"},
	"crossing":   {"port": 8083,
                   "server": "brs-crossing.local"},
	"lights":     {"port": 8084,
                   "server": "brs-lights.local"},
	"radio":      {"port": 8085,
                   "server": "brs-radio.local"},
	"train":      {"port": 8086,
                   "server": "brs-train.local"},
	"television": {"port": 8087,
                   "server": "brs-tv.local"}
}

var COMMANDS = {
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


/**
 * If you don't care about primitives and only objects then this function
 * is for you, otherwise look elsewhere.
 * This function will return `false` for any valid json primitive.
 * EG, 'true' -> false
 *     '123' -> false
 *     'null' -> false
 *     '"I'm a string"' -> false
 * From: https://stackoverflow.com/questions/3710204/how-to-check-if-a-string-is-a-valid-json-string-in-javascript-without-using-try
 */
function tryParseJSONObject (jsonString){
    try {
        var obj = JSON.parse(jsonString);
        // Handle non-exception-throwing cases:
        // Neither JSON.parse(false) or JSON.parse(1234) throw errors, hence the type-checking,
        // but... JSON.parse(null) returns null, and typeof null === "object",
        // so we must check for that, too. Thankfully, null is falsey, so this suffices:
        if (obj && typeof obj === "object") {
            return obj;
        }
    }
    catch (e) { }
    return false;
};

$("#submit").click(function(){
  var jsonText = $("#json").val();
  var method = $('input[name="method"]:checked').val();
  var controller = $('input[name="controller"]:checked').val();
  // validate json
  var json = tryParseJSONObject(jsonText);
  if (! json) {
    var msg = "<span class=error>Invalid JSON</span>";
    $("#msgs").html(msg);
  }
  else {
    var msg = "<span class=success>Valid JSON. Sending.</span>";
    $("#msgs").html(msg);
		var url = url_pre + CONTROLLERS[controller].server + ':' + CONTROLLERS[controller].port + url_post;
    if (method == "GET") {
      // construct URL
      var requestURL = url + '?' + $.param(json);
      // make request
      var ajax_obj = {
        url: requestURL,
        type: method,
        dataType: "json"
      };
    }
    else if(method == "POST") {
      var requestURL = url;
      // make request
      var ajax_obj = {
        url: requestURL,
        // url: "/get",
        type: method,
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(json)
      };
    }
    $.ajax(ajax_obj)
    .done(function(data) {
      //var json = JSON.parse(data);
      $('#results').html(JSON.stringify(data, undefined, 2))
    })
    .fail(function(request,error) {
      // var json = JSON.parse(request);
      $('#results').html(JSON.stringify(request, undefined, 2))
    })
   }
})

$(".cmd-button").click(function(){
	var cmd = $(this).data("cmd");
	var cmdObj = COMMANDS[cmd];
	$("#json").val(JSON.stringify(cmdObj));
	if (cmd == "order" || cmd == "reqTrains" || cmd == "reqAllTrains") {
			$('input[name=controller][value=scheduler]').prop("checked", true);
	}
	else if (cmd == "setAnnounce") {
			$('input[name=controller][value=announce]').prop("checked", true);
	}
	else if (cmd == "setGo" || cmd == "setStop") {
			$('input[name=controller][value=bridge]').prop("checked", true);
	}
	else if (cmd == "setTrain") {
			$('input[name=controller][value=train]').prop("checked", true);
	}
});
