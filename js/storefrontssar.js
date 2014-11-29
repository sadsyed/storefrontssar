($(function() {

    var catjson;
    var myCategories;
    var json;
    var myMerch;

    $.ajax({type:"POST",url: "/GetSaleCategories",success:function(data) {
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
      $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
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
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Coats") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Dresses', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Dresses") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Gloves', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Gloves") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Hats', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Hats") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Pants', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    console.log("reducing to only pants. My merch[" + i + "] is " + myMerch[i].productType);
    if(myMerch[i].productType == "Pants") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Scarves") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Shirts', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Shirts") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Shoes', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Shoes") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Shorts', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Shorts") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    console.log("myMerch equals zero.")
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    console.log("myMerch equals zero.")
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
    console.log("myMerch equals zero.")
  }

  console.log("before for loop.")
  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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
  console.log("after for loop.")
});

$(document).delegate('#Skirts', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Skirts") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt="">Merchendise Coming Soon!</div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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

$(document).delegate('#Sweaters', 'click', function()
{
  $('#merch0').empty();
  $('#articleslideshow').empty();
  $('#articleslides').empty();

  var myArticle = [];

  for (i=0; i<myMerch.length;i++) {
    if(myMerch[i].productType == "Sweaters") {
      myArticle.push(myMerch[i]);
    }
  }
  //loop through merch and find only pants
  if(myArticle.length == 0) {
    $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
    $('#articleslides').prepend('<div class="item active"><img class="slide-image" src="http://lh6.ggpht.com/VtzdDTxA6x5tVRGQDelP9B06vNcIx1O5NYYWzHGUxTirHrsgQxuC-VgDLAxpNMb7xwgGowSlSRxY25VhbH4KCVc8rxw" alt=""></div>');
  }


  for( var i=0; i < myArticle.length; i++) {
      console.log('mymerch i: ' + myArticle[i]);
      var productDescription = myArticle[i].productDescription;
      var productPrice = Number(myArticle[i].productPrice).toFixed(2);;
      var imageurl = myArticle[i].imageurl;
      var productName = myArticle[i].productName;
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
  
} (jQuery)));



 