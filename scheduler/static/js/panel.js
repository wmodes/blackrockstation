
//
// GLOBALS
//

statusInterval = 15 * 1000;
// url = "http://localhost:8080/cmd";
url_pre = "http://"
url_post = "/cmd"
var CONTROLLERS = {
	"scheduler":  {"port": 8080,
                 "server": "brs-scheduler.local",
								 "status" : null},
	"announce":   {"port": 8081,
                 "server": "brs-announce.local",
								 "status" : null},
	"bridge":     {"port": 8082,
                 "server": "brs-bridge.local",
								 "status" : null},
	"crossing":   {"port": 8083,
                 "server": "brs-crossing.local",
								 "status" : null},
	"lights":     {"port": 8084,
                 "server": "brs-lights.local",
								 "status" : null},
	"radio":      {"port": 8085,
                 "server": "brs-radio.local",
								 "status" : null},
	"train":      {"port": 8086,
                 "server": "brs-train.local",
								 "status" : null},
	"television": {"port": 8087,
                 "server": "brs-television.local",
								 "status" : null}
}

var COMMANDS = {
	"reqStatus": 		{'cmd': 'reqStatus'},
	"setOff":				{'cmd': 'setOff'},
	"setOn":				{'cmd': 'setOn'},
	"setAuto":			{'cmd': 'setAuto'},
	"setYear":			{'cmd': 'setYear',
									 'year': 1938},
	"setTrain":			{"cmd": "setTrain",
								   "index": 6,
								   "note": "Scheduler requires only index, while train subsystem requires all others except index"}
}

var nextSlipTime = null;
var nextTrainTime = null;
var currentYear = null;

//
// AJAX
//

// submit cmd (as JSON) and get results (as JSON)
function submitCmd(type, controller, cmdObj) {
	// choose or pass cmdObj
	// set method
	var method = "POST";
	// choose or pass controller
	// no need to validate cmdObj as JSON
	// construct url
	var url = url_pre + CONTROLLERS[controller].server + ':' + CONTROLLERS[controller].port + url_post;
	// construct ajax params
  if (method == "GET") {
    // construct final URL
    var requestURL = url + '?' + $.param(cmdObj);
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
      data: JSON.stringify(cmdObj)
    };
		// do AJAX call
    $.ajax(ajax_obj)
    .done(function(data) {
			// console.log("Success:",controller);
      //var json = JSON.parse(data);
      processAjaxResults(type, controller, data);
    })
    .fail(function(request,error) {
			// console.log("Fail:",controller);
      // var json = JSON.parse(request);
			processAjaxResults(type, controller, null);
    })
	}
}

// params:
// 	type - status, call, or time
// 	controller - controller that we sent to
// 	results - results from ajax (errors return at null)
function processAjaxResults(type, controller, results) {
	if (type == "status") {
		// if no results, i.e., ajax error
		if (!results) {
			changeStatus(controller, "unknown");
			CONTROLLERS[controller].status = "unknown";
		}
		// if we have a status, which we should if we get anything
		else if ("status" in results) {
			// if we we have "mode", we should use that
			if ("mode" in results.results) {
				changeStatus(controller, results.results.mode);
				CONTROLLERS[controller].status = results.results.mode;
			}
			else if (results.status == "OK") {
				changeStatus(controller, "ok");
				CONTROLLERS[controller].status = "ok";
			}
			else if (results.status == "FAIL") {
				changeStatus(controller, "error");
				CONTROLLERS[controller].status = "error";
			}
			else {
				changeStatus(controller, "unknown");
				CONTROLLERS[controller].status = "unknown";
			}
		}
		// if status not present
		else {
			changeStatus(controller, "unknown");
			CONTROLLERS[controller].status = "unknown";
		}
	}
	else if (type == "call") {
		if (!results) {

		}
	}
	else if (type == "time") {
		// if no results, i.e., ajax error
		if (!results) {
			nextSlipTime = null;
			nextTrainTime = null;
		}
		// if we have a status, which we should if we get anything
		else if ("status" in results) {
			// if we we have "mode", we should use that
			if (results.status == "OK")  {
				//
				// update current year
				currentYear = results.results.currentYear;
				//
				// parse and update timeslip
				var nextTimeslip = results.results.nextTimeslip;
				var split = nextTimeslip.split(':');
				var ms = 1000 * (parseInt(split[0]) * 60 + parseInt(split[1]));
				// get current time
				var t = new Date();
				// add timeslip to current to get future time
				var ts = new Date(t.getTime() + ms);
				nextSlipTime = ts;
				//
				// parse and update train time
				nextTrainTime = parseFutureHHMM( results.results.nextTrain.time);
				// update train description
				var trainDesc = results.results.nextTrain.event;
				updateTrain(trainDesc);
			}
			// if status other than "OK"
			else {
				nextSlipTime = null;
				nextTrainTime = null;
			}
		}
		// if "status" not in results (shouldn't happen)
		else {
			nextSlipTime = null;
			nextTrainTime = null;
		}
	}
}


$("button").click(function(){
	var buttonData = $(this).data("btn");
	console.log(buttonData);
})


//
// TIME UPDATES
//

function updateTimes() {
	var now = new Date();
	// check for new times
	if (nextSlipTime < now || nextTrainTime < now) {
		getNextTimes();
	}
	// otherwise display current time, timeslip, and train arrival
	else {
		// display current time
		$("#time-current").html(formatDate(now));
		// display current year
		$("#current-year").html(currentYear);
		// display timeslip time
		if (nextSlipTime) {
			$("#time-slip").html(msToTime(nextSlipTime - now));
		} else {
			$("#time-slip").html("???");
		}
		// display train time
		if (nextTrainTime) {
			$("#time-train").html(msToTime(nextTrainTime - now));
		} else {
			$("#time-train").html("???");
		}
	}
}

function updateTrain(text) {
	$("#next-train").html(text);
}

function getNextTimes() {
	var cmdObj = COMMANDS.reqStatus;
	var controller = "scheduler";
	submitCmd("time", controller, cmdObj);
}

var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// return date formatted as: Sun Nov 14, 2021 14:36:21
function formatDate(d) {
	var day = days[d.getDay()];
	var mo = months[d.getMonth()];
	var dt = d.getDate();
	var yr = d.getFullYear();
	var hr = d.getHours();
	var min = d.getMinutes();
	if (min < 10) {
	    min = "0" + min;
	}
	var sec = d.getSeconds();
	if (sec < 10) {
	    sec = "0" + sec;
	}
	return `${day} ${mo} ${dt}, ${yr} ${hr}:${min}:${sec}`;
}

function msToTime(duration) {
  var milliseconds = Math.floor((duration % 1000) / 100),
    seconds = Math.floor((duration / 1000) % 60),
    minutes = Math.floor((duration / (1000 * 60)) % 60),
    hours = Math.floor((duration / (1000 * 60 * 60)) % 24);
  hours = (hours < 10) ? "0" + hours : hours;
  minutes = (minutes < 10) ? "0" + minutes : minutes;
  seconds = (seconds < 10) ? "0" + seconds : seconds;
  return hours + ":" + minutes + ":" + seconds;
}

function parseFutureHHMM( t ) {
   var now = new Date();
	 var futureDate = new Date();
   var time = t.match( /(\d+)(?::(\d\d))?\s*(p?)/ );
   futureDate.setHours( parseInt( time[1]) + (time[3] ? 12 : 0) );
   futureDate.setMinutes( parseInt( time[2]) || 0 );
	 // if the constructed date is in the past, add a day
	 if (futureDate - now < 0) {
		 var ms = 24*60*60*1000;
		 futureDate = new Date(futureDate.getTime() + ms);
	 }
   return futureDate;
}

//
// ALERT UPDATES
//

function alertSummary() {
	var statusArray = [];
	var controllerList = Object.keys(CONTROLLERS);
	for (const controller of controllerList) {
		statusArray.push(CONTROLLERS[controller].status);
	}
	if (statusArray.includes("error")) {
		displayStatusAlert("alert-danger", "One or more controllers are in Error state");
	}
	else if (statusArray.includes("unknown")) {
		displayStatusAlert("alert-warning", "One or more controllers are in Unknown state");
	}
	else if (statusArray.includes("off") || statusArray.includes("on")) {
		displayStatusAlert("alert-warning", "One or more controllers are not in Auto mode");
	}
	else {
		displayStatusAlert("alert-success", "All controllers are responsive and in Auto mode");
	}
}

function displayStatusAlert(alertClass, alertText) {
	alertEl = $("#alert-status");
	alertColors = ["alert-primary", "alert-secondary", "alert-success", "alert-danger", "alert-warning", "alert-info", "alert-light", "alert-dark"];
	alertEl.removeClass(alertColors);
	alertEl.html(alertText);
	alertEl.addClass(alertClass);
}


//
// STATUS UPDATES
//

function checkAllStatus() {
	var cmdObj = COMMANDS.reqStatus;
	var controllerList = Object.keys(CONTROLLERS);
	for (const controller of controllerList) {
		submitCmd("status", controller, cmdObj);
	}
	setTimeout(alertSummary, 3000);
}

function changeStatus(controller, status) {
	if (status == "unknown") {
		btnText = "Unknown";
		btnClass = "btn-danger";
	} else if (status == "error") {
		btnText = "Error";
		btnClass = "btn-danger";
	} else if (status == "ok") {
		btnText = "OK";
		btnClass = "btn-success";
	} else if (status == "auto") {
		btnText = "Auto";
		btnClass = "btn-success";
	} else if (status == "on") {
		btnText = "On";
		btnClass = "btn-light";
	}else if (status == "off") {
		btnText = "Off";
		btnClass = "btn-dark";
	}
	btnEl = $(`[data-btn="${controller}"]`);
	btnColors = ["btn-primary", "btn-secondary", "btn-success", "btn-danger", "btn-warning", "btn-info", "btn-light", "btn-dark"];
	btnEl.removeClass(btnColors);
	btnEl.html(btnText);
	btnEl.addClass(btnClass);
}


//
// MAIN LOOP
//

function main() {
	getNextTimes();
	setInterval(updateTimes, 1000);
	checkAllStatus();
	setInterval(checkAllStatus, statusInterval);
}

main();
