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
        }, 1500)

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


$(document).ready(function(){
    $(":button").click(function(e){
        console.log($(this))
    })
});

function someFunc(e){
    var td = e.target
    var t = document.getElementById('datepicker')
    var t2 = document.getElementById('datepicker2')
    if(td.tagName == 'TD'){
        t.defaultValue = td.id
        t2.defaultValue = td.id
    }
}

document.addEventListener('click', someFunc)

