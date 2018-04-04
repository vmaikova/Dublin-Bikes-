// Reference from https://www.w3schools.com/jquery/jquery_ajax_get_post.asp
$(document).ready(
    function(){
        $.get("/weather/hourly", function(data, status){
            console.log(data);
            for (i=0; i<10; i+=2)
            {
                $("#alertDisplay").append(data["hourly_forecast"][i]["FCTTIME"]["hour"]);
                $("#alertDisplay").append(data["hourly_forecast"][i]["FCTTIME"]["year"]);
                $("#alertDisplay").append(data["hourly_forecast"][i]["FCTTIME"]["year"]);
            }
        });   
        initializeMap();
    });

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
            console.log(location, 'location')
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