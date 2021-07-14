const path = require('path')
const electron = require('electron')
const remote = require('electron').remote
var $ = jQuery = require('../node_modules/jquery/dist/jquery.min.js');
const axios = require('axios');
const ipc = require('electron').ipcRenderer;


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
        ipc.send('update-notify-value', "fetch-info");
        // clear 
//        let w = remote.getCurrentWindow()
//        w.close()
    });
});
function displayFunction(msg){
    document.getElementById('MiRi').innerHTML = msg;
}

function sendProducts(payload){
    console.log("send products",payload)
    axios.defaults.headers.post['Content-Type'] = 'application/json';
    axios.post('http://localhost:7001/miri/insert', payload)
      .then((response) => {
        // Here you can handle the API response
        // Maybe you want to add to your HTML via JavaScript?
        displayFunction("Product insert successfully 🎉 🎁 🎈")
        $('#product')[0].reset();
        return response

      })
      .catch((error) => {
        displayFunction("Product insertion failed. 💣 check your inputs..")
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


