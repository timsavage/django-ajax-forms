(function($) {

    $.fn.validation = function(fields, options) {
        // Setup options
        opts = $.extend({}, $.fn.validation.defaults, options);

        function validate_field(field) {
            field.next().addClass(opts.style.processing);
            var field_valid = true;

            var validators = field.data('validators');
            for (key in validators) {
                validator = $.fn.validation.validators[key]
                if (validator) {
                    field_valid &= validator(field, validators[key]);
                }
            }

            if (field_valid) {
                field.next()
                    .addClass(opts.style.valid)
                    .removeClass(opts.style.invalid);
            } else {
                field.next()
                    .removeClass(opts.style.valid)
                    .addClass(opts.style.invalid);
            }

            field.next().removeClass(opts.style.processing);
            return field_valid;
        }

        function validate_field_onblur() {
            validate_field($(this));
        }

        function validate_form_onsubmit() {
            var first_fail = null;
            var form = $(this);

            $.each(fields, function() {
                var field = form.find(':input[name='+this.name+']');
                if (field) {
                    if (!validate_field(field)) {
                        if (first_fail == null) {
                            first_fail = field;
                        }
                    }
                }
            });

            if (first_fail != null) {
                first_fail.focus();
                return false;
            }
            return true;
        }

        return $(this).each(function() {
            var form = $(this);

            // Setup fields
            $.each(fields, function() {
                var field = form.find(':input[name='+this.name+']');
                if (field) {
                    $('<span>&nbsp;</span>').insertAfter(field);
                    $(field)
                        .data('validators', this.validators)
                        .blur(validate_field_onblur);
                }
            });

            // Setup form events
            form.submit(validate_form_onsubmit);
        });
    };

    $.fn.validation.defaults = {
        // Default style to work around
        format: 'table',
        // Classes applied in various states
        style: {
            valid: 'valid',
            invalid: 'invalid',
            processing: 'processing'
        }
    };

    $.fn.validation.validators = {
        // Field requires a value
        'required': function(field, params) {
            if ($(field).val().length <= 0) {
                return false
            }
            return true;
        }
    };

})(jQuery);
