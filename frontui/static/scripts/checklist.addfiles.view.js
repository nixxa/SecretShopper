/**
 * 
 */
define(['jquery', 'dropzone', 'pica', 'bootstrap'], function($, dropzone, pica, bootstrap) {
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

    function getOrientation(file, callback) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var view = new DataView(e.target.result);
            if (view.getUint16(0, false) != 0xFFD8) return callback(-2);
            var length = view.byteLength, offset = 2;
            while (offset < length) {
                var marker = view.getUint16(offset, false);
                offset += 2;
                if (marker == 0xFFE1) {
                    if (view.getUint32(offset += 2, false) != 0x45786966) return callback(-1);
                    var little = view.getUint16(offset += 6, false) == 0x4949;
                    offset += view.getUint32(offset + 4, little);
                    var tags = view.getUint16(offset, little);
                    offset += 2;
                    for (var i = 0; i < tags; i++)
                        if (view.getUint16(offset + (i * 12), little) == 0x0112)
                            return callback(view.getUint16(offset + (i * 12) + 8, little));
                }
                else if ((marker & 0xFF00) != 0xFF00) break;
                else offset += view.getUint16(offset, false);
            }
            return callback(-1);
        };
        reader.readAsArrayBuffer(file.slice(0, 64 * 1024));
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
        var uid = $('#js-content').data('uid');
        $.each(window.checklist_files, function (index, value) {
            var file = { name: value.filename, size: value.size };
            var thumbnail = 'http://' + window.location.host + '/uploads/' + uid + '/' + value.filename;
            dropzone.emit('addedfile', file);
            if (value.filetype == 'image') {
                dropzone.createThumbnailFromUrl(file, thumbnail);
            } else if (value.filetype == 'document') {
                dropzone.createThumbnailFromUrl(file, '/static/img/excelfile.png');
            }
            dropzone.emit('complete', file);
            //dropzone.options.maxFiles = dropzone.options.maxFiles - 1;
        });

        dropzone.on('removedfile', function (origFile) {
            $.post('/uploads/remove/' + uid + '/' + origFile.name);
        });

        dropzone.on("addedfile", function(origFile) {
            var MAX_WIDTH = 800;
            var MAX_HEIGHT = 800;
            var reader = new FileReader();
            var imageExts = ['jpg', 'JPG', 'jpeg', 'JPEG', 'png', 'PNG', 'gif', 'GIF'];

            // Convert file to img
            reader.addEventListener("load", function (event) {
                var fileExt = origFile.name.split('.').pop();
                if ($.inArray(fileExt, imageExts) < 0) {
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

        var uid = $('#js-content').data('uid');
        var noticeSent = $('#js-content').data('notice-sent');
        $('#js-completed-btn').click(function (evt) {
            if (noticeSent == 'False')
                $('#myModal').modal('show');
            else
                $('#js-content').hide();
        });
        $('#js-modal-complete').click(function (evt) {
            if (noticeSent == 'False') {
                $.post('/checklist/complete/' + uid, { 'author_email': $('#js-author-email').val() }, function (data) {
                    $('#myModal').modal('hide');
                    $('#js-content').hide();
                });
            }
        });
    });
});