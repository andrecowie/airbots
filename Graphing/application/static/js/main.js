$(document).ready(function() {

    $.getJSON('graphql?query=%7B%0A%0A%20%20%20%20countries(name%3A%20%22New%20Zealand%22)%7B%0A%20%20%20%20%09cities%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%09%0A%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%09%0A%20%20%20%20%7D%0A%0A%7D', function(data) {
        var nzcities = {};
        data["data"]["countries"][0]["cities"].forEach(function(item) {
            nzcities[item["name"]] = "";
        });
        $('#nzcity').autocomplete({
            data: nzcities,
            limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
            onAutocomplete: function(val) {
                $.getJSON('graphql?query=%7B%0A%20%20countries(name%3A%20%22New%20Zealand%22)%20%7B%0A%20%20%20%20cities(name%3A%20%22' + val + '%22)%20%7B%0A%20%20%20%20%20%20events%20%7B%0A%20%20%20%20%20%20%20%20category%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A', function(cdata) {
                    var currentCategories = {}
                    cdata["data"]["countries"][0]["cities"][0]["events"].forEach(function(item) {
                        currentCategories[item["category"]] = "";
                    });
                    $('#nzcategory').autocomplete({
                        data: currentCategories,
                        limit: 20,
                        minLength: 1,
                        onAutocomplete: function(val2) {
                            var container = document.getElementById('eventfindaresponses');
                            while (container.firstChild) {
                                container.removeChild(container.firstChild);
                            }
                            $.getJSON("graphql?query=%7B%0A%20%20countries(name%3A%20%22New%20Zealand%22)%20%7B%0A%20%20%20%20cities(name%3A%20%22"+encodeURIComponent(val)+"%22)%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20events(category%3A%22"+encodeURIComponent(val2)+"%22)%7B%0A%20%20%20%20%20%20%20%20title%0A%20%20%20%20%20%20%20%20location%0A%20%20%20%20%20%20%20%20description%0A%20%20%20%20%20%20%20%20date%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A", function(rdata) {
                                console.log("got res");
                                rdata["data"]["countries"][0]["cities"][0]["events"].forEach(function(item){
                                    console.log(item);
                                    container.appendChild(eventcard(item));
                                });
                            })
                        },
                    });
                });
            },
            minLength: 2, // The minimum length of the input for the autocomplete to start. Default: 1.
        });

    });

})


function eventcard(event){
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
    var title= document.createElement('span');
    title.classList.add("card-title");
    title.innerHTML =event['title'];
    var body= document.createElement('p');
    body.innerHTML = event['description'];
    content.appendChild(title);
    content.appendChild(body);
    card.appendChild(content);
    divSize.appendChild(card);
    return divSize;
}
