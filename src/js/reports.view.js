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
        $this.text(moment.utc($this.data('datetime')).fromNow());
    });
});