$(function date () {
    $("#datepicker2").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "dd-mm-yy",        
    });
});

$(function birth_picker() {
    $("#datepicker_birth").datepicker({
        changeYear: true,
        yearRange: "1930:2003",
        dateFormat: "dd-mm-yy",
    })
});

$(function calendar_picker() {
    $("#calendar_picker").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'dd-mm-yy',
    })
});


$(function() {
    $("#datepicker").datepicker({
        changeMonth: true,
        dateFormat: "dd-mm-yy",
        beforeShowDay: function(d) {
        var day = d.getDay();
        const value = JSON.parse(document.getElementById('hello').textContent);
        const arr = []
        for (let i = 0; i< value.length; i++){
            value[i] += 1
            arr.push(value[i])
        }
        return [(!arr.includes(day))]
    }
    });
});

$(document).ready(function(){
    $("td").mouseenter(function(e){
        var x = $(e.target).find(".comment-list");
        timer = setTimeout(function(){
            x.click()
        }, 1000)

    }).mouseleave(function(){
        clearTimeout(timer)
    })
});

$(document).ready(function(){
    $("td").click(function(e){
        var x = $(e.target).find(".hide");
        x.click()
    });
});

$(document).ready(function(){
    $(".hide").hide()
    $(".comment-list").hide()
});



document.addEventListener('click', someFunc)

function someFunc(e){
    var td = e.target
    var t = document.getElementById('datepicker')
    var t2 = document.getElementById('datepicker2')
    if(td.tagName == 'TD'){
        t.defaultValue = td.id
        t2.defaultValue = td.id
    }
}

// function editCommentDefaultValue(e){
//     var button = e.target;
//     var li1 = button.closest('ul').children[0].innerText;
//     var li2 = button.closest('ul').children[1].innerText;
//     var commentForm = button.closest('.modal').nextElementSibling;
//     // var title = commentForm.children[1].children[1];
//     console.log(commentForm.find('#comment-form'))
//     title.defaultValue = li1
// }
$(document).ready(function(){
    $(".edit-comment-btn").click(function(e){
        var button = $(e.target);
        var li1 = button.closest('ul').children()[0];
        var li2 = button.closest('ul').children()[1];
        console.log(li1);

        var commentForm = button.closest('.modal').next()
        
        // console.log(button.attr('id'))
        // var form = document.getElementById('form' + button.attr('id'))
        // console.log(button)
        // var title = form.getElementsByTagName('input')[1]
        // var content = form.getElementsByTagName('textarea')[0]
        // title.defaultValue = li1.textContent
        // content.defaultValue = li2.textContent
        // console.log(form)


        // var content = commentForm.find('.content');
        // console.log(commentForm.closest('.text').attr('class'))

    });
});


$(document).ready(function(){
    $(".edit-comment-btn").click(function(e){
        console.log('s')
    });
});


function getData(request){
    console.log(request)
    return request
}
function gData(){
    console.log(getData())
}