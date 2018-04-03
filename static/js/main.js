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
    }
);



//"year": "2018","mon": "3","mon_padded": "03","mon_abbrev": "Mar","mday": "30","mday_padded": "30","yday": "88","isdst": "1","epoch": "1522443600","pretty": "10:00 PM IST on March 30, 2018","civil": "10:00 PM","month_name": "March","month_name_abbrev": "Mar","weekday_name": "Friday","weekday_name_night": "Friday Night","weekday_name_abbrev": "Fri","weekday_name_unlang": "Friday","weekday_name_night_unlang": "Friday Night","ampm": "PM","tz": "","age": "","UTCDATE"