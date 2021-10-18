var deleteAppoint;
var deleteComment;

var lang = document.getElementById('lang')
if (lang.text == '"he"'){
  deleteAppoint = 'את בטוחה שאת רוצה לבטל את הפגישה הזאת?'
  deleteComment = 'את בטוחה שאת רוצה לבטל את התגובה הזאת?'
}else{
  deleteAppoint = 'Are you sure you want to cancel this appointment?'
  deleteComment = 'Are you sure you want to cancel this comment?'
}


$(document).ready(function(){
    $(".confirm_delete").click(function(){
        return confirm(deleteAppoint);
    });
});

$(document).ready(function(){
    $(".comment-confirm-delete").click(function(){
        return confirm(deleteComment);
    });
});

