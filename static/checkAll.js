


$('#check-all').click(function(event) {   
    if(this.checked) {
        $(':checkbox').each(function() {
            this.checked = true;                        
        });
    } else {
        $(':checkbox').each(function() {
            this.checked = false;                       
        });
    }
});

$('#submit-similar').click(function(event) {
    var similarCheckboxes = $('input[name="virals"]');
    simVirals = {};
    
    similarCheckboxes.each(function(){
        simVirals[$(this).attr("id")] = this.checked;
    });
    
    //$.each(simVirals,function(k,v){
    //    alert(k+ " " +v);
    //})
    //serializedSimVirals = JSON.stringify(similarCheckboxes);

    var postURL = window.location.pathname;

    $.ajax({
        url: postURL,
        type: 'POST',
        data: simVirals,
        succes: function(response) {
            alert(response)
        }
        //contentType = "application/json",
        //dataType = "json",
        //async = false,
        //cache = false
    });


});


/*
var mainWords = []

$(function()  {
    

});
*/


$('.snippetText').each(function () {
    var mainWords = $('#mainText').text().split(" ")
    spans = []
    txt = $('#' + this.id).text();
    words = txt.split(" ");
    for(var x = 0; x < words.length; x++){
        if(mainWords.indexOf(words[x]) >= 0){
            var span = "<span style='background-color: lightgreen;'>" + words[x] + "</span>"
        } else {
            var span = "<span>" + words[x] + "</span>"
        }
        spans.push(span);
    }

    $('#' + this.id).html(spans.join(" "));

});