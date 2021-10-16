$(document).ready(function()
{
  url = "http://localhost:9090/status.json"

  $('#submit').click(function() {
    console.log("click");
    $.ajax(
      {
        'password' : $('input[name=password]').val(),
        'username' : $('input[name=username]').val(),
        'url'      : url,
        'type'     : 'GET',
        'data'     : {
          'command' : $('input[name=command]').val(),
          'input'   : $('input[name=input]').val()
        },
        'success'  : function(results){
          $("#output").html(JSON.stringify(results));
        },
        'error'    : function(status){
          $("#output").html(JSON.stringify(status));
        }
      }
    );

    return false;
  });
});
