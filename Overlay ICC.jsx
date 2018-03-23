//~ Adapted from: https://forums.adobe.com/thread/1222258//~
// To be run on Adobe ExtendScript Toolkit with PS CS6 as the target.

// get the source folder from the user and store in variable
// make a reference to the savedFolder
var sourceFolder = Folder.selectDialog();
// create the folder if it doesn't exists
var savedFolder = new Folder(sourceFolder + '/Merged');
if(!savedFolder.exists) savedFolder.create();
// get an array of red images and store in variable.
// In this case, the array grep is based on the Hoechst/nuclear staining as
// it is the most likely to be present compared to the other Abs
var sourceFiles = sourceFolder.getFiles("*_b.jpg");
// make a loop to process all found sets.
for(var i = 0; i < sourceFiles.length;i++){
  // first, open the blue/reference file and store it as reference
  var blueName = sourceFiles[i].name;
  var blueImage = open(sourceFiles[i]);
  var redName = blueName.replace('_b.jpg','_r.jpg');
  var greenName = blueName.replace('_b.jpg', '_g.jpg');

  // second, define the filenames of the red/A-rabbit and green/A-mouse files
  var redImage = new File(sourceFolder+'/'+redName);
  var greenImage = new File(sourceFolder+'/'+greenName);

  // third, check the conditions if either or both exist, then apply filtering
  // overlayering
  if (redImage.exists && greenImage.exists){
    var redImage = open(redImage)
    applyChannel( charIDToTypeID( "RGB " ) , blueImage.name );
    var greenImage = open(greenImage)
    applyChannel( charIDToTypeID( "RGB " ) , redImage.name );
    // If both files exist, then close the red one after it has been
    // overlaid to the blue one. This way, in the saving function only the
    // active (i.e. merger and green, and subsequently blue) will be closed
    if (redImage.length != 0){
      redImage.close(SaveOptions.DONOTSAVECHANGES)
    }
  } else if (redImage.exists && !greenImage.exists){
      var redImage = open(redImage)
      applyChannel( charIDToTypeID( "RGB " ) , blueImage.name );
    }
    else if (!redImage.exists && greenImage.exists){
      var greenImage = open(greenImage)
      applyChannel( charIDToTypeID( "RGB " ) , blueImage.name );
    }

  // finally, save the results onto another file called merge and close all
  // opened files to conserve memory
  SaveAsTIFF(savedFolder+'/'+blueName.replace(/_b\.jpg$/i,'_merged.tif'),true);
}

function applyChannel( channelID, documentName ){
  // charIDToTypeID( "RGB " )
  // charIDToTypeID( "Rd  " )
  // charIDToTypeID( "Grn " )
  // charIDToTypeID( "Bl  " )
  var desc = new ActionDescriptor();
  var channelsDesc = new ActionDescriptor();
  var ref = new ActionReference();
  ref.putEnumerated( charIDToTypeID( "Chnl" ), charIDToTypeID( "Chnl" ), channelID);
  ref.putProperty( charIDToTypeID( "Lyr " ), charIDToTypeID( "Bckg" ) );
  ref.putName( charIDToTypeID( "Dcmn" ), documentName );
  channelsDesc.putReference( charIDToTypeID( "T   " ), ref );
  channelsDesc.putEnumerated( charIDToTypeID( "Clcl" ), charIDToTypeID( "Clcn" ), charIDToTypeID( "Lghn" ) );
  channelsDesc.putBoolean( charIDToTypeID( "PrsT" ), true );
  desc.putObject( charIDToTypeID( "With" ), charIDToTypeID( "Clcl" ), channelsDesc );
  executeAction( charIDToTypeID( "AppI" ), desc, DialogModes.NO );
};

function SaveAsTIFF( inFileName, inLZW ) {
  var tiffSaveOptions = new TiffSaveOptions();
  if ( inLZW ) {
    tiffSaveOptions.imageCompression = TIFFEncoding.TIFFLZW;
  }
  else {
    tiffSaveOptions.imageCompression = TIFFEncoding.NONE;
  }
  app.activeDocument.saveAs( File( inFileName ), tiffSaveOptions );
  // Close the documents no longer needed
  activeDocument.close(SaveOptions.DONOTSAVECHANGES);
  if (blueImage.length != 0){
    blueImage.close(SaveOptions.DONOTSAVECHANGES)
  }
};
