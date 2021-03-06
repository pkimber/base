$(function () {
    var dropZoneId = "filedrop-zone";
    var buttonId = "filedrop-click-here";
    var mouseOverClass = "mouse-over";
    var defaultText =  "Drop your file...";

    var dropZone = $("#" + dropZoneId);

    if (dropZone.length) {
      var ooleft = dropZone.offset().left;
      var ooright = dropZone.outerWidth() + ooleft;
      var ootop = dropZone.offset().top;
      var oobottom = dropZone.outerHeight() + ootop;
      var inputFile = dropZone.find("input[type='file']");

      if (buttonId != "") {
          var clickZone = $("#" + buttonId);

          var oleft = clickZone.offset().left;
          var oright = clickZone.outerWidth() + oleft;
          var otop = clickZone.offset().top;
          var obottom = clickZone.outerHeight() + otop;

          $("#" + buttonId).mousemove(function (e) {
              var x = e.pageX;
              var y = e.pageY;
              if (!(x < oleft || x > oright || y < otop || y > obottom)) {
                  inputFile.offset({ top: y - 15, left: x - 160 });
              } else {
                  inputFile.offset({ top: -400, left: -400 });
              }
          });
      }

      dropZone.on("dragover", function(e) {
          e.preventDefault();
          e.stopPropagation();
          dropZone.addClass(mouseOverClass);
          var x = e.originalEvent.pageX;
          var y = e.originalEvent.pageY;

          if (!(x < ooleft || x > ooright || y < ootop || y > oobottom)) {
              inputFile.offset({ top: y - 15, left: x - 100 });
          } else {
              inputFile.offset({ top: -400, left: -400 });
          }
      });

      inputFile.on('change', function(e) {
        var filePath = inputFile.val();
        if (filePath) {
          var fileName = filePath.replace(/^.*[\\\/]/, '');
          $("#filedrop-file-name").text(fileName);
        }
        else {
          var defText = inputFile.data('default-text');
          if (defText === undefined)
            defText = defaultText;
          $("#filedrop-file-name").text(defText);
        }
      });

      dropZone.on("drop", function(e){
          $("#" + dropZoneId).removeClass(mouseOverClass);
      });
    }
});
