($(function() {

    var catjson;
    var myCategories;
    var json;
    var myMerch;

    $.ajax({type:"POST",url: "/GetCategories",success:function(data) {
      console.log(data);
      catjson = JSON.parse(data);
      myCategories = catjson.currentCategories;
      console.log(myCategories.length);

      if(myCategories.length > 0) {
        console.log("Entering category for loop");
        for(var i=0; i<myCategories.length; i++) {
          console.log('mycat i: ' + myCategories[i]);
          var categoryName = myCategories[i].name;
          console.log('mycat i name: ' + categoryName);

          $(document).ready(function () {
            $('#catlist').append('<a href="#" id="' + myCategories[i].name + '" onclick="return false;" class="list-group-item">'+ myCategories[i].name + '</a>');
          });
        }
      }
    }});

    $.ajax({url: "/GetMerch",success:function(data) {
        console.log(data);
        json = JSON.parse(data);
        myMerch = json.myMerch;
        console.log(myMerch.length);


        if(myMerch.length == 0) {
          $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
          $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="Merchandise coming soon..." alt=""></div>');
        }


        for( var i=0; i < myMerch.length; i++) {
            console.log('mymerch i: ' + myMerch[i]);
            var productDescription = myMerch[i].productDescription;
            var productPrice = Number(myMerch[i].productPrice).toFixed(2);;
            var imageurl = myMerch[i].imageurl;
            var productName = myMerch[i].productName;
            var rowcount = 0;
            var rowstring = '"#merch' + rowcount + '"';

            $(document).ready(function () {
                if(i == 0) {
                  $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="' + i +'" class="active"></li>');
                  $('#articleslides').prepend('<div class="item active" ><img class="slide-image" src="' + imageurl + '" alt="" height="400" width="400"></div>');
                } else {
                  $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="' + i + '"></li>');
                  $('#articleslides').prepend('<div class="item" ><img class="slide-image" src="' + imageurl +'" alt="" height="400" width="400"></div>');
                }
                $("#merch0").prepend('<div class="col-sm-5 col-lg-5 col-md-5"><div class="thumbnail"><img src="' + imageurl + '" alt=""><div class="caption"><h4 class="pull-right">$' + productPrice + '</h4><h4><a href="#">' + productName + '</a></h4><p>' + productDescription + '</p></div></div></div>');

            });
        }
    }});

$(document).ready(function() {
  $('#All').click( function() {
    $('#merch0').empty();  
    $('#articleslideshow').empty();
    $('#articleslides').empty();

    if(myMerch.length == 0) {
      $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
      $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="Merchandise coming soon..." alt=""></div>');
    }


    for( var i=0; i < myMerch.length; i++) {
        console.log('mymerch i: ' + myMerch[i]);
        var productDescription = myMerch[i].productDescription;
        var productPrice = Number(myMerch[i].productPrice).toFixed(2);;
        var imageurl = myMerch[i].imageurl;
        var productName = myMerch[i].productName;
        var rowcount = 0;
        var rowstring = '"#merch' + rowcount + '"';

        $(document).ready(function () {
            if(i == 0) {
              $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="' + i +'" class="active"></li>');
              $('#articleslides').prepend('<div class="item active" ><img class="slide-image" src="' + imageurl + '" alt="" height="400" width="400"></div>');
            } else {
              $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="' + i + '"></li>');
              $('#articleslides').prepend('<div class="item" ><img class="slide-image" src="' + imageurl +'" alt="" height="400" width="400"></div>');
            }
            $("#merch0").prepend('<div class="col-sm-5 col-lg-5 col-md-5"><div class="thumbnail"><img src="' + imageurl + '" alt=""><div class="caption"><h4 class="pull-right">$' + productPrice + '</h4><h4><a href="#">' + productName + '</a></h4><p>' + productDescription + '</p></div></div></div>');

        });
    }
  });
});

$(document).delegate('#Coats', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Dresses', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Gloves', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Hats', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Pants', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myPants = [];

  for (i=0; i<myMerch.length;i++) {
    console.log("reducing to only pants. My merch[" + i + "] is " + myMerch[i].productType);
    if(myMerch[i].productType == "Pants") {
      console.log('found a pants');
      myPants.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myPants.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="Merchandise coming soon..." alt=""></div>');
  }


  for( var i=0; i < myPants.length; i++) {
      console.log('mymerch i: ' + myPants[i]);
      var productDescription = myPants[i].productDescription;
      var productPrice = Number(myPants[i].productPrice).toFixed(2);;
      var imageurl = myPants[i].imageurl;
      var productName = myPants[i].productName;
      var rowcount = 0;
      var rowstring = '"#merch' + rowcount + '"';

      $(document).ready(function () {
          if(i == 0) {
            $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="' + i +'" class="active"></li>');
            $('#articleslides').prepend('<div class="item active" ><img class="slide-image" src="' + imageurl + '" alt="" height="400" width="400"></div>');
          } else {
            $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="' + i + '"></li>');
            $('#articleslides').prepend('<div class="item" ><img class="slide-image" src="' + imageurl +'" alt="" height="400" width="400"></div>');
          }
          $("#merch0").prepend('<div class="col-sm-5 col-lg-5 col-md-5"><div class="thumbnail"><img src="' + imageurl + '" alt=""><div class="caption"><h4 class="pull-right">$' + productPrice + '</h4><h4><a href="#">' + productName + '</a></h4><p>' + productDescription + '</p></div></div></div>');

      });
  }
});

$(document).delegate('#Scarves', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Shirts', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Shoes', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Shorts', 'click', function()
{
  console.log('Shorts clicked');
});

$(document).delegate('#Skirts', 'click', function()
{
  console.log('coats clicked');
});

$(document).delegate('#Sweaters', 'click', function()
{
  console.log('Sweaters clicked');
});
  
} (jQuery)));



 