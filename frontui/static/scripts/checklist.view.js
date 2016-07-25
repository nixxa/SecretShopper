/***
 * Questionnaire view script.
 * Define onClick handler for question buttons.
 * DOM structure must be follow:
 * .js-section
 *      .js-section-title
 *          .js-section-badge
 *              .js-section-badge-value
 *              .js-section-badge-total
 *      .js-section-body
 *          .js-question
 *              .js-question-btns
 */
define(['require','jquery','bootstrap', 'dropzone', 'audiojs'], 
    function(require, $, bootstrap, dropzone, audiojs) {
    'use strict';
    
    function changeBadge($question) {
        var $badge = $question.parents('.js-section').find('.js-section-badge');
        var $badgeVal = $badge.find('.js-section-badge-value');
        var $badgeTotal = $badge.find('.js-section-badge-total');
        $badgeVal.text($question.parents('.js-section-body').find('.js-question[data-filled="1"]').length);
        if ($badgeVal.text() === $badgeTotal.text()) {
            $badge.removeClass('text-danger').addClass('text-success');
        }
        var $form = $badge.parents('.js-form');
        if ($form.find('.js-section-badge.text-danger').length == 0) {
            $('#form-save').removeAttr('disabled');
        }
    };
    
    function initForm() {
        if ($('input[name="p1_r1"]').val() !== '') {
            var parts = $('input[name="p1_r1"]').val().split('-');
            $('#year').val(parts[0]);
            $('#month').val(parts[1]);
            $('#day').val(parts[2]);
            // trigger events to set data-filled attributes
            $('#year').trigger('change');
            $('#month').trigger('change');
            $('#day').trigger('change');
        }
        if ($('input[name="p1_r2"]').val() !== '') {
            var parts = $('input[name="p1_r2"]').val().split(':');
            $('#hour1').val(parts[0]);
            $('#minute1').val(parts[1]);
            // trigger change events to set data-filled
            $('#hour1').trigger('change');
            $('#minute1').trigger('change');
        }
        if ($('input[name="p1_r3"]').val() !== '') {
            var parts = $('input[name="p1_r3"]').val().split(':');
            $('#hour2').val(parts[0]);
            $('#minute2').val(parts[1]);
            // trigger change events to set data-filled
            $('#hour2').trigger('change');
            $('#minute2').trigger('change');
        }
        if ($('input[name="p1_r4"]').val() !== '') {
            var parts = $('input[name="p1_r4"]').val().split(':');
            $('#hour3').val(parts[0]);
            $('#minute3').val(parts[1]);
            // trigger change events to set data-filled
            $('#hour3').trigger('change');
            $('#minute3').trigger('change');
        }
        if ($('input[name="operator_fullname"]').val() !== '') {
            $('input[name="operator_fullname"]').trigger('change');
        }
        if ($('input[name="accounter_fullname"]').val() !== '') {
            $('input[name="accounter_fullname"]').trigger('change');
        }
        if ($('input[name="accounter_cafe_fullname"]').val() !== '') {
            $('input[name="accounter_cafe_fullname"]').trigger('change');
        }
        $.each($('input[type=hidden]'), function () {
            var $this = $(this);
            if ($this.val() !== '' && $this.attr('role') === 'checkbox') {
                var $target = $this.parent().find('button[value=' + $this.val() + ']');
                $target.addClass('active');
                $target.html('<i class="glyphicon glyphicon-ok mr5"></i>' + $target.html());
                $target.blur();
                $this.parent().attr('data-filled', '1');
                changeBadge($this.parent());
            }
        });
    }

    function clearQuestions() {
        $.each($('.js-question'), function () {
            var filled = $(this).attr('data-filled');
            if (filled == undefined) {
                $(this).attr('data-filled', '0');
            }
        });
    }

    function initHandlers() {
        // init mouse handlers for checkboxes
        $('.js-question-btns .btn').click(function (evt) {
            evt.preventDefault();
            var $target = $(evt.target);
            var $grp = $target.parent();
            var $old = $grp.find('button.active');
            if ($old.length > 0) {
                $old.removeClass('active');
                $old.find('i').remove();
            }
            $target.addClass('active');
            $target.html('<i class="glyphicon glyphicon-ok mr5"></i>' + $target.html());
            $target.blur();
            
            var $question = $grp.parents('.js-question');
            $question.attr('data-filled', '1');
            var $input = $question.find('input[type=hidden]');
            $input.val($target.val());

            changeBadge($question);
        });
        // init handler for inputs
        $('input.js-question,select.js-question,textarea.js-question').change(function (evt) {
            var $target = $(evt.target);
            if ($target.val() !== '') {
                $target.attr('data-filled', '1');
                changeBadge($target);
            }
        });
        $('.js-question input[type=radio]').change(function (evt) {
            var $target = $(evt.target);
            if ($target.val() !== '') {
                var $question = $target.parents('.js-question');
                $question.attr('data-filled', '1');
                changeBadge($question);
            }
        });
        // init handlers for hours and minutes
        $.each($('select[data-rel-field]'), function () {
            var $target = $(this);
            var $rel = $('#' + $target.data('rel-field'));
            $rel.change(function (e) {
                $target.val($rel.val());
                $target.attr('data-filled', '1');
                changeBadge($target);
            });
        });
        // init min-diff setter
        $('#minute1,#minute3').change(function (evt) {
            var min = $('#minute1').val();
            var max = $('#minute3').val();
            if (/^[\d]+$/.test(min) && /^[\d]+$/.test(max)) {
                $('#min-diff').val(+max - +min);
                $('#min-diff').attr('data-filled', '1');
                changeBadge($('#min-diff'));
            }
        });
    }

    function initAudio() {
        window.audiojs.events.ready(function() {
            var as = window.audiojs.createAll();
        });
    }

    // document.onload
    $(function () {
        // init all questions, setting they not filled
        clearQuestions();
        // init all handlers
        initHandlers();
        // disable save button
        $('#form-save').attr('disabled', 'disabled');
        // set save handler
        $('#form-save').click(function (e) {
            var $target = $(e.target);
            if ($target.attr('disabled') != undefined) {
                return;
            }
            
            e.preventDefault();
            // create JSON and submit form
            $('input[name="p1_r1"]').val($('#year').val() + '-' + $('#month').val() + '-' + $('#day').val());
            $('input[name="p1_r2"]').val($('#hour1').val() + ':' + $('#minute1').val());
            $('input[name="p1_r3"]').val($('#hour2').val() + ':' + $('#minute2').val());
            $('input[name="p1_r4"]').val($('#hour3').val() + ':' + $('#minute3').val());
            $('input[name="p1_r5"]').val($('#min-diff').val());
            
            $('form').submit();
        });
        initForm();
        initAudio();        
    });
});