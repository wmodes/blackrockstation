var grammar;
var spacerFlag = false;
var yearMin = 1998;
var yearMax = 2104;

function randYear(){
  return Math.floor(Math.random() * (yearMax - yearMin + 1)) + yearMin;
}

function genTrace(){
  return grammar.flatten("#description#");
}

function output(str, cls) {
  $("#output").append(`<span class="${cls}">${str}</span>`);
  spacerFlag = false;
}

function spacer() {
  if (! spacerFlag) {
    $("#output").append(`<p class="spacer">&nbsp;</p>`);
  }
  spacerFlag = true;
}

function generate() {
  // iterate over states in railyard data
  for (stateIndex=0; stateIndex<railyardData.length; stateIndex++) {
    spacer();
    var soloFlag = false;
    var stateObj = railyardData[stateIndex];
    var stateName = stateObj.state;
    output(`${stateName} `, "state");
    spacer();
    var cityArray = stateObj.cities;
    // iterate over cities in state
    for (cityIndex=0; cityIndex<cityArray.length; cityIndex++) {
      if (soloFlag) {
        spacer();
        soloFlag = false;
      }
      var cityObj = cityArray[cityIndex];
      var cityName = cityObj.city;
      // console.log(cityName, cityObj.yards.length)
      if (cityObj.yards.length > 2) {
        spacer();
        soloFlag = true;
      }
      output(`${cityName} `, "city");
      var yardArray = cityObj.yards;
      // iterate over cities in state
      for (yardIndex=0; yardIndex<yardArray.length; yardIndex++) {
        var yardObj = yardArray[yardIndex];
        var yardName = yardObj.yard;
        var yardCarrier = yardObj.carrier;
        var yardNotes = yardObj.notes;
        if (yardCarrier) {
          output(`(${yardCarrier}*) `, "carrier");
        }
        if (yardName) {
          output(`${yardName} `, "yard");
        }
        if (yardNotes) {
          output(`(${yardNotes}) `, "notes");
        }
        var desc = grammar.flatten("#description#");
        output(`${desc} `, "desc");
        output(`(${randYear()}) `, "year");
      }
    }
  }
}

function main() {
  generate();
}

$(document).ready(function(){

  grammar = tracery.createGrammar(grammarObj);
  main();

});
