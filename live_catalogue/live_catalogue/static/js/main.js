$(function () {

    $('#id_start_date').datepicker({'dateFormat': 'dd/mm/yy'});
    $('#id_end_date').datepicker({'dateFormat': 'dd/mm/yy'});

    var catalogue_filter = $('#catalogue-filter');
    $('#id_date_range').daterangepicker({'format': 'DD/MM/YYYY',
                                         'parentEl': catalogue_filter});

    var submitFilterForm = function (e) {
        e.preventDefault();
        $(this).parents('form').submit();
    }
    catalogue_filter.on('change', 'select', submitFilterForm);
    catalogue_filter.find('select').select2({'width': 'resolve'});
});
