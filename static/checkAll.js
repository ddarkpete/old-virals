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