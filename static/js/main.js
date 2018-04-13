// Reference from https://www.w3schools.com/jquery/jquery_ajax_get_post.asp
$(document).ready(
    function(){
        initializeMap();
        getWeather ()

    });

    function getWeather() 
    {
        const currentDate = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit', hour12: true }); 
        $("#CityAndTime").html(`Dublin ${currentDate}`)

        $.get("/weather/hourly", function(data, status){

                $("#weatherTemp").html(data["hourly_forecast"][0]["temp"]["metric"] + " °C");
                $("#weatherImage").attr("src", data["hourly_forecast"][0]["icon_url"]);
                $("#weatherFeelsLike").html(" Feels like: " + data["hourly_forecast"][0]["feelslike"]["metric"] + " °C");
                $("#weatherDescription").html(data["hourly_forecast"][0]["condition"]);
                $("#weatherHumidity").html("Humidity: " + data["hourly_forecast"][0]["humidity"] + " %");
                $("#weatherWind").html("Wind: " + data["hourly_forecast"][0]["wspd"]["metric"] + " km/h");
                
                 for (i=2; i<5; i+=2)
                 {
                    $("#lowerPart").append(
                        `<hr> 
                        <div class = "row lessPadding">
                          <div class="col-md-4">
                          <p class="text-left">${data["hourly_forecast"][i]["FCTTIME"]["civil"]}</p>
                          </div>
                          <div class="col-md-4">
                          <image id = "weatherImage" src = "${data["hourly_forecast"][i]["icon_url"]}"> </image>
                          </div>
                          <div class="col-md-4">
                          <p class="text-right">${data["hourly_forecast"][i]["temp"]["metric"]} °C</p>
                          </div>
                        </div>`
                    ); 

                 }
        }); 
    }





// Reference from https://developers.google.com/maps/documentation/javascript/examples/marker-simple

function initializeMap()
{
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13.1,
        center: new google.maps.LatLng(53.3475, -6.2703),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var locations = [];
    var getJSON = function(url, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.responseType = 'json';
        xhr.onload = function() {
            var status = xhr.status;
            if (status === 200) {
                callback(null, xhr.response);
            } else {
                callback(status, xhr.response);
            }
        };
        xhr.send();
    };

    getJSON('https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=6e5370c5f5f18f19d1bd95ba3279ace3208759ab',
        function(err, data) {
            if (err !== null) {
                console.log('error')
            } else {
                console.log('sucess', data)
                setLocations(data)
            }
        });
    function setLocations(data) {
        for (var i = 0; i < data.length; i++) {
            var location = [];
            location.push(data[i].name, data[i].position.lat, data[i].position.lng, data[i].available_bikes, data[i].available_bike_stands, data[i].number, data[i].contract_name, data[i].banking, data[i].bonus, data[i].status)
            locations.push(location)
        }
        addMarkersToTheMap();
    }

    var marker, i;

    function addMarkersToTheMap() {
        for (i = 0; i < locations.length; i++) {

            marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                map: map
            });

            var contentString = '<div>' + locations[i][0] + '<ul>' +
                '<li>Number of available bikes: ' + locations[i][3] + '</li>' +
                '<li>Number of available bikes stands: ' + locations[i][4] + '</li>' +
                '<li>Number: ' + locations[i][5] + '</li>' +
                '<li>Contact name: ' + locations[i][6] + '</li>' +
                '<li>Banking: ' + locations[i][7] + '</li>' +
                '<li>Bonus: ' + locations[i][8] + '</li>' +
                '<li>Status: ' + locations[i][9] + '</li>' +
                '</ul>' + '</div>';

            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infowindow.setContent(locations[i][0]);
                    //infowindow.setContent(contentString[i]);
                    infowindow.open(map, marker);
                }
            })(marker, i));            
        }
    }
}

