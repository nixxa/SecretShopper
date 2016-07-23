/**
 * 
 */
define(['jquery', 'dropzone'], function($, dropzone) {
    'use strict';

    var Dropzone = window.Dropzone;

    function initFileUpload() {
        Dropzone.options.myDropzone = { 
            url: "/file/upload",
            method: "post",
            maxFilesize: 10,
            addRemoveLinks: true
        };
        //var mockFile = { name: "banner2.jpg", size: 12345 };
        //myDropzone.options.addedfile.call(myDropzone, mockFile);
        //myDropzone.options.thumbnail.call(myDropzone, mockFile, "http://localhost/test/drop/uploads/banner2.jpg");
    }

    $(document).ready(function () {
        initFileUpload();
    });
});