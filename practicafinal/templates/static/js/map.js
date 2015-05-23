$(document).ready(function() {
    $("#map").hide()
    $("#mostrarmapa").click(function(){
        $("#mostrarmapa").fadeOut()
        $("#map").show()
        var coord = $("#localizacion").text().split(", ")
        if (coord.length == 2) {
            var map = L.map('map').setView(coord, 14);
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { //para mapquest: http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            }).addTo(map);
            var marker = L.marker(coord).addTo(map);
        }else{
            $("#map").hide()
            alert("No hay coordenadas para esta actividad");
        }   
        
    })
});
