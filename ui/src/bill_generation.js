const path = require('path')
const electron = require('electron')
const remote = require('electron').remote
var $ = jQuery = require('../node_modules/jquery/dist/jquery.min.js');
const axios = require('axios');
const { dialog } = require('electron');

let stack = []

$(function() {
    $("#bill").submit(function (e) {
        console.log("dededede-------")
        e.preventDefault();
        inputs = {};
        input_serialized =  $(this).serializeArray();
        input_serialized.forEach(field => {
        inputs[field.name] = field.value;
        })
        console.log(inputs);
        stackEach(inputs)
        $('#bill')[0].reset();
        // clear
//        let w = remote.getCurrentWindow()
//        w.close()
    });
});

function stackEach(item){
    stack.push(inputs);
    document.getElementById("stack-count").innerHTML = stack.length;
}
function proccedBill(){
    var productForm = document.getElementById("bill-product");
    productForm.style.display = "none";
    var customerForm= document.getElementById("customer-dis");
    customerForm.style.display = "block"

}

$(function() {

    $("#coustomer").submit(function (e) {
    console.log("triggered... ....")


        e.preventDefault();
        inputs = {};
        input_serialized =  $(this).serializeArray();
        input_serialized.forEach(field => {
        inputs[field.name] = field.value;
        })
        console.log(inputs);
        console.log('---- --- --- ');
        console.log(stack)
        $.when(billGeneration({'user_data':inputs,'oders':stack})).then(function(){
            DispFunction("<p> Loading .... </p>");
        })



    });
});


function discardBill(){
    let w = remote.getCurrentWindow()
    w.close()
}
function DispFunction(html_){
    console.log(html_)
    document.getElementById('form-container-main').innerHTML = html_

    };
function billGeneration(payload){

        axios.defaults.headers.post['Content-Type'] = 'application/json';
        axios.post('http://localhost:7001/miri/bill_generation', payload)
          .then((response) => {
            DispFunction("I'm miRi 👧,Your mini-billing management assistant.I had generated a bill with refferance id "+response.data.bill_ref+". You can click <a target = '_blank' href="+"'"+"../../"+response.data.file_link+"'"+">here</a> to download.")
          })
          .catch((error) => {
          console.error(error);
              DispFunction("<p> 😈 403 Sorry we'd a issue, raise this to support </p>")
          });
};

window.addEventListener("load", function(){

    // Add a keyup event listener to our input element
    var name_input = document.getElementById('product_name');
    name_input.addEventListener("keyup", function(event){hinter(event)});

    // create one global XHR object
    // so we can abort old requests when a new one is make
    window.hinterXHR = new XMLHttpRequest();
});

// Autocomplete for form
function hinter(event) {

    // retireve the input element
    var input = event.target;

    // retrieve the datalist element
    var huge_list = document.getElementById('product_list');

    // minimum number of characters before we start to generate suggestions
    var min_characters = 0;

    if (input.value.length < min_characters ) {
        return;
    } else {

        // abort any pending requests
        window.hinterXHR.abort();

        window.hinterXHR.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {

                // We're expecting a json response so we convert it to an object
                var response = JSON.parse( this.responseText );
                console.log("----->>>> GOT ---->",response.products)
                // clear any previously loaded options in the datalist
                huge_list.innerHTML = "";

                response.products.forEach(function(item) {
                    // Create a new <option> element.
                    const found = stack.some(el => el.name === item)
                    if(!found){

                        var option = document.createElement('option');
                        console.log("here stack ",stack);
//                    option.data-value = item.name;
//                    option.text = item;
                        option.value = item;
                        // attach the option to the datalist element
                        huge_list.appendChild(option);
                    }

                });
            }
        };

        window.hinterXHR.open("GET", "http://localhost:7001/miri/products/query?query=" + input.value, true);
        window.hinterXHR.send()
    }
}



$(document).on('change', '#product_name', function() {
console.log("here we are in product change");
    var products_ = $("#product_name").val();
    const value_ = products_.split("/")
    $("#count").attr({
       "max" : value_[value_.length-1],        // substitute your own
       "min" : 1          // values (or variables) here
    });
});
