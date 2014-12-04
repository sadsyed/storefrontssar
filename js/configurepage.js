($(function() {

    var json;
    var myMerch;


    $.ajax({url: "/GetAccountSettings",success:function(data) {
        console.log(data);


    }});

    $.ajax({url: "/ConfigureCategories",success:function(data) {
        console.log(data);
        json = JSON.parse(data);
        myMerch = json.myMerch;
        console.log(myMerch.length);

        $('#Title2').show();
        $('#configaccount').show();
        $('#Title2').show();
        $('#Title3').show();
        $('#configaccount').show();

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
                $("#merch0").prepend('<div class="col-sm-5 col-lg-5 col-md-5"><div class="thumbnail"><img src="' + imageurl + '" alt=""><div class="caption"><h4 class="pull-right">$' + productPrice + '</h4><h4><a href="#" id="' + productDescription + '" class="callarticle" name="' + productName + '" click="return false;">' + productName + '</a></h4><p>' + productDescription + '</p></div></div></div>');

            });
        }
    }});

$(document).delegate('.callarticle', 'click', function()
{
    var thisItem = this.name;
    console.log("The id is: " + this.name);
    var jsonData = {articleName: this.name};
    $.ajax({type:"POST", dataType: "json", url: "/GetArticleInfo", success:function(returndata) {
      console.log("Got success: " + returndata);

      var name = returndata.articleName;
      var lastUsed = returndata.articleLastUsed;
      var articlePrice = parseFloat(returndata.articlePrice);
      articlePrice = articlePrice.toFixed(2);
      var articleId = returndata.articleId;
      var articleDescription = returndata.articleDescription;
      var articleImageUrl = returndata.articleImageUrl;
      var articleTimesUsed = returndata.articleTimesUsed;
      var articleOkToSell =returndata.articleOkToSell;
      console.log('OK to sell: ' + articleOkToSell);
      var articleTags = returndata.articleTags;

      $('#merch0').empty();  
      $('#articleslideshow').empty();
      $('#articleslides').empty();

      $('#Title2').hide();
      $('#Title3').hide();
      $('#configaccount').hide();
      //$('#articleslideshow').hide();
      //$('#articleslides').hide();
      //$('carousel-example-generic').hide();

      $('#articleslideshow').append('<li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>');
      $('#articleslides').prepend('<div class="item active" ><img class="slide-image" src="' + articleImageUrl + '" alt="" height="400" width="400"></div>');
      $('#merch0').append('<b>Article Name:   </b><label id="articleName" padding-left:5em> ' + name + '</label><BR>');
      $('#merch0').append('<b>Article Id:   </b><label id="articleId" value="' + articleId + '" padding-left:5em>' + articleId +'</label><BR>');
      $('#merch0').append('<b>Article Last Used:   </b><br><INPUT type="text" id="articleLastUsed" name="articleLastUsed" value="' + lastUsed +'" padding-left:5em><BR>');
      $('#merch0').append('<b>Article Price:   </b><br><INPUT type="text" id="articlePrice" name="articlePrice" value="' + articlePrice +'" padding-left:5em><BR>');
      $('#merch0').append('<b>Article Description:   </b><br><INPUT type="text" id="articleDescription" name="articleDescription" value="' + articleDescription +'" padding-left:5em><BR>');
      $('#merch0').append('<b>Article Times Used:   </b><br><INPUT type="text" id="articleTimesUsed" name="articleTimesUsed" value="' + articleTimesUsed +'" padding-left:5em><BR>');
      $('#merch0').append('<b>Article Tags:   </b><br><INPUT type="text" id="articleTags" name="articleTags" value="' + articleTags[0] +'" padding-left:5em><br>');
      if (articleOkToSell == true) {
        $('#merch0').append('<b><input type="checkbox" id="articleOkToSell" name="articleOkToSell" checked> Article Ok To Sell</b><br>');
        $('#articleOkToSell').prop('checked', true);
      } else {
        $('#merch0').append('<b><input type="checkbox" id="articleOkToSell" name="articleOkToSell"> Article Ok To Sell</b><br>');
        $('#articleOkToSell').prop('checked', false);
      }
      $('#merch0').append('<b><input type="checkbox" id="articleDelete" name="articleDelete" value="uc"> Delete Article </b><br>');
      $('#merch0').append('<a class="btn btn-success" id="' + name + '"" href="#" onclick="return false;">Update Item</a></p>');

    }, error: function(jqXHR, textStatus, errorThrown) {
      console.log("There was an error.")
    }, data: jsonData });
});

$(document).delegate('.btn-success', 'click', function()
{
    var articleid = $('#articleId').attr('value');
    console.log('articleId is: ' + articleid);
    if ($('#articleDelete').prop('checked') == true) {
      articledelete = true;
      console.log('Delete article: ' + articleid)
      var jsonData = {articleidstodelete: articleid};
      console.log('JSon sending to update article is: ' + jsonData);
      $.ajax({type:"POST", dataType: "json", url: "/DeleteArticle", success:function(returndata) {
        console.log("Deleted article");
        window.location ="https://storefrontssar2.appspot.com/authenticated"
      }, error: function(jqXHR, textStatus, errorThrown) {
        console.log("There was an error.")
      }, data: jsonData });
    } else {
      var lastused = $('#articleLastUsed').val();
      var articleprice = $('#articlePrice').val();
      var articledescription = $('#articleDescription').val();
      var articletimesused = $('#articleTimesUsed').val();
      var articleoktosell;
      var articledelete;
      if ($('#articleOkToSell').prop('checked') == true)  {
        articleoktosell = true;
      } else {
        articleoktosell = false;
      }
      console.log('OK to sell value is: ' + articleoktosell);
      var temp = $('#articleTags').val();
      console.log('temp is: ' + temp);
      var articletags = temp;
      console.log('articletags is: ' + articletags);

      var jsonData = {articleId: articleid,append:'false', articleLastUsed:lastused, articleTags: articletags, articleDescription:articledescription, articleOkToSell:articleoktosell, articleDelete:articledelete, articlePrice:articleprice, articleDelete:articledelete};
      console.log('JSon sending to update article is: ' + jsonData);
      $.ajax({type:"POST", dataType: "json", url: "/UpdateArticle", success:function(returndata) {
        console.log("Sent price");
        window.location ="https://storefrontssar2.appspot.com/authenticated"
      }, error: function(jqXHR, textStatus, errorThrown) {
        console.log("There was an error.")
      }, data: jsonData });
    }


});  
 
} (jQuery)));



 