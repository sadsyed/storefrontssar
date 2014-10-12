($(function() { 

    $.ajax({url: "/GetMerch",success:function(data) {
        console.log(data)
        var json = JSON.parse(data);
        var myMerch = json.myMerch;
        console.log(myMerch.length);

        for( var i=0; i < myMerch.length; i++) {
            console.log('mymerch i: ' + myMerch[i]);
            var productDescription = myMerch[i].productDescription;
            var productPrice = myMerch[i].productPrice;
            var imageurl = myMerch[i].imageurl;
            var productName = myMerch[i].productName;
            $(document).ready(function () {
                $("#merch").prepend('<div class="col-sm-4 col-lg-4 col-md-4"><div class="thumbnail"><img src="' + imageurl + '" alt=""><div class="caption"><h4 class="pull-right">$' + productPrice + '</h4><h4><a href="#">' + productName + '</a></h4><p>' + productDescription + '</p></div></div></div>');
            });
        }
    }});

} (jQuery)));



