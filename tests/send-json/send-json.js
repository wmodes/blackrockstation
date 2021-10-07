
url = "http://localhost:8080/cmd";

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
  // validate json
  var json = tryParseJSONObject(jsonText);
  if (! json) {
    var msg = "<span class=error>Invalid JSON</span>";
    $("#msgs").html(msg);
  }
  else {
    var msg = "<span class=success>Valid JSON. Sending.</span>";
    $("#msgs").html(msg);
    // construct URL
    var urlPlusQuery = url + '?' + $.param(json);
    console.log("urlPlusQuery:", urlPlusQuery);
    // make request
    $.ajax({
        url: urlPlusQuery,
        type: "GET",
        dataType: "json",
        success: function(data) {
          //var json = JSON.parse(data);
          $('#results').html(JSON.stringify(data, undefined, 2))
        },
        error: function(request,error) {
          // var json = JSON.parse(request);
          $('#results').html(JSON.stringify(request, undefined, 2))
        }
      });
   }
})
