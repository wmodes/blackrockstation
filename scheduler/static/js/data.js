

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
				beforeSend: function (xhr) {
	    		xhr.setRequestHeader ("Authorization", "Basic " + btoa(HTUSER + ":" + HTPASS));
				},
        url: requestURL,
        type: method,
        dataType: "json",
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
        data: JSON.stringify(json)
      };
    }
    jqxhr = $.ajax(ajax_obj)

		jqxhr.done(function(data) {
      //var json = JSON.parse(data);
      results = JSON.stringify(data, undefined, 2).replace(/\\n/g, '<br>');
      $('#results').html(results)
    })

		jqxhr.fail(function(request,error) {
      // var json = JSON.parse(request);
      $('#results').html(JSON.stringify(request, undefined, 2))
    })

		jqxhr.always(function(){
	    //here is how to access the response header
	    console.log("Header: " + jqxhr.getResponseHeader("Content-Type"));
			console.log("Header: " + jqxhr.getResponseHeader("Access-Control-Allow-Origin"));
			console.log("Header: " + jqxhr.getResponseHeader("Access-Control-Allow-Credentials"));
	  });
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
	else if (cmd == "stateOn" || cmd == "stateOff") {
			$('input[name=controller][value=crossing]').prop("checked", true);
	}
	else if (cmd == "setTrain") {
			$('input[name=controller][value=train]').prop("checked", true);
	}
});
