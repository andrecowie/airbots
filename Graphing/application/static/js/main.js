$(document).ready(function(){
  console.log("Ready!");
	$.getJSON('graphql?query=%7B%0A%0A%20%20%20%20countries(name%3A%20%22New%20Zealand%22)%7B%0A%20%20%20%20%09cities%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%09%0A%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%09%0A%20%20%20%20%7D%0A%0A%7D', function(data){
    var nzcities = {};
    data["data"]["countries"][0]["cities"].forEach(function(item){
      nzcities[item["name"]] = "";
    });
    $('#nzcity').autocomplete({
      data: nzcities,
    limit: 20, // The max amount of results that can be shown at once. Default: Infinity.
    onAutocomplete: function(val) {
        $.getJSON('graphql?query=%7B%0A%20%20countries(name%3A%20%22New%20Zealand%22)%20%7B%0A%20%20%20%20cities(name%3A%20%22'+val+'%22)%20%7B%0A%20%20%20%20%20%20events%20%7B%0A%20%20%20%20%20%20%20%20category%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A', function(cdata){
          var currentCategories = {}
          cdata["data"]["countries"][0]["cities"][0]["events"].forEach(function(item){
            console.log(item["category"]);
            currentCategories[item["category"]] = "";
          });
          $('#nzcategory').autocomplete({
            data: currentCategories,
            limit: 20,
            minLength: 1,
            onAutocomplete: function(val2){
              //Do graphql query with val and val2
            },
          });
        });
    },
    minLength: 2, // The minimum length of the input for the autocomplete to start. Default: 1.
    });

  });
})
