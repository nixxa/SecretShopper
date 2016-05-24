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
 *          .question
 *              .btn-group
 */
define([
    'require',
    'jquery'
], function(require, $) {
    'use strict';
    
    function changeBadge($question) {
        $question.attr('data-filled', '1');
        var $badge = $question.parents('.js-section').find('.js-section-badge');
        var $badgeVal = $badge.find('.js-section-badge-value');
        var $badgeTotal = $badge.find('.js-section-badge-total');
        $badgeVal.text($question.parents('.js-section-body').find('.question[data-filled="1"]').length);
        if ($badgeVal.text() === $badgeTotal.text()) {
            $badge.removeClass('text-danger').addClass('text-success');
        }
    };
    
    // document.onload
    $(function () {
        $.each($('.js-question'), function () {
            $(this).attr('data-filled', '0');
        });
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
            changeBadge($question);
        });
        $('input.js-question').change(function (evt) {
            var $target = $(evt.target);
            if ($target.val() !== '') {
                $target.attr('data-filled', '1');
            }
            changeBadge($target);
        });
    });
});