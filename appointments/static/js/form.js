function validButton(button, disabled){
    button.attr("disabled", disabled);
}

var createAlert;
var createComment;
var editAppoint;
var emailSent;
var updateEmailSent;
var gratitudeEmail;

var lang = document.getElementById('lang')
if (lang.text == '"he"'){
    createAlert = 'פגישה נוצרה'
    createComment = 'תגובה נוצרה'
    editAppoint = 'השינויים נשמרו בהצלחה'
    emailSent = 'מייל נשלח'
    updateEmailSent = 'נשלחה הודעת עדכון למשתמש'
    gratitudeEmail = 'תודה שיצרת קשר נשוב עליך בהקדם האפשרי'
}else{
    createAlert = 'created an appointment.'
    createComment = 'created a comment.'
    editAppoint = 'appointment edited successfully.'
    emailSent = 'email sent'
    updateEmailSent = 'update email sent'
    gratitudeEmail = 'thank you for sending an email, we will get back to you as soon as possible'
}


// $(document).ready(function(){
//     var formLi = $('form li')
//     for (let i = 0; i < formLi.length; i++){
//         formLi[i].classList.add('alert', 'alert-success')
//     }
// });

$("#appoint-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();

    var button = $($(this).children('.modal-footer').children(':button')[0])
    validButton(button, true)
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.

            $("#appoint-form").trigger('reset');
            // 2. focus to nickname input 
            alert(createAlert)

            location.reload(true);
            // display the newly friend to table.
        },
        error: function (response) {
            validButton(button, false)
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#appoint-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);
        }
    })
});

$("#comment-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    var button = $($(this).children('.modal-footer').children(':button')[0])
    validButton(button, true)
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            alert(createComment)

            location.reload(true)
            $("#comment-form").trigger('reset');

        },
        error: function (response) {
            validButton(button, false)
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#comment-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);

        }
    })
});

$("#edit-appoint-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    var button = $($(this).children('.modal-footer').children(':button')[0])
    validButton(button, true)
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            $(this).trigger('reset');
            // 2. focus to nickname input 
            alert(editAppoint)
            location.reload(true)
            // display the newly friend to table.
        },
        error: function (response) {
            validButton(button, false)
            // alert the error if any error occured
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#edit-appoint-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);
        }
    })
});

$("#edit-appoint-res-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();

    var button = $($(this).children('.modal-footer').children(':button')[0])
    validButton(button, true)

    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            
            $(this).trigger('reset');
            // 2. focus to nickname input 
            alert(editAppoint)

            location.reload(true);
            // display the newly friend to table.
        },
        error: function (response) {
            // alert the error if any error occured
            validButton(button, false)
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#edit-appoint-res-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);
        }
    })
});



$("#contact-form-therapist").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var button = $($(this).children('.modal-footer').children(':button')[0])
    validButton(button, true)

    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            alert(emailSent)
            location.reload(true)
        },
        error: function (response) {
            
            validButton(button, false)
            // alert the error if any error occured
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#contact-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);
        }
    })

});

$("#update-appoint-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();

    var button = $($(this).children('.modal-footer').children(':button')[0])
    validButton(button, true)
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            
            $(this).trigger('reset');
            // 2. focus to nickname input 
            // display the newly friend to table.
            // alert('sent email')
            alert(updateEmailSent)

            location.reload(true)
        },
        error: function (response) {
            // alert the error if any error occured
            validButton(button, false)
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#update-appoint-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);

        }
    })

});

$("#working-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            
            $(this).trigger('reset');
            // 2. focus to nickname input 
            // display the newly friend to table.
            // alert('sent email')
            location.reload(true)
        },
        error: function (response) {
            // alert the error if any error occured
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#working-form-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);

        }
    })

});

$("#date-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,
        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            
            $(this).trigger('reset');
            // 2. focus to nickname input 
            // display the newly friend to table.
            // alert('sent email')
            location.reload(true)
        },
        error: function (response) {
            // alert the error if any error occured
            var x = Object.values(response.responseJSON.error)[0][0]
            $('#date-form-result').html(`<div class="alert alert-danger" role="alert"> ${x} </div>`);

        }
    })

});

$("#contact-form-home").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    var button = $('#send-btn')
    // validButton(button, true)
    // serialize the data for sending the form data.
    var serializedData = $(this).serialize();
    // make POST ajax call
    console.log($(this).attr('action'),)

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: serializedData,

        success: function (response) {
            // on successfull creating object
            // 1. clear the form.
            
            $(this).trigger('reset');
            alert(gratitudeEmail)
            location.reload(true)
        },
        error: function (response) {
            // alert the error if any error occured
            validButton(button, false)
            alert('error')
        }
    })

});

$('a[name="accept"]').on('click',function(){
    $(this).hide()
});

$('#box').click(function(){
    if(this.checked){
    $("#id_password").attr("type", "text");
    $("#id_password1").attr("type", "text");
    $("#id_password2").attr("type", "text");
    $("#id_old_password").attr("type", "text");
    $("#id_new_password1").attr("type", "text");
    $("#id_new_password2").attr("type", "text");
    }else{
        $("#id_password").attr("type", "password");
        $("#id_password1").attr("type", "password");
        $("#id_password2").attr("type", "password");
        $("#id_old_password").attr("type", "password");
        $("#id_new_password1").attr("type", "password");
        $("#id_new_password2").attr("type", "password");
    }
});



