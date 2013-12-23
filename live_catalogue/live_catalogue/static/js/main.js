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

    $('#document-add').on('click', function () {
        var i = $('#documents-container').find('.document-container-upload').length;
        var max_forms = parseInt($('#id_form-MAX_NUM_FORMS').val());
        if(i >= max_forms - 1) {
            $(this).hide();
        }
        var dc = $('#documents-container')
            .find('.document-container-upload:last')
            .clone();
        var input = dc.find('input')
        input.attr('name', 'form-' + i + '-name');
        input.attr('id', 'id_form-' + i + '-name');
        input.val('');
        $('#id_form-TOTAL_FORMS').val(i+1);
        $('#document-add').before(dc);
    });

    $('.document-container').on('click', '.remove', function (e) {
        e.preventDefault()
        if(!confirm('Are you sure you want to delete this file?')) {
            return;
        }

        var i = $('#documents-container').find('.document-container').length;
        var max_forms = $('#id_form-MAX_NUM_FORMS').val();

        var $this = $(this);
        var href = $this.data('href');
        $.ajax({
            type: 'DELETE',
            url: href,
            success: function (data) {
                $this.parents('.document-container').fadeOut('fast', function () {
                    $(this).remove();
                });
                if(i - 1 <= max_forms) {
                    $('#document-add').show();
                }
            }
        });

    });

});
