
$(function () {
    $("#datepicker").datepicker({
        changeMonth: true,
        dateFormat: "dd-mm-yy",
        beforeShowDay: function(d) {
        var day = d.getDay();
        return [(day != 5 && day != 6)];
    }
    });
});
