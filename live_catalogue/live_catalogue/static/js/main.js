$(function () {

    $('#id_start_date').datepicker({'dateFormat': 'dd/mm/yy'});
    $('#id_end_date').datepicker({'dateFormat': 'dd/mm/yy'});

    var submitFilterForm = function (e) {
        e.preventDefault();
        $(this).parents('form').submit();
    }
    $('#catalogue-filter').on('change', 'select', submitFilterForm);
});
