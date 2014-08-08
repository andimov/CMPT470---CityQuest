var placeSearch, autocomplete;
var geocoder;
var map;
var markers = {};
function initialize() {
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(49.278640, -122.919937);
  var mapOptions = {
    zoom: 11,
    center: latlng
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  var infowindow = new google.maps.InfoWindow({
    content:"Hello World!"
  });
  initializeSearch()
}

function initializeSearch() {
// Create the autocomplete object, restricting the search
// to geographical location types.
    geocoder = new google.maps.Geocoder();
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
    { types: ['geocode'] });
    // When the user selects an address from the dropdown,
    // populate the address fields in the form.
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        fillInAddress();
    });
}

function codeAddress(address, eventid) {
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
      markers[eventid] = marker;
    } else {
      alert(address);
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });


  //var infowindow = new google.maps.InfoWindow({
  //  content:"Hello World!"
  //});

  //google.maps.event.addListener(marker, 'click', function() {
  //  infowindow.open(map,marker);
  //});
}
//gets the address and sets the hidden inputs to the lat and lon of that address
function getGeo() {
    var address = document.getElementById('autocomplete').value;
    return geocoder.geocode( {'address' : address}, function(results, status){
        if (status == google.maps.GeocoderStatus.OK){
            document.getElementById('latitude').value = results[0].geometry.location.lat();
            document.getElementById('longitude').value = results[0].geometry.location.lng();
        } else {
            alert('That address is not valid because of: ' + status);
        }
    })
}

function validate(){
    if (document.getElementById('latitude').value == "" || document.getElementById('categorySelect').value == "" ){
	alert('Please enter a valid location and select a category');
	return false;   
    }
}

// [START region_fillform]
function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();
    getGeo();
/*
    for (var component in componentForm) {
        document.getElementById(component).value = '';
        document.getElementById(component).disabled = false;
    }

    // Get each component of the address from the place details
    // and fill the corresponding field on the form.
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];
        if (componentForm[addressType]) {
            var val = place.address_components[i][componentForm[addressType]];
            document.getElementById(addressType).value = val;
        }
    }
*/
}
// [END region_fillform]

// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var geolocation = new google.maps.LatLng(
            position.coords.latitude, position.coords.longitude);
            autocomplete.setBounds(new google.maps.LatLngBounds(geolocation,
            geolocation));
        });
    }
}
    
    // [END region_geolocation]


$(window).load(function(){
	$('.event').each(function(){
		codeAddress($(this).find('.addr').text(), $(this).find('.eventID').text());
	});
	//codeAddress('Vancouver');

});
$(window).load(function(){
	$('.distance').each(function(){
		var distance = $(this).text();
        	distance = Math.round(distance * 10)/10;
        	$(this).text(distance);
	});
});

$('.zoom').click(function(){
	var markerPos = markers[$(this).siblings('.eventID').text()].getPosition();
	map.setCenter(markerPos);
	map.setZoom(14);
});



$('.event').click(function(){
	$(this).addClass("selected");
	$(this).siblings().removeClass("selected");
});

$("#autocomplete").keypress(function(e1){
   if(e1.keyCode==13){          // if user is hitting enter
       return false;
   }
});   
