var locations = [];
var contentStrings = [];

// Reference from https://www.w3schools.com/jquery/jquery_ajax_get_post.asp
$(document).ready(function(){
        initializeMap();
        getWeather ();
    });

// Reference from https://developers.google.com/maps/documentation/javascript/examples/marker-simple
// Reference from https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple-max
function getWeather() 
{
    const currentDate = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit', hour12: true }); 
    $("#CityAndTime").html(`Dublin ${currentDate}`)
    $.get("/weather/hourly", function(data, status){

        $("#weatherTemp").html(data["hourly_forecast"][0]["temp"]["metric"] + " &#8451;");
        $("#weatherImage").attr("src", data["hourly_forecast"][0]["icon_url"]);
        $("#weatherFeelsLike").html(" Feels like: " + data["hourly_forecast"][0]["feelslike"]["metric"] + " &#8451;");
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
                        <p class="text-right">${data["hourly_forecast"][i]["temp"]["metric"]} &#8451;</p>
                        </div>
                    </div>`
                ); 
            }
    });
}






// Reference from https://developers.google.com/maps/documentation/javascript/examples/marker-simple
// Reference from https://developers.google.com/maps/documentation/javascript/examples/infowindow-simple

function initializeMap()
{
//    var locations = [];
//         var contentStrings = [];

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
                setLocations(data);
                generateDropdown();
            }
        });


    function setLocations(data) {
        for (var i = 0; i < data.length; i++) {
            var location = [];
            location.push(data[i].name, data[i].position.lat, data[i].position.lng, data[i].available_bikes, data[i].available_bike_stands, data[i].number,
                data[i].contract_name, data[i].banking, data[i].bonus, data[i].status, data[i].number, data[i].address, data[i].bike_stands, data[i].available_bikes)
            locations.push(location);
            var contentString = '<div>' + locations[i][0] + '<ul>' +
                '<li>Number of available bikes: ' + locations[i][3] + '</li>' +
                '<li>Number of free stands: ' + locations[i][12] + '</li>' +
                '<p class="text-primary" onclick="displayMoreInfo(' + i + ')"> More info </p>'
            '</ul>' + '</div>';

            contentStrings.push(contentString);
        }
        addMarkersToTheMap();
    }

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12.8,
        center: new google.maps.LatLng(53.3498, -6.2703),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    function addMarkersToTheMap() {
        for (i = 0; i < locations.length; i++) {

            marker = new google.maps.Marker({
                position: new google.maps.LatLng(locations[i][1], locations[i][2]),
                map: map,
                icon: getMarker(locations[i][13])
            });

            google.maps.event.addListener(marker, 'click', (function(marker, i) {
                return function() {
                    infowindow.setContent(contentStrings[i]);
                    infowindow.open(map, marker);
                }
            })(marker, i));

        }
    }
}

function displayMoreInfo(id) {
    $('#hiddenView').show(400);
    showTable();
    document.getElementsByClassName("station-number")[0].innerHTML = locations[id][10];
    document.getElementsByClassName("address")[0].innerHTML = locations[id][11];
    document.getElementsByClassName("bikes-available")[0].innerHTML = locations[id][13];
    document.getElementsByClassName("free-stands")[0].innerHTML = locations[id][4];
    document.getElementsByClassName("capacity")[0].innerHTML = locations[id][12];
    locations[id][8] === true ? document.getElementsByClassName("card-payments")[0].innerHTML = 'Yes' : document.getElementsByClassName("card-payments")[0].innerHTML = 'No';
}

function displayTable(){
    
}

// function clearDOM() {
//     document.getElementsByClassName("station-number")[0].innerHTML = '';
//     document.getElementsByClassName("station-name")[0].innerHTML ='';
//     document.getElementsByClassName("address")[0].innerHTML = '';
//     document.getElementsByClassName("bikes-available")[0].innerHTML ='';
//     document.getElementsByClassName("free-stands")[0].innerHTML ='';
//     document.getElementsByClassName("capacity")[0].innerHTML = '';
//     document.getElementsByClassName("card-payments")[0].innerHTML = '';
// }

function generateDropdown(){
    for (var i = 0; i < locations.length; i++) {
        var option = document.createElement("option");
        option.setAttribute("value", i);
        option.innerHTML = locations[i][0];
        var select = document.getElementsByTagName("select")[0];
        select.appendChild(option)
    }
}

function showTable() {
    document.getElementsByClassName("hide-table")[0].style.display = 'block';
}

function getMarker(x) {
    if (x > 10) {
        return 'http://maps.google.com/mapfiles/ms/icons/green-dot.png';
    } else if (x >= 1 && x < 10) {
        return 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png';
    } else {
        return 'http://maps.google.com/mapfiles/ms/icons/red-dot.png';
    }
}
