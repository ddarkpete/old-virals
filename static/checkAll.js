var mainNgrams = []
var textNgrams = []

function chunkIt(str,chunk) {
    var words = str.split(" ");
    var arr = [];
    for (var i = (chunk - 1); i < words.length; i++) {
      var start = i - (chunk - 1);
      arr.push(words.slice(start, start + chunk));
    }
    return arr.map(v => v.join(" "));
  }
  
  


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
    txt = $('#' + this.id).text()
    words = txt.split(" ");
    for(var x = 0; x < words.length; x++){
        if(words[x]=='//'){
            words[x] = '<br>'
        }
    }

    $('#' + this.id).html(words.join(" "));
});

$('#mainText').each(function () {
    txt = $('#mainText').text()
    words = txt.split(" ");
    for(var x = 0; x < words.length; x++){
        if(words[x]=='//'){
            words[x] = '<br>'
        }
    }

    $('#mainText').html(words.join(" "));
});

$('.snippetText').first(function () {
    txt = $('#' + this.id).text();
    textNgrams = chunkIt($('#' + this.id).text(),4);
    console.log(mainNgrams);
});

$('#mainText').first(function() {
    mainNgrams = chunkIt(this.text(),4);

});


$('.snippetText').each(function () {
    var mainWords = $('#mainText').text().split(" ")
    var mainGrams = [];
    //for()
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

$('.s')

$('.mainSnippet').each(function () {
    var txt= $('#' + this.id).text();
    if(txt.length > 155)
        txt = txt.substring(0,500) + '.....';
    $('#' + this.id).html(txt);
});

$('#methodSelect').change(function(){
    var item = $(this).val();

    if (item == "N-grams")
    {
        window.location.href = '/ngrams'
    } else if (item === "Shingling")
    {
        window.location.href = '/shingling'
    } else if (item === "All")
    {
        window.location.href = '/all'
    }
    else if (item === "TFIDF")
    {
        window.location.href = '/tfidf'
    }
});