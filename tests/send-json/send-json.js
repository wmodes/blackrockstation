
url = "http://localhost:8080/cmd";
url_pre = "http://"
url_post = "/cmd"
CONTROLLERS = {
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
