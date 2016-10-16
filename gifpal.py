import sys
import csv
from PIL import Image, ImagePalette

if len(sys.argv) < 3:
    sys.exit('Usage: %s [GIF-filename] [Palette file]' % sys.argv[0])

# Two dimension array for colormap
num_colors, elements = 256, 3
colormap = [0 for x in range(num_colors * elements)]

red = 0
green = 1
blue = 2

# Load colormap file
with open(sys.argv[2]) as f:
    reader = csv.reader(f)
    x = 0
    for row in reader:
        colormap[x + red] = int(row[red])
        colormap[x + green] = int(row[green])
        colormap[x + blue] = int(row[blue])
        x += 3

img = Image.open(sys.argv[1], "r")

if img.tile[0][0] == "gif":
    img.putpalette(colormap)
    img.save(sys.argv[1] + '_fc.gif')
