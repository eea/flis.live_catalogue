$(function () {

    var submitFilterForm = function (e) {
        e.preventDefault();
        $(this).parents('form').submit();
    }

    var catalogue_filter = $('#catalogue-filter');
    catalogue_filter.on('change', 'select', submitFilterForm);
    catalogue_filter.find('select').select2({'width': 'resolve'});

    $('select').select2({
        width: 'resolve'
    });

    $('select').each(function () {
        var $this = $(this);
        if($this.data('readonly') == 'readonly') {
            $this.select2('readonly', true);
        }
    });

});
