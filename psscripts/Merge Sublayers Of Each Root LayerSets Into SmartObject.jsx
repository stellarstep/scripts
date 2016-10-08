app.preferences.rulerUnits = Units.PIXELS;

#include "stdlib.js"

var DOC = app.activeDocument;

main();

function main() {
    for (var a = 0; a < DOC.layerSets.length; a++) {
		var layerSet = DOC.layerSets[a];
        layerSet.visible = true;
        convertLayerSetToSmartObject(layerSet);
    }
}

function convertLayerSetToSmartObject(layerSet){
    for(var i=0; i<layerSet.layers.length; i++){
        var layer = layerSet.layers[i];
        if ( layer.kind == LayerKind.SMARTOBJECT ){
            continue;
        }
        Stdlib.convertToSmartLayer(DOC, layer);
    }
}
