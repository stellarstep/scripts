#target photoshop

var doc = app.activeDocument;
var startState = doc.activeHistoryState;       // save for undo
var initialPrefs = app.preferences.rulerUnits; // will restore at end

app.activeDocument.flatten();
$.sleep(1000)
exportIcons([
  {"name": "Icon-27x20", 	"width": 27, "height": 20},
  {"name": "Icon-27x20@2x", "width": 54, "height": 40},
  {"name": "Icon-27x20@3x", "width": 81, "height": 60},

  {"name": "Icon-29",       "size": 29},
  {"name": "Icon-29@2x",    "size": 58},
  {"name": "Icon-29@3x",    "size": 87},

  {"name": "Icon-32x24", 	"width": 32, "height": 24},
  {"name": "Icon-32x24@2x", "width": 64, "height": 48},
  {"name": "Icon-32x24@3x", "width": 96, "height": 72},

  {"name": "Icon-60x45@2x", "width": 120, "height": 90},
  {"name": "Icon-60x45@3x", "width": 180, "height": 135},

  {"name": "Icon-67x50", 	"width": 67, "height": 50},
  {"name": "Icon-67x50@2x", "width": 134, "height": 100},

  {"name": "Icon-74x55@2x", "width": 148, "height": 110},

  {"name": "Icon-1024x768", "width": 1024, "height": 768}
])

function exportIcons(icons){
  try {

    app.preferences.rulerUnits = Units.PIXELS;     // use pixels

    if (doc.width < 1024 && doc.height < 1024) {
      throw "Image is too small!  Must be at least 1024x1024 pixels. Any aspect ratio is allowed.";
    }

    // Folder selection dialog
    var destFolder = Folder.selectDialog( "Choose an output folder");

    if (destFolder == null) {
      // User canceled, just exit
      throw "";
    }

    // Save icons in PNG using Save for Web.
    var sfw = new ExportOptionsSaveForWeb();
    sfw.format = SaveDocumentType.PNG;
    sfw.PNG8 = false; // use PNG-24
    sfw.transparency = true;
    doc.info = null;  // delete metadata

    var icon;
    for (i = 0; i < icons.length; i++)
    {
      icon = icons[i];
      var height = icon.height ? icon.height : icon.size
      var width = icon.width ? icon.width : icon.size

      // Resize the image respecting a larger width or height
      if (doc.width!=width || doc.height!=height){
        if (width == height){
          if (doc.height > doc.width) {
            doc.resizeImage(UnitValue(width,"px"),null,null,ResampleMethod.BICUBIC);
          } else {
            doc.resizeImage(null,UnitValue(height,"px"),null,ResampleMethod.BICUBIC);
          }
        }else{
          doc.resizeImage(UnitValue(width,"px"), UnitValue(height,"px"),null,ResampleMethod.BICUBIC);
        }
        // Crop the canvas to the final width and height
        app.activeDocument.resizeCanvas(UnitValue(width,"px"),UnitValue(height,"px"));
      }

      // Make the default background white
      var bgColor = new SolidColor();
      bgColor.rgb.hexValue = "FFFFFF";
      app.backgroundColor = bgColor;

      var destFileName = icon.name + ".png";

      if ((icon.name == "iTunesArtwork@2x") || (icon.name == "iTunesArtwork"))
      {
        // iTunesArtwork files don't have an extension
        destFileName = icon.name;
      }

      doc.exportDocument(new File(destFolder + "/" + destFileName), ExportType.SAVEFORWEB, sfw);
      doc.activeHistoryState = startState
    }

    alert("iMessage app icons created!");


  }
  catch (exception) {
    // Show degbug message and then quit
  	if ((exception != null) && (exception != ""))
      alert(exception);
   }
  finally {

      app.preferences.rulerUnits = initialPrefs; // restore prefs
  }
}
