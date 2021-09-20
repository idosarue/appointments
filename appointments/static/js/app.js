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

