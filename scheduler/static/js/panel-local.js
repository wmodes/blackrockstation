
const TRAINS = {
	"frt-through" : 2,
	"frt-stop" : 8,
	"psgr-through" : 3,
	"psgr-stop" : 6
}

const BTNCOLORS = "btn-primary btn-secondary btn-success btn-danger btn-warning btn-info btn-light btn-dark";
const BTNDEFAULT = "btn-secondary";
const ALERTCOLORS = "bg-primary bg-secondary bg-success bg-danger bg-warning bg-info bg-light bg-dark bg-white text-light"

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
			beforeSend: function (xhr) {
    		xhr.setRequestHeader ("Authorization", "Basic " + btoa(HTUSER + ":" + HTPASS));
			},
      url: requestURL,
      type: method,
      dataType: "json"
    };
  }
  else if(method == "POST") {
    var requestURL = url;
    // make request
    var ajax_obj = {
			beforeSend: function (xhr) {
    		xhr.setRequestHeader ("Authorization", "Basic " + btoa(HTUSER + ":" + HTPASS));
			},
      url: requestURL,
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
	// first let's check and update status
	var statusOkay = wasStatusOkay(controller, results);

	if (type == "calltrain") {
		msg = "Train has been called. New calls temporarily disabled."
		displayCallAlert("bg-warning text-dark", msg);
		setTimeout(function(){
			clearCallAlert();
			enableCalls();
		}, 5 * 60 * 1000);
	}
	else if (type == "callyear") {
		msg = "Timeslip triggered. New calls temporarily disabled."
		displayCallAlert("bg-warning text-dark", msg);
		setTimeout(function(){
			clearCallAlert();
			enableCalls();
		}, 50 * 1000);
	}
	else if (type == "changemode") {
		$(`[data-contr="${controller}"]`).prop("disabled", false);
		var cmdObj = COMMANDS.reqStatus;
		submitCmd("status", controller, cmdObj);
		setTimeout(alertSummary,1000);
	}
	else if (type == "time") {
		// if no results, i.e., ajax error
		if (! statusOkay) {
			nextSlipTime = null;
			nextTrainTime = null;
		}
		// if the status is okay
		else {
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
	}
}

// if we have AJAX errors, or the status we get back is not okay
// we need to update status
function wasStatusOkay(controller, results) {
	// if no results, i.e., ajax error
	if (!results) {
		changeStatus(controller, "unknown");
		CONTROLLERS[controller].status = "unknown";
	}
	// if we have a status, which we should if we get anything
	else if ("status" in results) {
		// if we we have "mode", we should use that
		if ("results" in results && "mode" in results.results) {
			changeStatus(controller, results.results.mode);
			CONTROLLERS[controller].status = results.results.mode;
			return true;
		}
		else if (results.status == "OK") {
			changeStatus(controller, "ok");
			CONTROLLERS[controller].status = "ok";
			return true
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
	return false;
}


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
		$("#years .btn").removeClass(BTNCOLORS);
		$("#years .btn").addClass(BTNDEFAULT);
		$("#years .btn." + currentYear).addClass("btn-success");
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
		displayStatusAlert("bg-danger text-white", "One or more controllers are in Error state");
	}
	else if (statusArray.includes("unknown")) {
		displayStatusAlert("bg-warning text-dark", "One or more controllers are in Unknown state");
	}
	else if (statusArray.includes("off") || statusArray.includes("on")) {
		displayStatusAlert("bg-warning text-dark", "One or more controllers are not in Auto mode");
	}
	else {
		displayStatusAlert("bg-success text-white", "All controllers are responsive and in Auto mode");
	}
}

function displayStatusAlert(alertClass, alertText) {
	alertEl = $("#alert-status");
	alertEl.removeClass(ALERTCOLORS);
	alertEl.html(alertText);
	alertEl.addClass(alertClass);
}

function displayCallAlert(alertClass, alertText) {
	alertEl = $("#alert-calls");
	alertEl.removeClass(ALERTCOLORS);
	alertEl.html(alertText);
	alertEl.addClass(alertClass);
}

function clearCallAlert() {
	alertEl = $("#alert-calls");
	alertEl.removeClass(ALERTCOLORS);
	alertEl.html("No current calls...");
	alertEl.addClass("alert-dark");
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
		btnClass = BTNDEFAULT;
	}else if (status == "off") {
		btnText = "Off";
		btnClass = "btn-dark";
	}
	btnEl = $(`[data-contr="${controller}"]`);
	btnEl.removeClass(BTNCOLORS);
	btnEl.html(btnText);
	btnEl.addClass(btnClass);
}

function setupStatusBtns() {
	$(".controller .btn").click(function() {
		var activeContrs = ["announce", "crossing", "lights", "radio", "television", "train"];
		var controller = $(this).data("contr");
		if (activeContrs.includes(controller)) {
			var currentStatus = CONTROLLERS[controller].status;
			if (currentStatus == "auto") {
				var cmdObj = COMMANDS.setOff;
			}
			else if (currentStatus == "off") {
				var cmdObj = COMMANDS.setOn;
			}
			else {
				var cmdObj = COMMANDS.setAuto;
			}
			$(this).prop("disabled", true);
			submitCmd("changemode", controller, cmdObj)
		}
		else {

		}
	});
}


//
// TRAIN AND TIMESLIP CALLS
//

function setupTrainCallBtns() {
	$("#trains .btn").removeClass(BTNCOLORS);
	$("#trains .btn").addClass(BTNDEFAULT);
	$("#trains .btn").click(function() {
		var controller = "scheduler";
		var call = $(this).data("call");
		var index = TRAINS[call];
		var cmdObj = COMMANDS.setTrain;
		cmdObj.index = index;
		submitCmd("calltrain", controller, cmdObj);
		disableCalls();
	});
}

function setupTimeslipCallBtns() {
	for (i=0; i<YEARS.length; i++) {
		var html = `<div><button class="btn ${BTNDEFAULT} ${YEARS[i]}" data-year="${YEARS[i]}">${YEARS[i]}</button></div>`;
		$("#years").append(html);
	}
	$("#years .btn").click(function() {
		var controller = "scheduler";
		var year = $(this).data("year");
		var cmdObj = COMMANDS.setYear;
		cmdObj.year = year;
		submitCmd("callyear", controller, cmdObj);
		disableCalls();
	});
}

function disableCalls() {
	$("#trains .btn").prop("disabled", true);
	$("#years .btn").prop("disabled", true);
}

function enableCalls() {
	$("#trains .btn").prop("disabled", false);
	$("#years .btn").prop("disabled", false);
}


//
// MAIN LOOP
//

function main() {
	setupStatusBtns();
	setupTrainCallBtns();
	setupTimeslipCallBtns();
	getNextTimes();
	setInterval(updateTimes, 1000);
	checkAllStatus();
	setInterval(checkAllStatus, statusInterval);
}

main();
