function GEOCODE(address){
  var r = Maps.newGeocoder().geocode(address)
        for (var i = 0; i < r.results.length; i++) {
            var res = r.results[i]
            return res.geometry.location.lat + ", " + res.geometry.location.lng
  
  }
}

function RGEOCODE(latlong){
  var latlong = latlong.split(',')
  var lat = latlong[0];
  var long = latlong[1];
  var response = Maps.newGeocoder().reverseGeocode(lat, long);
  var address = response["results"][0].formatted_address;
  return address
}