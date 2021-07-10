const path = require('path')
const electron = require('electron')
const remote = require('electron').remote
var $ = jQuery = require('../node_modules/jquery/dist/jquery.min.js');
const axios = require('axios');


$(function() {
    $("#product").submit(function (e) { 
        console.log("dededede-------")
        e.preventDefault();
        inputs = {};
        input_serialized =  $(this).serializeArray();
        input_serialized.forEach(field => {
        inputs[field.name] = field.value;
        })
        console.log(inputs)
        sendProducts({
        'type':"products",
        'upsert_data':inputs
        })
        // clear 
//        let w = remote.getCurrentWindow()
//        w.close()
    });
});

function sendProducts(payload){
    console.log("send products",payload)
    axios.defaults.headers.post['Content-Type'] = 'application/json';
    axios.post('http://localhost:7001/miri/insert', payload)
      .then((response) => {
        // Here you can handle the API response
        // Maybe you want to add to your HTML via JavaScript?
        $('#product')[0].reset();
        return response

      })
      .catch((error) => {
        let w = remote.getCurrentWindow()
        w.close()
        console.error(error);
      });

//

}

$(document).ready(function(){

    let html_ = '<option value="" disabled selected hidden>Choose Ventor...</option>';
      // you might need the next line, depending on your API provider.
    //  axios.defaults.headers.post['Content-Type'] = 'application/json';
      axios.get('http://localhost:7001/miri/fetch_ventors', {/* here you can pass any parameters you want */})
      .then((response) => {
        // Here you can handle the API response
        // Maybe you want to add to your HTML via JavaScript?
        response.data.result.forEach(myFunction);
        function myFunction(value, index, array) {
          html_ += "<option value="+"'"+value+"'"+">"+value+"</option>";
        }
        console.log(html_)
        $('#ventor').html(html_)

      })
      .catch((error) => {
        console.error(error);
      });

});


