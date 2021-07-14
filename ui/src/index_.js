const path = require('path')
const electron = require('electron')
var $ = jQuery = require('../node_modules/jquery/dist/jquery.min.js');
const axios = require('axios');

$(document).ready(function(){
// Menu tab for miRi
console.log("--api call for fetch info 1--")
    fetchInfo();
 });


 function fetchInfo(){

    axios.get('http://localhost:7001/miri/fetch_counts')
      .then((response) => {
        document.getElementById("bills_count").innerHTML = response.data.result.bills;
        document.getElementById("products_count").innerHTML = response.data.result.products;
         document.getElementById("ventors_count").innerHTML = response.data.result.ventors;
      })
      .catch((error) => {
        console.error(error);
      });

 }

 $(document).ready(function() {

  typing( 0, $('.typewriter-text').data('text') );

  function typing( index, text ) {

    var textIndex = 1;

    var tmp = setInterval(function() {
      if ( textIndex < text[ index ].length + 1 ) {
				$('.typewriter-text').text( text[ index ].substr( 0, textIndex ) );
				textIndex++;
			} else {
        //setTimeout(function() { deleting( index, text ) }, 2000);
        clearInterval(tmp);
      }

		}, 150);

	}
});
