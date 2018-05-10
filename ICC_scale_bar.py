#!/usr/bin/env python3
from PIL import Image
import glob, os, time, argparse

## Set script such that it can also convert coloured images to BW.
parser = argparse.ArgumentParser()
parser.add_argument('-col','--colour', help='\'bw\' for grayscale image.',
                    type=str, default='col')
args = parser.parse_args()
colour = args.colour

## Informs user about the current working directory as further cd commands
## are relative to this location.
wd = os.getcwd()
## Load the scale bar. In this case the 10x is loaded with a length of 200px
## which corresponds to 100µm in length.
scalebar = Image.open("px200_10_scalebar.tif")

print ("Current directory: %s" % wd)

## Change directory to the location of the actualy merged files. So this script
## should be run after the images have been overlaid.
loc = input("Location: ")
loc = str(loc)
## Just a checkpoint in case user did not put closing '/' at the end of dir.
if loc[-1] != "/":
    loc += "/"
os.chdir(loc)

## Globbing all the merged files
## Using ** instructs function to search recursively
merged = []
for ext in ("*.jpg", "*.png", "*.tiff"):
    merged.extend(glob.glob(os.path.join(loc, ext)))

## For 1320x1040, the following coordinates correspond to bottom-right
## corner with a small (but adequate margin).
position = (1150, 1000)

## Loop through the lists of merged files, add the scale bar and overwrite.
for icc in merged:
    print ("Processing %s" % icc)
    if colour == 'bw':
        image = Image.open(icc).convert('L')
    else:
        image = Image.open(icc)
    image.paste(scalebar, position)
    image.save(icc)

print ("Processed {} images.".format(len(merged)))
print ("Done!")
