(function($) {

    $.fn.validation = function(settings) {
        settings = $.extend({
            fields: {},
            token_valid: 'valid',
            token_invalid: 'invalid',
        }, settings);

        function validate_field(field) {
            var validators = field.data('validators');
            var field_valid = true;
            if (validators.required) {
                field_valid &= field.val().length != 0;
            }

            if (field_valid) {
                field.next()
                    .addClass(settings.token_valid)
                    .removeClass(settings.token_invalid);
            } else {
                field.next()
                    .removeClass(settings.token_valid)
                    .addClass(settings.token_invalid);
            }
            return field_valid;
        }

        function validate_field_onblur() {
            validate_field($(this));
        }

        /*function validate_form_onsubmit() {
            var first_fail = null;
            var form = $(this);

            $.each(settings.validators, function() {
                var element = form.find('[name='+field.name+']');
                if (!validate_field($(element))) {
                    if (first_fail == null) {
                        first_fail = $(element);
                    }
                }
            });

            if (first_fail != null) {
                first_fail.focus();
                form.find(':submit').next().show().fadeout(1000);
                return false;
            }
            return true;
        }*/

        return $(this).each(function() {
            var form = $(this);
            var fields = form.find(':input');

            // Setup fields
            $.each(settings.fields, function() {
                var field = form.find('[name='+this.name+']');
                if (field) {
                    $('<span>&nbsp;</span>').insertAfter(field);
                    $(field)
                        .data('validators', this.validators)
                        .blur(validate_field_onblur);
                }
            });

            // Setup form events
            //$('<span>Form not valid!</span>').hide().insertAfter(form.find(':submit'));
            //form.submit(validate_form_onsubmit);
        });
    };

})(jQuery);
