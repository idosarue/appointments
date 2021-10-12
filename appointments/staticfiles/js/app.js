
function createValidDate(x){
    var newDate = x.split('-').reverse()
    if (newDate[1].length < 2){
        newDate[1] = 0 + newDate[1]
    }
    if (newDate[2].length < 2){
        newDate[2] = 0 + newDate[2] 
    }
    return newDate.join('-')
}

$(document).ready(function(){
    var uls = $('.list-group')
    var cards = $('.card')
    var lang = document.getElementById('lang')
    if (lang.text == '"he"'){
        for (let i =0; i<uls.length; i++){
            $(uls[i]).css('text-align', 'right')            
        }
        for (let i =0; i<cards.length; i++){
            if (!cards[i].classList.contains('card-contact')){
                console.log(cards[i].classList)
                $(cards[i]).css('text-align', 'right')            
            }
        }
    }

});

$(document).ready(function(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    var dateInputs = $("input[name='appointment_date']").not('#filter')
    for (let i = 0; i<dateInputs.length; i++){
        console.log(dateInputs[i])
        dateInputs[i].type = 'date'
        dateInputs[i].setAttribute('min', today);

    };


});

$(document).ready(function(){
    var screen = $(window).width();
    var noDates = $('.grid-item');
    var mobileDays = $('.week-day-name');
    var days = $('.day-name');
    if (screen <= 800){
        tables = $('table');
        for (let i = 0; i<tables.length; i++){
            tables[i].classList.add('table-responsive');
        }
        for (i = 0; i < noDates.length; i++) {
            if ($(noDates[i]).attr('id') == '--'){
                $(noDates[i]).hide();
            }
          }
        for (i = 0; i < mobileDays.length; i++) {
            $(days[i]).show();
          }
        for (i = 0; i < days.length; i++) {
            $(days[i]).hide();
          }
    }else{
        for (i = 0; i < mobileDays.length; i++) {
            $(mobileDays[i]).hide();
          } 

        for (i = 0; i < days.length; i++) {
            $(days[i]).show();
        }
    }

});


$(document).ready(function(){
    $('.hide').hide()
    $('.hide2').hide()
    var inputs = document.querySelectorAll('input')
    var selects = document.querySelectorAll('select')
    var textareas = document.querySelectorAll('textarea')
    var tds = $('.calendar').children().not('.table-danger')
    var navLis = $('nav li')
    for (i = 0; i < navLis.length; i++) {
        navLis[i].classList.add('active')
      }
    for (i = 0; i < inputs.length; i++) {
        if (inputs[i].type == 'submit'){
            inputs[i].setAttribute('class','form-control btn btn-primary')
        }else{
            inputs[i].setAttribute('class','form-control')
            inputs[i].setAttribute('autocomplete','off')
        }
      }
    for (i = 0; i < selects.length; i++) {
        selects[i].setAttribute('class','form-control')
      }
    for (i = 0; i < textareas.length; i++) {
        textareas[i].setAttribute('class','form-control')
      }
    for (i = 0; i < tds.length; i++) {
        $(tds[i]).css('background-color','white')
      }

});

$(document).ready(function(){
    var click = 0;
    $('.grid-item').click(function(e){
        var x = $(e.target).find(".hide");
        var y = $(e.target).find(".hide2");
        var id = $(this).attr('id')
        console.log(id)
        click++
        timer = setTimeout(function(){
            if (click == 1){
                x.click();
                var appointDate = $('#appoint-form').children('p').children('input[name=appointment_date]');
                console.log(appointDate)
                appointDate.val(createValidDate(id))
            }else{
                y.click()
                var appointDate = $('#comment-form').children('p').children('input[name=date]');
                console.log(id)
                appointDate.val(createValidDate(id))
            }
        click =0
        }, 300)

    });
});


function createDefault(button, form, id, select){
    var appointId = button.attr('id')
    var appointDate = form.children('p').children('input[name=appointment_date]');
    var timeValue = button.attr('name') + ':00'
    for (let i =0; i<select.children.length; i++){
        if (select[i].value == timeValue){
            select.selectedIndex = i
        }
    }
    $('#edit-appoint-form').attr('action',`/therapist/update_apt/${appointId}/`)
    $('#edit-appoint-res-form').attr('action',`/therapist/update_apt_res/${appointId}/`)
    $('#update-appoint-form').attr('action',`/therapist/appointment_response/${appointId}/`)
    appointDate.val(createValidDate(id))
}

$(document).ready(function(){
    $(':button').click(function(e){
        var mySelect = document.getElementById('mySelect')
        var mySelect2 = document.getElementById('mySelect2')
        if ($(this).attr('class') == 'btn btn-success edit-appoint-btn-a'){
            createDefault($(this), $('#edit-appoint-form'), $(this).closest('tr').attr('id'), mySelect)
        }else if ($(this).attr('class') == 'btn btn-success edit-appoint-res-btn-a'){
            createDefault($(this), $('#edit-appoint-res-form'), $(this).closest('tr').attr('id'), mySelect2)
        }else if ($(this).attr('class') == 'btn btn-success edit-appoint-btn'){
            createDefault($(this), $('#edit-appoint-form'), $(this).closest('.grid-item').attr('id'), mySelect)
        }else if ($(this).attr('class') == 'btn btn-success edit-appoint-res-btn'){
            createDefault($(this), $('#edit-appoint-res-form'), $(this).closest('.grid-item').attr('id'), mySelect2)
        }else if ($(this).attr('class') == "btn btn-primary update-appoint-btn"){
            createDefault($(this), $('#update-appoint-form'), $(this).closest('tr').attr('id'), mySelect)
        }

    });
});


$(document).ready(function(){
    $('#con').css('width', $('#myVideoCon').css('width'))
    $('#hand-container').css('width', $('#myVideoCon').css('width'))
});


$(document).ready(function(){
    $('.send').click(function(e){
        var email = $(this).text()
        var emailField = $('#contact-form-therapist').children('p').children('input[name=email]');
        emailField.val(email)
    });
});


$(document).ready(function(){
    $(".edit-comment-btn").click(function(e){
        var button = $(e.target);
        var li1 = button.closest('ul').children()[0];
        var li2 = button.closest('ul').children()[1];
        console.log(li1);
        console.log(button.attr('id'))
        var form = document.getElementById('form' + button.attr('id'))
        var title = form.getElementsByTagName('input')[1]
        var content = form.getElementsByTagName('textarea')[0]
        title.defaultValue = li1.textContent
        content.defaultValue = li2.textContent

    });
});

