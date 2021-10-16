$(document).ready(function()
{

  $('#submit').click(function() {
    var url = "http://localhost:9090/requests/"
    var username = $('input[name=username]').val();
    var password = $('input[name=password]').val();
    //
    var endpoint = $('input[name=endpoint]').val();
    url = url + endpoint;
    //
    var data = {}
    var command = $('input[name=command]').val();
    if (command !== "") {
      data.command = command;
    }
    var input = $('input[name=input]').val();
    if (input !== "") {
      data.input = input;
    }
    console.log("click");
    $.ajax(
      {
        'username' : username,
        'password' : password,
        'url'      : url,
        'type'     : 'GET',
        'data'     : data,
        'success'  : function(results){
          $("#output").html(JSON.stringify(results));
        },
        'error'    : function(status){
          $("#output").html(JSON.stringify(status));
        }
      }
    );
  });


});
