var mainNgrams = []
var textNgrams = []


function ngrams(str,n) {
    //alert(type(str));
    var words = str.split(" ");
    var arr = [];
    for(var i = 0 ; i < words.length - n; i++ ){
        var temparr = []
        for(var j = i; j < i + n ; j++){
        temparr.push(words[j]);
        }
        arr.push(temparr);
    }

    return arr;
}

$('#check-all').click(function(event) {
    alert(mainNgrams);   
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




var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
//output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
//slider.oninput = function() {
//  output.innerHTML = this.value;
//}


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


mainText = "" 
textText = ""

$('#mainText').each(function() {
    mainText = $("#mainText").text();
});


$('.snippetText').each(function () {
    textText = $('#' + this.id).text();
});

function calcNgrams(n) {

    

   //
        xd= parseInt(n);
        
        mainNgrams = ngrams(mainText,xd);
        textNgrams = ngrams(textText,xd);
        
        
    //});



    $('.snippetText').each(function () {
        spans = []
        x = 0;
        while( x < textNgrams.length){
            if(JSON.stringify(mainNgrams).includes(JSON.stringify(textNgrams[x]))){
                 ngram = true;
                tempspan = [];
                textNgrams[x].forEach(element => {
                    tempspan.push(element)
                });
                z = x + 1;
                while(ngram){
                    if(JSON.stringify(mainNgrams).includes(JSON.stringify(textNgrams[z]))){
                        tempspan.push(textNgrams[z][textNgrams[z].length - 1]);
                        z+=1;
                    } else {
                        spans.push("<span style='background-color: lightgreen;'>" + tempspan.join(" ") + "</span>");
                        x = z + xd;
                        ngram = false;
                    }
                }
            } else {
                
                spans.push("<span>" + textNgrams[x][0] + "</span>");
                x+=1;
            }
        }
        $('#' + this.id).html(spans.join(" "));
    });

    $('#mainText').each(function() {
        spans = []
        x = 0;
        while( x < mainNgrams.length){
            if(JSON.stringify(textNgrams).includes(JSON.stringify(mainNgrams[x]))){
                ngram = true;
                tempspan = [];
                mainNgrams[x].forEach(element => {
                    tempspan.push(element)
                });
                z = x + 1;
                while(ngram){
                    if(JSON.stringify(textNgrams).includes(JSON.stringify(mainNgrams[z]))){
                        tempspan.push(mainNgrams[z][mainNgrams[z].length - 1]);
                        z+=1;
                    } else {
                        spans.push("<span style='background-color: lightgreen;'>" + tempspan.join(" ") + "</span>");
                        x = z + xd;
                        ngram = false;
                    }
                }
            } else {
                
                spans.push("<span>" + mainNgrams[x][0] + "</span>");
                x+=1;
            }
        }
        $('#' + this.id).html(spans.join(" "));
        $("#ngramslabel").html(n + "-grams");
    });
}

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