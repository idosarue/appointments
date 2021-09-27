
function createValidDate(x){
    var newDate = x.split('-').reverse()
    if (newDate[1].length < 2){
        newDate[1] = 0 + newDate[1]
    }
    if (newDate[2].length < 2){
        newDate[2] = 0 + newDate[2] 
    }

    console.log(newDate)

    return newDate.join('-')
}



$(document).ready(function(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    var dateInputs = $("input[name*='date']")
    for (let i = 0; i<dateInputs.length; i++){
        console.log(dateInputs[i])
        dateInputs[i].type = 'date'
        dateInputs[i].setAttribute('min', today);
    };
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
        }
      }
    for (i = 0; i < selects.length; i++) {
        selects[i].setAttribute('class','form-control')
      }
    for (i = 0; i < textareas.length; i++) {
        textareas[i].setAttribute('class','form-control')
      }
    for (i = 0; i < tds.length; i++) {
        $(tds[i]).css('background-color','whitesmoke')
      }
});

$(document).ready(function(){
    var click = 0;
    $('td').click(function(e){
        var x = $(e.target).find(".hide");
        var y = $(e.target).find(".hide2");
        var id = $(this).attr('id')
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

$(document).ready(function(){
    $('.edit-appoint-btn').click(function(){
        var id = $(this).closest('td').attr('id')
        var appointId = $(this).closest('li').attr('id')        
        var timeValue = $(this).closest('li').text().slice(0,5) + ':00'
        var appointDate = $('#edit-appoint-form').children('p').children('input[name=appointment_date]');
        $('#edit-appoint-form').attr('action',`/therapist/update_apt/${appointId}/`)
        console.log(id)
        appointDate.val(createValidDate(id))
        $(`select option[value="${timeValue}"]`).attr("selected",true);
        var start_time = $('#edit-appoint-form').children('p').children('input[name=start_time]');
        start_time.val(timeValue)
    });
});

$(document).ready(function(){
    $('.hide').click(function(){
        var id = $(this).closest('td').attr('id')
        var appointId = $(this).closest('li').attr('id')        
        var appointDate = $('#appoint-form').children('p').children('input[name=appointment_date]');
        $('#edit-appoint-form').attr('action',`/therapist/update_apt/${appointId}/`)
        console.log(id)
        appointDate.val(createValidDate(id))
    });
});

$(document).ready(function(){
    $('.edit-appoint-res-btn').click(function(e){
        var id = $(this).closest('td').attr('id')
        var appointId = $(this).closest('li').attr('id')
        var timeValue = $(this).closest('li').text().slice(0,5) + ':00'
        var appointDate = $('#edit-appoint-res-form').children('p').children('input[name=appointment_date]');
        $('#edit-appoint-res-form').attr('action',`/therapist/update_apt_res/${appointId}/`)
        console.log(appointId)
        appointDate.val(createValidDate(id))
        $(`select option[value="${timeValue}"]`).attr("selected",true);
        var start_time = $('#edit-appoint-res-form').children('p').children('input[name=start_time]');
        start_time.val(timeValue)
    });
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

        var commentForm = button.closest('.modal').next()
        
        console.log(button.attr('id'))
        var form = document.getElementById('form' + button.attr('id'))
        console.log(button)
        var title = form.getElementsByTagName('input')[1]
        var content = form.getElementsByTagName('textarea')[0]
        console.log(title)
        title.defaultValue = li1.textContent
        content.defaultValue = li2.textContent
        console.log(form)

    });
});



// $(function date () {
//     $("#datepicker2").datepicker({
//         changeMonth: true,
//         changeYear: true,
//         dateFormat: "dd-mm-yy",        
//     });
// });

// $(function birth_picker() {
//     $("#datepicker_birth").datepicker({
//         changeYear: true,
//         yearRange: "1930:2003",
//         dateFormat: "dd-mm-yy",
//     })
// });

// $(function calendar_picker() {
//     $("#calendar_picker").datepicker({
//         changeMonth: true,
//         changeYear: true,
//         dateFormat: 'dd-mm-yy',
//     })
// });


// $(function() {
//     $("#datepicker").datepicker({
    //     changeMonth: true,
    //     dateFormat: "dd-mm-yy",
    //     beforeShowDay: function(d) {
    //     var day = d.getDay();
    //     const value = JSON.parse(document.getElementById('hello').textContent);
    //     const arr = []
    //     for (let i = 0; i< value.length; i++){
    //         value[i] += 1
    //         arr.push(value[i])
    //     }
    //     return [(!arr.includes(day))]
    // }
    // });
// });
// $(function() {
//     $(".edit-datepicker").datepicker({
//         changeMonth: true,
//         dateFormat: "dd-mm-yy",
//         beforeShowDay: function(d) {
//         var day = d.getDay();
//         const value = JSON.parse(document.getElementById('hello').textContent);
//         const arr = []
//         for (let i = 0; i< value.length; i++){
//             value[i] += 1
//             arr.push(value[i])
//         }
//         return [(!arr.includes(day))]
//     }
//     });
// });



// $(document).ready(function(){
//     $("td").click(function(e){
//         var x = $(e.target).find(".hide");
//         x.click()
//     });
// });

// $(document).ready(function(){
//     $(".hide").hide()
//     $(".comment-list").hide()
// });
// $(document).ready(function(){
//     var x= $(".datepicker")
//     var td = x.closest('td').attr('id')
//     for (i =0; i<x.length; i++){
//         x[i]
//     }
//     console.log(x)
//     console.log('s')
// });


// $(document).ready(function(){
//     $(".edit-comment-btn").click(function(e){
//         var button = $(e.target);
        // var li1 = button.closest('ul').children()[0];
        // var li2 = button.closest('ul').children()[1];
//         console.log(li1);

//         var commentForm = button.closest('.modal').next()
        
//         console.log(button.attr('id'))
//         var form = document.getElementById('form' + button.attr('id'))
//         console.log(button)
//         var title = form.getElementsByTagName('input')[1]
//         var content = form.getElementsByTagName('textarea')[0]
//         console.log(title)
//         title.defaultValue = li1.textContent
//         content.defaultValue = li2.textContent
//         console.log(form)

//     });
// });

// // $(document).ready(function(){
// //     $(".hide").click(function(e){
// //         var button = $(e.target);
// //         var date = $('#datepicker')
// //         var date2 = $('#datepicker2')
// //         date.defaultValue = button.attr('id')
// //         date2.defaultValue = button.attr('id')
// //     });
// // });


// // $(document).ready(function(){
// //     $(".edit-appoint-btn").click(function(e){
// //         var button = $(e.target);
// //         var li1 = button.closest('li')[0];
// //         console.log(li1);
// //         var td_date = button.closest('td')
// //         console.log()
// //         var time = $('select')
// //         var date = $('#datepicker')
// //         // date.defaultValue = button.attr('id')
// //         time.defaultValue = li1.textContent.slice(0,5) + ':00'
// //     });
// // });



// // $(document).ready(function(){
// //     $(".edit-appoint-btn").click(function(e){
// //         var button = $(e.target);
// //         var button = $(e.target);
// //         var li1 = button.closest('li')[0];
// //         console.log(li1);
// //         var td_date = button.closest('td')
// //         console.log()

// //         console.log(button.attr('id'))
// //         var form = document.getElementById('edit-appoint-form' + button.attr('id'))
// //         console.log(button)
// //         var time = $('select')
// //         var date = form.getElementsByTagName('input')[1]
// //         console.log(title)
// //         time.defaultValue = li1.textContent.slice(0,5) + ':00'
// //         date.defaultValue = td_date.attr('id')
// //         console.log(form)

// //     });
// // });

