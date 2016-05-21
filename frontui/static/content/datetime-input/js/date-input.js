define(function(require) {
    var $ = require('jquery');
    
    var dateInput = function (options) {
        options = $.extend({}, options);
        var id = options.id;
        if (id == undefined || id === '') {
            id = 'js-date-input-' + Math.random();
        }
        // add html container to body
        $('body').append('<div id="' + id + '" style="display:none;"></div>');
        var $container = $(id);
        container.css({
            'position': 'absolute',
            'height': '50%',
            'left': '0',
            'right': '0',
            'bottom': '0'
        });
        
        // set onclick function
        var $field = $(this);
        $field.on('click', function (evt) {
            $container.css('display', 'block');
        });
        $('body').on('click', function (evt) {
            $container.css('display', 'none');
        })
    };
    $.fn.DateInput = dateInput;
    
    // activate on document ready
    $(function () {
        $('input[data-toggle="date-input"]').DateInput();
    });
});