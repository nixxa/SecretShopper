import 'bootstrap/dist/css/bootstrap.css';
import 'bootswatch/yeti/bootstrap.css';
import '../css/site.css';

window.jQuery = require('jquery');
let $ = window.jQuery;
let moment = require('moment');

$(function () {
    moment.locale('ru');
    $.each($('.js-datetime-from'), function () {
        var $this = $(this);
        $this.text(moment.utc($this.data('datetime')).format('D MMMM YYYY'));
    });
    $.each($('.js-month'), function () {
        var $this = $(this);
        $this.text(moment.utc($this.data('datetime')).format('MMMM'));
    });
    $('.js-remove-report-btn').click(function (e) {
        if (!confirm('Вы действительно желаете удалить анкету?')) {
            e.preventDefault();
        }
    });
    $('.js-change-month>a.btn-link').click(function (e) {
        var $this = $(this);
        $this.parent().addClass('hidden');
        $this.parents('.js-change-month-container').find('.js-change-month-select').removeClass('hidden');
    });
    $('.js-change-month-select').change(function (e) {
        $.post('/report/changemonth', { uid: $(this).data('uid'), month: $(this).val() }, function (data) {
            window.location.reload();
        });                    
    });
});