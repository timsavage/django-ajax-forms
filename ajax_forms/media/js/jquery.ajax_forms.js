/*! Copyright 2009 Tim Savage <tim.savage@jooceylabs.com>
 * Licensed under the BSD license (http://www.opensource.org/licenses/bsd-license.php)
 *
 * Version: 0.2
 * Requires jQuery 1.2.6+
 * Docs: http://code.google.com/p/django-ajax-forms/
 */

(function($) {

    // Console helper
    function log(message) {
        if (window.console) {
            console.debug(message);
        }
    }


    $.fn.validation = function(fields, options) {
        // Setup options
        var opts = $.extend({}, $.fn.validation.defaults, options);

        return $(this).each(function() {
            var form = $(this);

            // Setup fields
            for (var name in fields) {
                var field = form.find(':input[name='+name+']');
                if (field) {
                    field.data('validation', fields[name]);
                    // Bind events
                    for (var idx in opts.validation_events) {
                        field.bind(opts.validation_events[idx], function() {
                            validate_field($(this), opts);
                        });
                    }
                }
            }

            // Setup form events
            form.submit(function() {
                var first_fail = null;

                for (var name in fields) {
                    var field = form.find(':input[name='+name+']');
                    if (field) {
                        if (!validate_field(field, opts)) {
                            if (first_fail == null) {
                                first_fail = field;
                            }
                        }
                    }
                }

                if (first_fail) {
                    first_fail.focus();
                }
                return first_fail == null;
            });
        });
    };


    // Custom error object
    $.fn.validation.ValidationError = function(msg, params) {
        params = params || [];
        for(idx in params) {
            msg = msg.replace(idx, params[idx]);
        }
        var err = new Error(msg);
        err.name = "ValidationError";
        return err;
    }
    var ValidationError = $.fn.validation.ValidationError;


    // Validate a single field
    function validate_field(field, opts) {
        var parent = opts.callbacks.get_parent_element(field, opts.layout);
        var field_valid = true;
        var validation = field.data('validation');
        var value = field.val();

        // Handle checkboxs
        if (field[0].type && field[0].type == "checkbox") {
            if (!field[0].checked) {
                value = null;
            }
        }

        log('Validate: ' + value);

        parent.removeClass(opts.style.valid);
        parent.removeClass(opts.style.invalid);
        parent.addClass(opts.style.processing);

        // Catch Validation errors
        try {
            if (value && value.length > 0) {
                for (var rule in validation.rules) {
                    var rule_func = $.fn.validation.rules[rule]
                    if (rule_func) {
                        rule_func(validation.rules[rule], value, validation.msgs, field[0].form);
                    } else {
                        log('Rule not found: ' + rule);
                    }
                }
            } else {
                if (validation.required) {
                    throw new ValidationError(validation.msgs['required']);
                }
            }

            // Clear existing error
            opts.callbacks.clear_error(field, opts.layout);
        } catch (e) {
            // Make sure error was thrown by validation.
            if (e.name && e.name == 'ValidationError') {
                field_valid = false;
                opts.callbacks.show_error(field, e.message, opts.layout);
            } else {
                log(e.message);
                throw e;
            }
        }

        if (field_valid) {
            parent.addClass(opts.style.valid);
        } else {
            parent.addClass(opts.style.invalid);
        }
        parent.removeClass(opts.style.processing);
        return field_valid;
    }

    // Default settings
    $.fn.validation.defaults = {
        // Type of form layout to interact with;
        // p | ul | table | dl
        layout: 'table',

        // Events on which to perform validation
        validation_events: ['blur'],

        // Classes applied in various states
        style: {
            valid: 'valid',
            invalid: 'invalid',
            processing: 'processing'
        },

        // Callback methods
        callbacks: {
            // Get the parent of a particular field element (mainly to handle
            // the case of tables)
            get_parent_element: function(field, layout) {
                if (!field._parent) {
                    if (layout == 'table') {
                        field._parent = field.parent().parent();
                    } else {
                        field._parent = field.parent();
                    }
                }
                return field._parent;
            },

            // Show error message
            show_error: function(field, msg, layout) {
                var errors = field.siblings('ul');
                if (errors.length) {
                    errors.empty();
                } else {
                    errors = $('<ul>')
                        .addClass('errorlist')
                        .hide();
                    if (layout == 'table') {
                        errors.insertBefore(field);
                    } else {
                        field.parent().prepend(errors);
                    }
                }
                $('<li>')
                    .text(msg)
                    .appendTo(errors);
                errors.fadeIn();
            },

            // Clear existing error message
            clear_error: function(field, layout) {
                field.siblings('ul').fadeOut(function() { $(this).remove(); });
            }
        }
    };


    // Regular expressions
    var IS_FLOAT = /^-?[0-9]*(\.?[0-9]*)$/;
    var IS_INTEGER = /^-?[0-9]+$/;
    var DECIMAL_LENGTHS = /^[-\s0]*(\d*).?(\d*)\s*$/;

    /* Validation methods, additional functions can be added to preform
     * custom validation eg:
     * $.fn.validation.rules['foo'] = function(arg, value, msgs) {
     *     if (validation fail) {
     *         throw new ValidationError(msgs['msg_code']);
     *     }
     * };
     */
    $.fn.validation.rules = {

        'max_length': function(arg, value, msgs, form) {
            if (value.length > arg) {
                throw new ValidationError(msgs['max_length'], {
                    '%(max)d': arg,
                    '%(length)d': value.length
                });
            }
        },

        'min_length': function(arg, value, msgs, form) {
            if (value.length < arg) {
                throw new ValidationError(msgs['min_length'], {
                    '%(min)d': arg,
                    '%(length)d': value.length
                });
            }
        },

        'is_float': function(arg, value, msgs, form) {
            value = $.trim(value);
            if (!IS_FLOAT.test(value) || isNaN(parseFloat(value))) {
                throw new ValidationError(msgs['invalid']);
            }
        },

        'is_integer': function(arg, value, msgs, form) {
            value = $.trim(value);
            if (!IS_INTEGER.test(value) || isNaN(parseInt(value))) {
                throw new ValidationError(msgs['invalid']);
            }
        },

        'max_value': function(arg, value, msgs, form) {
            var value = Number(value);
            if (value > arg) {
                throw new ValidationError(msgs['max_value'], {
                    '%s': arg
                });
            }
        },

        'min_value': function(arg, value, msgs, form) {
            var value = Number(value);
            if (value < arg) {
                throw new ValidationError(msgs['min_value'], {
                    '%s': arg
                });
            }
        },

        'decimal_lengths': function(arg, value, msgs, form) {
            var match = DECIMAL_LENGTHS.exec(value);
            if (match) {
                var max_digits = arg[0];
                if (max_digits !== null && (match[1].length + match[2].length) > max_digits) {
                    throw new ValidationError(msgs['max_digits'], {
                        '%s': max_digits
                    });
                }

                var max_decimal_places = arg[1];
                if (max_decimal_places !== null && match[2].length > max_decimal_places) {
                    throw new ValidationError(msgs['max_decimal_places'], {
                        '%s': max_decimal_places
                    });
                }

                if (max_digits !== null && max_decimal_places !== null) {
                    var max_whole_digits = max_digits - max_decimal_places;
                    if (match[1].length > max_whole_digits) {
                        throw new ValidationError(msgs['max_whole_digits'], {
                            '%s': max_whole_digits
                        });
                    }
                }
            }
        },

        'regex': function(arg, value, msgs, form) {
            var re = RegExp(arg[0], arg[1]);
            if (!re.test(value)) {
                throw new ValidationError(msgs['invalid']);
            }
        },

        'equal_to_field': function(arg, value, msgs, form) {
            var other = $(form).find(':input[name='+arg+']').val();
            if (other != value) {
                throw new ValidationError(msgs['equal_to_field']);
            }
        }

    };

})(jQuery);
