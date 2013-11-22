$(function () {

    $('#id_start_date').datepicker();
    $('#id_end_date').datepicker();

    var submitFilterForm = function (e) {
        e.preventDefault();
        $(this).parents('form').submit();
    }
    $('#catalogue-filter').on('change', 'select', submitFilterForm);
});
