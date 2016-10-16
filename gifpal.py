#!/usr/bin/env python

# GIFpal by John Herndon

import argparse
import csv
import sys
from PIL import Image

version = '1.2.0'


def verbose(verbosity, message):
    if verbosity:
        print message


output_header = '''\
 ______ _____ _______  _____  _______
|  ____   |   |______ |_____] |_____| |
|_____| __|__ |       |       |     | |_____ %s

Convert a GIF image\'s palette to one of your choosing.
''' % version

output_footer = '''\

examples:

gifpal.py weather.gif falsecolor5.pal

gifpal.py weather.gif falsecolor5.pal output.gif

\000
'''

# Command line arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=output_header, epilog=output_footer)

parser.add_argument('in_file', help='Filename of GIF to be changed.', nargs=1)
parser.add_argument('palette_file', help='Filename of 256-color CSV file containing the palette to use.', nargs=1)
parser.add_argument('out_file', help='Filename of resulting GIF. (optional)', nargs='?')
parser.add_argument('--inverse', action='store_true',
                    help='Inverse palette application. (not recommended)')
parser.add_argument('--show', action='store_true',
                    help='Show resulting image.')
parser.add_argument('--verbose', action='store_true',
                    help='Step by step processing report.')
parser.add_argument('--version', action='store_true', help='Output current version number and exit. ')

args = parser.parse_args()

if args.version:
    sys.exit(output_header)

# Two dimension array for palette
num_colors, values = 256, 3
palette = [0 for x in range(num_colors * values)]

# RGB value indices
red = 0
green = 1
blue = 2

verbose(args.verbose, output_header)

verbose(args.verbose, 'Verbose output requested. (--verbose)')

# Load palette (csv) file
with open(''.join(args.palette_file)) as f:
    reader = csv.reader(f)
    if args.inverse:
        verbose(args.verbose, 'Inverse palette application requested. (--inverse)')
        index = num_colors - 1
    else:
        index = 0

    verbose(args.verbose, 'Loading palette file %s.' % ''.join(args.palette_file))

    for row in reader:
        palette[index + red] = int(row[red])
        palette[index + green] = int(row[green])
        palette[index + blue] = int(row[blue])
        if args.inverse:
            index -= 3
        else:
            index += 3


# Load GIF image into memory
img = Image.open(''.join(args.in_file), "r")

verbose(args.verbose, 'Loading GIF file %s.' % ''.join(args.in_file))

# If it is indeed a gif, change the palette
if img.tile[0][0] == "gif":
    verbose(args.verbose, 'Applying new palette to GIF file %s.' % ''.join(args.in_file))
    img.putpalette(palette)

    if args.out_file:
        verbose(args.verbose, 'Saving new GIF file %s.' % ''.join(args.out_file))
        img.save(''.join(args.out_file))
    else:
        verbose(args.verbose, 'Saving new GIF file %s.' % ''.join(args.in_file) + '_falsecolor.gif')
        img.save(''.join(args.in_file) + '_falsecolor.gif')

    if args.show:
        verbose(args.verbose, 'Displaying image. (--show)')
        img.show()

verbose(args.verbose, 'Process complete.')

sys.exit(0)