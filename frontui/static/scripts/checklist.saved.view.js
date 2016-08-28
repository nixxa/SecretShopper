/**
 * 
 */
define(['jquery', 'dropzone', 'pica'], function($, dropzone, pica) {
    'use strict';

    var Dropzone = window.Dropzone;
    Dropzone.autoDiscover = false;

    function dataURItoBlob(dataURI) {
        // convert base64/URLEncoded data component to raw binary data held in a string
        var byteString;
        if (dataURI.split(',')[0].indexOf('base64') >= 0)
            byteString = atob(dataURI.split(',')[1]);
        else
            byteString = unescape(dataURI.split(',')[1]);

        // separate out the mime component
        var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

        // write the bytes of the string to a typed array
        var ia = new Uint8Array(byteString.length);
        for (var i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }

        return new Blob([ia], {type:mimeString});
    }

    function base64ToFile(dataURI, origFile) {
        var byteString, mimestring;

        if (dataURI.split(',')[0].indexOf('base64') !== -1) {
            byteString = atob(dataURI.split(',')[1]);
        } else {
            byteString = decodeURI(dataURI.split(',')[1]);
        }

        mimestring = dataURI.split(',')[0].split(':')[1].split(';')[0];

        var content = new Array();
        for (var i = 0; i < byteString.length; i++) {
            content[i] = byteString.charCodeAt(i);
        }

        var newFile = {};
        try {
            newFile = new File(
                [new Uint8Array(content)], origFile.name, { 'type': mimestring }
            );
        } catch (error) {
            // create Blob instead File because in IE constructor for File object doesn't exsist'
            newFile = new Blob(
                [new Uint8Array(content)], { 'type': mimestring }
            );
            newFile.name = origFile.name;
        }

        // Copy props set by the dropzone in the original file
        var origProps = [
            "upload", "status", "previewElement", "previewTemplate", "accepted"
        ];

        $.each(origProps, function (i, p) {
            newFile[p] = origFile[p];
        });

        return newFile;
    }

    function initFileUpload() {
        var dropzone = new Dropzone('.dropzone', { 
            url: "/file/upload",
            method: "post",
            maxFilesize: 20,
            addRemoveLinks: true,
            autoQueue: false,
            parallelUploads: 1
        });
        //var mockFile = { name: "banner2.jpg", size: 12345 };
        //myDropzone.options.addedfile.call(myDropzone, mockFile);
        //myDropzone.options.thumbnail.call(myDropzone, mockFile, "http://localhost/test/drop/uploads/banner2.jpg");

        dropzone.on("addedfile", function(origFile) {
            var MAX_WIDTH = 1200;
            var MAX_HEIGHT = 1200;
            var reader = new FileReader();
            var allowedExts = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF'];

            // Convert file to img
            reader.addEventListener("load", function (event) {
                var fileExt = origFile.name.split('.').pop();
                if ($.inArray(fileExt, allowedExts) < 0) {
                    dropzone.enqueueFile(origFile);
                    return;
                }

                var origImg = new Image();
                origImg.src = event.target.result;

                origImg.addEventListener("load", function (event) {
                    var width = event.target.width;
                    var height = event.target.height;

                    // Don't resize if it's small enough
                    if (width <= MAX_WIDTH && height <= MAX_HEIGHT) {
                        dropzone.enqueueFile(origFile);
                        return;
                    }

                    // Calc new dims otherwise
                    if (width > height) {
                        if (width > MAX_WIDTH) {
                            height *= MAX_WIDTH / width;
                            width = MAX_WIDTH;
                        }
                    } else {
                        if (height > MAX_HEIGHT) {
                            width *= MAX_HEIGHT / height;
                            height = MAX_HEIGHT;
                        }
                    }

                    // Resize
                    
                    var canvas = document.createElement('canvas');
                    canvas.width = width;
                    canvas.height = height;

                    //var ctx = canvas.getContext("2d");
                    //ctx.drawImage(origImg, 0, 0, width, height);
                    pica.resizeCanvas(origImg, canvas, 3, function () {
                        var resizedFile = base64ToFile(canvas.toDataURL(), origFile);

                        // Replace original with resized
                        var origFileIndex = dropzone.files.indexOf(origFile);
                        dropzone.files[origFileIndex] = resizedFile;

                        // Enqueue added file manually making it available for
                        // further processing by dropzone
                        dropzone.enqueueFile(resizedFile);
                    });
                });
            });

            reader.readAsDataURL(origFile);
        });        
    }

    $(document).ready(function () {
        initFileUpload();
    });
});