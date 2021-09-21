
$(document).ready(function(){
    $(".confirm_delete").click(function(){
        return confirm('Are you sure you want to cancel this appointment?');
    });
});

$(document).ready(function(){
    $(".comment-confirm-delete").click(function(){
        return confirm('Are you sure you want to cancel this comment?');
    });
});
$(document).ready(function(){
    $(".hide").hide()

});

$(document).ready(function(){
    $("td").click(function(e){
        $(e.target).find("button").click();
    });
});