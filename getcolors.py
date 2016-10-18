#!/usr/bin/env python

# GETcolors by John Herndon

import argparse
import sys
from PIL import Image

version = '1.0.0'


def verbose(verbosity, message):
    if verbosity:
        print message


output_header = '''\
 ______ _______ _______ _______  _____          _____   ______ _______
|  ____ |______    |    |       |     | |      |     | |_____/ |______
|_____| |______    |    |_____  |_____| |_____ |_____| |    \_ ______|  %s

Creates a Python data structure from an image's palette for use with GIFPAL.
''' % version

output_footer = '''\

\000
'''

# Command line arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=output_header, epilog=output_footer)

parser.add_argument('in_file', help='Filename of GIF to extract palette from.', nargs=1)
parser.add_argument('palette_file', help='Filename of generated palette data structure.', nargs=1)
parser.add_argument('format', choices=['list', 'listlist', 'dict'],
                    help='Data Struct: List, List of Lists, or Dictionary')
parser.add_argument('--verbose', action='store_true', help='Step by step processing report.')
parser.add_argument('--version', action='store_true', help='Output current version number and exit. ')

args = parser.parse_args()

if args.version:
    sys.exit(output_header)

# RGB value indices
red = 0
green = 1
blue = 2

verbose(args.verbose, output_header)

verbose(args.verbose, 'Verbose output requested. (--verbose)')

# Load GIF image into memory
img = Image.open(''.join(args.in_file), 'r')

verbose(args.verbose, 'Loading GIF file %s.' % ''.join(args.in_file))

# If it is indeed a gif, get the palette
if img.tile[0][0] == "gif":
    verbose(args.verbose, 'Extracting palette from GIF file %s.' % ''.join(args.in_file))
    img_palette = img.getpalette()

else:
    sys.exit(1)

in_palette = [0 for x in range(256 * 3)]
palette_index = 0

for pixel in range(0, img.width):
    pixel_palette_index = img.getpixel((pixel, 0)) * 3
    in_palette[palette_index + red] = img_palette[pixel_palette_index + red]
    in_palette[palette_index + green] = img_palette[pixel_palette_index + green]
    in_palette[palette_index + blue] = img_palette[pixel_palette_index + blue]

    palette_index += 3

verbose(args.verbose, 'Opening palette output file %s.' % ''.join(args.palette_file))
output_file = open(args.palette_file[0], 'w')

python_code = 'def palette():\n\n' \
                '\ttype = "%s"\n\n' % str(args.format)
output_file.write(python_code)

verbose(args.verbose, 'Writing palette output file %s.' % ''.join(args.palette_file))

output_file.write('\tpalette = ')
if args.format == 'list':
    verbose(args.verbose, 'Writing Python list.')
    output_file.write(str(in_palette))

elif args.format == 'listlist':
    new_palette = list()
    for index in range(0, len(in_palette), 3):
        new_palette.append(in_palette[index:index + 3])
    verbose(args.verbose, 'Writing Python list of list.')
    output_file.write(str(new_palette))

elif args.format == 'dict':
    counter = 0
    new_palette = {}
    for index in range(0, len(in_palette), 3):
        new_palette[counter] = in_palette[index:index + 3]
        counter += 1
    verbose(args.verbose, 'Writing Python dictionary.')
    output_file.write(str(new_palette))

output_file.write('\n\n\treturn type, palette\n')
output_file.close()

verbose(args.verbose, 'Process complete.')

sys.exit(0)
