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
        var opts = $.extend({}, $.validation.defaults, options);

        return $(this).each(function() {
            var form = $(this);

            // Setup fields
            for (var name in fields) {
                var field = form.find(':input[name='+name+']');
                if (field) {
                    field.data('validation', fields[name]);
                    // Bind events
                    for (var idx in opts.validation_events) {
                        field.bind(opts.validation_events[idx], function(e) {
                            // Work around to prevent validation when tabbing
                            // into a field.
                            if (e.keyCode === 9) {
                                return;
                            }
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
                    first_fail
                        .focus()
                        .scroll();
                }
                return first_fail == null;
            });
        });
    };


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

        parent.removeClass(opts.style.valid);
        parent.removeClass(opts.style.invalid);
        parent.addClass(opts.style.processing);

        // Catch Validation errors
        try {
            if (value && value.length > 0) {
                for (var rule in validation.rules) {
                    var rule_func = $.validation.rules[rule]
                    if (rule_func) {
                        rule_func(field[0], validation.rules[rule], value, validation.msgs);
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
    

    // Validation "namespace"
    $.validation = new Object();


    // Rules placeholder
    $.validation.rules = {};
    

    // Custom error object
    $.validation.ValidationError = function(msg, params) {
        params = params || [];
        for(idx in params) {
            msg = msg.replace(idx, params[idx]);
        }
        var err = new Error(msg);
        err.name = "ValidationError";
        return err;
    }
    var ValidationError = $.validation.ValidationError;


    // Default settings
    $.validation.defaults = {
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
                var parent = field.data('parent');
                if (!parent) {
                    if (layout == 'table') {
                        parent = field.parent().parent();
                    } else {
                        parent = field.parent();
                    }
                    field.data('parent', parent);
                }
                return parent;
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
                    } else if (layout == 'dl') {
                        errors.insertAfter(field);
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

})(jQuery);
