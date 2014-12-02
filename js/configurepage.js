($(function() {

    var json;
    var myMerch;


    $.ajax({url: "/ConfigureCategories",success:function(data) {
        console.log(data);
        json = JSON.parse(data);
        myMerch = json.myMerch;
        console.log(myMerch.length);


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
                $("#merch0").prepend('<div class="col-sm-5 col-lg-5 col-md-5"><div class="thumbnail"><img src="' + imageurl + '" alt=""><div class="caption"><h4 class="pull-right">$' + productPrice + '</h4><h4><a href="#" click="return false;">' + productName + '</a></h4><p>' + productDescription + '</p></div></div></div>');

            });
        }
    }});
 
} (jQuery)));



 