$(function date () {
    $("#datepicker").datepicker({
        changeMonth: true,
        dateFormat: "dd-mm-yy",
        beforeShowDay: function(d) {
        var day = d.getDay();
        return [(day != 5 && day != 6)];
    }
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