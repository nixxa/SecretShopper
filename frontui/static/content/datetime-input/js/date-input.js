/*  Date input control
    Using:
    In HTML:
    <input type="text" name="check_date" 
        data-toggle="date-input"
        data-isodate="2016-05-21"
        value="21 Май 2016" />
    Or manually in JS:
        $('input[name="check_date"]').DateInput();
*/
define(function(require) {
    var $ = require('jquery');
    
    Date.prototype.getMonthName = function(lang) {
        lang = lang && (lang in Date.locale) ? lang : 'en';
        return Date.locale[lang].month_names[this.getMonth()];
    };

    Date.prototype.getMonthNameShort = function(lang) {
        lang = lang && (lang in Date.locale) ? lang : 'en';
        return Date.locale[lang].month_names_short[this.getMonth()];
    };

    Date.locale = {
        en: {
            month_names: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            month_names_short: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        ru: {
            month_names: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
            month_names_short: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
        },
    };
    
    function randomInteger(min, max) {
        var rand = min + Math.random() * (max - min)
        rand = Math.round(rand);
        return rand;
    };
    
    function close(cont, evt) {
        if (evt) {
            evt.preventDefault();
            evt.stopPropagation ? evt.stopPropagation() : (evt.cancelBubble=true);
        }
        if (cont) {
            cont.removeClass('in');
            cont.find('.view').removeClass('in');
            cont.data('shown', 'false');
        }
        $('body').css('overflow', 'auto');
        $('body').removeClass('shadow-bg');
        $('input').removeClass('shadow-bg');
        $('select').removeClass('shadow-bg');
    };
    
    function showSelected() {
        var $this = $(this);
        var $cont = $this.parents('.date-input-container');
        if ($cont.data('shown') == 'false') {
            return;
        }
        var offset = $this.parent().offset().top - $this.offset().top;
        if (offset > 0) {
            return;
        }
        offset = -offset;
        if (Math.abs(60 - offset) < 7) {
            $this.addClass('selected');
        } else {
            $this.removeClass('selected');
        }
    }

    var dateInput = function (options) {
        var $field = $(this);
        options = $.extend({
            lang: 'ru'
        }, options);
        var id = options.id;
        var date = null;
        if ($field.data('isodate') != '') {
            date = new Date(Date.parse($field.data('isodate')));
        }
        if (id == undefined || id === '') {
            id = 'js-date-input-' + randomInteger(1000000, 9999999);
        }
        // add html container to body
        $('body').append(
            '<div id="' + id + '" class="date-input-container" data-shown="false">' + 
                '<div class="chooser">' +
                    '<div class="view">&nbsp;</div>' +
                    '<div class="day-column"></div>' +
                    '<div class="month-column"></div>' +
                    '<div class="year-column"></div>' +
                '</div>' +
                '<div class="controls">' + 
                    '<a href="#" class="btn-set" disabled="disabled">Выбрать</a>' +
                    '<a href="#" class="btn-cancel">Отмена</a>' +
                '</div>' + 
            '</div>');
        var $container = $('#' + id);
        var $cancelBtn = $container.find('.btn-cancel');
        $cancelBtn.click(function (evt) {
            close($container, evt);
        });
        
        var $dayColumn = $container.find('.day-column');
        for (var i = -1; i < 33; i++) {
            if (i < 1 || i > 31) {
                $dayColumn.append('<div class="column-cell" data-value="-1"><div>&nbsp;</div></div>');
            } else {
                $dayColumn.append('<div class="column-cell" data-value="' + 
                        (i < 10 ? '0'+i : i) + '"><div>' + i + '</div></div>');
            }
        }
        
        var $monthColumn = $container.find('.month-column');
        var dt = new Date();
        for (var i = -2; i < 14; i++) {
            if (i < 0 || i > 11) {
                $monthColumn.append('<div class="column-cell" data-value="-1"><div>&nbsp;</div></div>');
            } else {
                dt.setMonth(i);
                var m = dt.getMonth() + 1;
                $monthColumn.append('<div class="column-cell" data-value="' + 
                        (m < 10 ? '0' + m : m) + '"><div>' + 
                        dt.getMonthName(options.lang) + '</div></div>');
            }
        }
        
        var $yearColumn = $container.find('.year-column');
        dt = new Date(); 
        for (var i = dt.getFullYear() + 2; i > 1987; i--) {
            if (i > dt.getFullYear() || i < 1990) {
                $yearColumn.append('<div class="column-cell" data-value="-1"><div>&nbsp;</div></div>');
            } else {
                $yearColumn.append('<div class="column-cell" data-value="' + i + '"><div>' + i + '</div></div>');
            }
        }
        
        // set on scroll event handler
        $dayColumn.on('scroll', function (evt) {
            $.each($dayColumn.find('.column-cell'), showSelected);
        });
        $monthColumn.on('scroll', function (evt) {
            $.each($monthColumn.find('.column-cell'), showSelected);
        });
        $yearColumn.on('scroll', function (evt) {
            $.each($yearColumn.find('.column-cell'), showSelected);
        });
        
        // if date set in field - set it in control
        if (date != null) {
            var h = $yearColumn.find('.column-cell:first').height();
            var y = date.getDate();
            $dayColumn.scrollTop((y-1) * h + 1);
            y = date.getMonth();
            $monthColumn.scrollTop(y * h + 1);
            y = dt.getFullYear() - date.getFullYear();
            $yearColumn.scrollTop(y * h + 1);
        }
        
        var $selectBtn = $container.find('.btn-set');
        $selectBtn.click(function (evt) {
            var daySelected = $dayColumn.find('.column-cell.selected');
            var monthSelected = $monthColumn.find('.column-cell.selected');
            var yearSelected = $yearColumn.find('.column-cell.selected');
            $field.val(yearSelected.data('value') + '-' + monthSelected.data('value') + '-' + daySelected.data('value'));
            close($container, evt);
        });

        
        // set onclick function
        $field.on('click', function (evt) {
            evt.preventDefault();
            evt.stopPropagation ? evt.stopPropagation() : (evt.cancelBubble=true);
            $field.blur();
            $container.addClass('in');
            $container.find('.view').addClass('in');
            $container.data('shown', 'true');
            $('body').css('overflow', 'hidden');
            $('body').addClass('shadow-bg');
            $('input').addClass('shadow-bg');
            $('select').addClass('shadow-bg');
        });
        // set close action at outside click
        $('body').on('click', function (evt) {
            close($container);
        })
    };
    $.fn.DateInput = dateInput;
    
    // activate on document ready
    $(function () {
        $('input[data-toggle="date-input"]').DateInput();
    });
});