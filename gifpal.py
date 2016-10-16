# GIFpal v1.1.0
# by John Herndon

import csv
import sys
from PIL import Image

# Command line arguments
if len(sys.argv) < 3:
    sys.exit('Usage: %s <input GIF filename> <palette filename> [output GIF filename]' % sys.argv[0])

# Two dimension array for palette
num_colors, values = 256, 3
palette = [0 for x in range(num_colors * values)]

# RGB value indices
red = 0
green = 1
blue = 2

# Load palette (csv) file
with open(sys.argv[2]) as f:
    reader = csv.reader(f)
    x = 0
    for row in reader:
        palette[x + red] = int(row[red])
        palette[x + green] = int(row[green])
        palette[x + blue] = int(row[blue])
        x += 3

# Load GIF image into memory
img = Image.open(sys.argv[1], "r")

# If it is indeed a gif, change the palette
if img.tile[0][0] == "gif":
    img.putpalette(palette)
    if len(sys.argv) == 4:
        img.save(sys.argv[3])
    else:
        img.save(sys.argv[1] + '_falsecolor.gif')