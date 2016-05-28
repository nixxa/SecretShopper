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
define([
    'require',
    'jquery'
], function(require, $) {
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
    
    // document.onload
    $(function () {
        // disable save button
        $('#form-save').attr('disabled', 'disabled');
        $('#form-save').click(function (e) {
            var $target = $(e.target);
            if ($target.attr('disabled') !== '') {
                return;
            }
            
            e.preventDefault();
            // create JSON and submit form
        });
        // init all questions, setting they not filled
        $.each($('.js-question'), function () {
            $(this).attr('data-filled', '0');
        });
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

            changeBadge($question);
        });
        // init handler for inputs
        $('input.js-question').change(function (evt) {
            var $target = $(evt.target);
            if ($target.val() !== '') {
                $target.attr('data-filled', '1');
                changeBadge($target);
            }
        });
        // init handler for selects
        $('select.js-question').change(function (evt) {
            var $target = $(evt.target);
            if ($target.val() !== '') {
                $target.attr('data-filled', '1');
                changeBadge($target);
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
    });
});