$(document).ready(function() {

    $.getJSON('graphql?query={%0A%09countries(name%3A"New Zealand"){%0A %09events{%0A category%0A }%0A%09}%0A}', function(catdata) {
        var allCategories = {};
        catdata["data"]["countries"][0]["events"].forEach(function(item) {
            if (allCategories.hasOwnProperty(item)) {} else {
                allCategories[item["category"]] = ""
            }
        });
        $('#nzcategory').autocomplete({
            data: allCategories,
            limit: 5,
            onAutocomplete: function(val) {
                var container = document.getElementById('eventfindaresponses');
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                $.getJSON('graphql?query={%0A events(category%3A "' + encodeURIComponent(val) + '"){%0A title%0A description%0A }%0A}', function(resdata) {
                    var counter = 0;
                    resdata["data"]["events"].forEach(function(item) {
                        if (counter < 4) {
                            container.appendChild(eventcard(item));
                        }
                        counter++;
                    });
                })
            },
            minLength: 1,
        });
    });

    $.getJSON('static/eventfulcities.json', function(datares) {
        var countryful = {};
        datares.forEach(function(item) {
            countryful[item] = "";
        });
        $("#countryful").autocomplete({
            data: countryful,
            limit: 5,
            onAutocomplete: function(val) {
                var citiesful = [];
                $.getJSON('graphql?query=%7B%0A%09countries(name%3A%22' + val + '%22)%7B%0A%20%20%20%20cities%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D', function(cities) {
                    cities["data"]["countries"][0]["cities"].forEach(function(item) {
                        citiesful[item["name"]] = "";
                    });
                    $("#cityful").autocomplete({
                        data: citiesful,
                        limit: 5,
                        onAutocomplete: function(val) {
                            $("#fulsearch").removeClass("hidden");

                        },
                        minLength: 1,
                    });

                });
            },
            minLength: 1,
        });
    });
    $("#fulsearch").click(function(event) {
        event.preventDefault();
        if (($("#cityful").val().length > 0) && ($("#countryful").val().length > 0) && ($("#searchful").val().length > 3)) {
            $.getJSON('graphql?query=%7B%0A%09cities(name%3A"' + encodeURIComponent($("#cityful").val()) + '")%7B%0A%20%20%20%20eventful(search%3A%20"' + encodeURIComponent($("#searchful").val()) + '")%7B%0A%20%20%20%20%20%20title%0A%20%20%20%20%20%20description%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D', function(ful) {
                var container = document.getElementById('eventfulresponses');
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                var counter = 0;
                if (ful["data"]["cities"][0]["eventful"] != null) {
                    ful["data"]["cities"][0]["eventful"].forEach(function(item) {
                        if (counter < 4) {
                            container.appendChild(eventcard(item));
                        }
                        counter++;
                    });
                } else {
                    container.appendChild(eventcard({
                        "title": "No Events",
                        "description": "In eventful api for: " + $("#cityful").val()
                    }));
                }
            });
        }
    });

    $.getJSON('graphql?query=%7B%0A%0A%20%20%20%20countries(name%3A%20%22New%20Zealand%22)%7B%0A%20%20%20%20%09cities%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%09%0A%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%09%0A%20%20%20%20%7D%0A%0A%7D', function(data) {
        var nzcities = {};
        data["data"]["countries"][0]["cities"].forEach(function(item) {
            nzcities[item["name"]] = "";
        });
        $('#nzcity').autocomplete({
            data: nzcities,
            limit: 5, // The max amount of results that can be shown at once. Default: Infinity.
            onAutocomplete: function(val) {
                $.getJSON('graphql?query=%7B%0A%20%20countries(name%3A%20%22New%20Zealand%22)%20%7B%0A%20%20%20%20cities(name%3A%20%22' + encodeURIComponent(val) + '%22)%20%7B%0A%20%20%20%20%20%20events%20%7B%0A%20%20%20%20%20%20%20%20category%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A', function(cdata) {
                    var currentCategories = {}
                    cdata["data"]["countries"][0]["cities"][0]["events"].forEach(function(item) {
                        currentCategories[item["category"]] = "";
                    });
                    $('#nzcategory').autocomplete({
                        data: currentCategories,
                        limit: 5,
                        minLength: 1,
                        onAutocomplete: function(val2) {
                            var container = document.getElementById('eventfindaresponses');
                            while (container.firstChild) {
                                container.removeChild(container.firstChild);
                            }
                            $.getJSON("graphql?query=%7B%0A%20%20countries(name%3A%20%22New%20Zealand%22)%20%7B%0A%20%20%20%20cities(name%3A%20%22" + encodeURIComponent(val) + "%22)%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20events(category%3A%22" + encodeURIComponent(val2) + "%22)%7B%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20location%0A%20%20%20%20%20%20%20%20description%0A%20%20%20%20%20%20%20%20date%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A", function(rdata) {
                                var counter = 0;
                                rdata["data"]["countries"][0]["cities"][0]["events"].forEach(function(item) {
                                    if (counter < 4) {
                                        container.appendChild(eventcard(item));
                                    }
                                    counter++;
                                });
                            })
                        },
                    });
                });
            },
            minLength: 1, // The minimum length of the input for the autocomplete to start. Default: 1.
        });

    });
    $.getJSON('static/places.json', function(places) {
        var allPlaces = {};
        places.forEach(function(item) {
            allPlaces[item] = "";
        });
        $("#placetype").autocomplete({
            data: allPlaces,
            limit: 5,
            onAutocomplete: function(val) {},
            minLength: 1,
        });
    });
    var countries = {
        "United States of America": "",
        "New Zealand": "",
        "Australia": "",
        "Japan": ""
    };
    $("#aircountry").autocomplete({
        data: countries,
        limit: 5,
        onAutocomplete: function(val) {

            $.getJSON('graphql?query=%7B%0A%20%20countries(name%3A%20%22'+encodeURIComponent(val)+'%22)%7B%0A%20%20%20%20cities%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20airports%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%7D%7D', function(data){
                    var citiesWithAirport = {};
                    data["data"]["countries"][0]["cities"].forEach(function(item){
                        if( item["airports"].length > 0){
                            if (item["name"] in citiesWithAirport){

                            }else{
                                citiesWithAirport[item["name"]] =""
                            }
                        }

                    });
                    $("#aircity").autocomplete({
                        data: citiesWithAirport,
                        limit: 5,
                        onAutocomplete: function(val2){
                            var container = document.getElementById('airportresponses');
                            while (container.firstChild) {
                                container.removeChild(container.firstChild);
                            }

                            $.getJSON('graphql?query=%7B%0A%09cities(name%3A"'+val2+'")%7B%0A%20%20%20%20airports%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20iata%0A%20%20%20%20%20%20airnzdestination%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D', function(airdata){
                                var counter = 0;
                                airdata["data"]["cities"][0]["airports"].forEach(function(item){
                                    if (counter < 4) {
                                        container.appendChild(airportcard(item));
                                    }
                                    counter++;
                                });
                                if (counter == 0){
                                        container.appendChild(airportcard({"name": "No Airport", "iata":" in "+val2, "airnzdestination": false}));
                                }
                            })
                        },
                        minLength: 1,
                    })
            })
        },
        minLength: 1,
    });
    $("#placesearch").click(function(event) {
        event.preventDefault();
        if (($("#meters").val().length > 0) && ($("#placetype").val().length > 0) && ($("#latitude").val().length > 6) && ($("#longitude").val().length > 6)) {
            var container = document.getElementById('googleplacesresponse');
            while (container.firstChild) {
                container.removeChild(container.firstChild);
            }
            $.getJSON('graphql?query=%7B%0A%20%20where(latlng%3A%20%7Blatitude%3A%20' + $("#latitude").val() + '%2C%20longitude%3A%20' + $("#longitude").val() + '%7D)%7B%0A%20%20%20%20places(radius%3A%20' + $("#meters").val() + '%2C%20category%3A%20%22' + $("#placetype").val() + '%22)%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20isopen%0A%20%20%20%20%20%20rating%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D', function(res) {
                var counter = 0;
                res['data']['where']['places'].forEach(function(item) {
                    if (counter < 4) {
                        container.appendChild(placecard(item));
                    }
                    counter++;
                });
            });
        }
    });
    $("#location").click(function(event) {
        event.preventDefault();
        if (($("#meters").val().length > 0) && ($("#placetype").val().length > 0)) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var container = document.getElementById('googleplacesresponse');
                while (container.firstChild) {
                    container.removeChild(container.firstChild);
                }
                $.getJSON('graphql?query=%7B%0A%20%20where(latlng%3A%20%7Blatitude%3A%20' + position.coords.latitude + '%2C%20longitude%3A%20' + position.coords.longitude + '%7D)%7B%0A%20%20%20%20places(radius%3A%20' + $("#meters").val() + '%2C%20category%3A%20%22' + $("#placetype").val() + '%22)%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20isopen%0A%20%20%20%20%20%20rating%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D', function(res) {
                    var counter = 0;
                    res['data']['where']['places'].forEach(function(item) {
                        if (counter < 4) {
                            container.appendChild(placecard(item));
                        }
                        counter++;
                    });
                });

            });
        }
    });
});

function eventcard(event) {
    var divSize = document.createElement('div');
    divSize.classList.add("col");
    divSize.classList.add("m3");
    divSize.classList.add("s6");
    var card = document.createElement('div');
    card.classList.add("card");
    card.classList.add("blue-grey");
    card.classList.add("darken-1");
    var content = document.createElement('div');
    content.classList.add("card-content");
    content.classList.add("white-text");
    var title = document.createElement('span');
    title.classList.add("card-title");
    title.innerHTML = event['title'];
    var body = document.createElement('p');
    if (event['description'] != null) {
        if (event['description'].length > 150) {
            body.innerHTML = event['description'].substring(0, 150) + "...";
        } else {
            body.innerHTML = event['description'];
        }
    }
    content.appendChild(title);
    content.appendChild(body);
    card.appendChild(content);
    divSize.appendChild(card);
    return divSize;
}

function airportcard(airport) {
    var divSize = document.createElement('div');
    divSize.classList.add("col");
    divSize.classList.add("m3");
    divSize.classList.add("s6");
    var card = document.createElement('div');
    card.classList.add("card");
    card.classList.add("blue-grey");
    card.classList.add("darken-1");
    var content = document.createElement('div');
    content.classList.add("card-content");
    content.classList.add("white-text");
    var title = document.createElement('span');
    // title.classList.add("card-title");
    title.innerHTML = airport['name']+"("+airport["iata"]+")";
    var body = document.createElement('p');
    var open = "";
    if (airport['airnzdestination']){
        open += '<i class="material-icons">airplanemode_active</i>';
    }
    body.innerHTML = open;
    content.appendChild(title);
    content.appendChild(body);
    card.appendChild(content);
    divSize.appendChild(card);
    return divSize;
}

function placecard(place) {
    var divSize = document.createElement('div');
    divSize.classList.add("col");
    divSize.classList.add("m3");
    divSize.classList.add("s6");
    var card = document.createElement('div');
    card.classList.add("card");
    card.classList.add("blue-grey");
    card.classList.add("darken-1");
    var content = document.createElement('div');
    content.classList.add("card-content");
    content.classList.add("white-text");
    var title = document.createElement('span');
    title.classList.add("card-title");
    title.innerHTML = place['name'];
    var body = document.createElement('p');
    var open = "";
    if (place['isopen']) {
        open += "Open";
    } else if (place['isopen'] == null) {

    } else {
        open += "Closed";
    }
    if (place['rating']) {
        open += "<br/>Rated: " + place['rating'] + " stars.";
    }
    body.innerHTML = open;
    content.appendChild(title);
    content.appendChild(body);
    card.appendChild(content);
    divSize.appendChild(card);
    return divSize;
}
