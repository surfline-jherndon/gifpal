# gifpal
Convert gif palette to a palette of your choice.

### Requirements

Pillow

`pip install pillow`


### Execution

`python gifpal.py <input GIF filename> <palette filename> [output GIF filename]`

### Examples

Replace the weather.gif palette to a false-color palette defined in falsecolor5.pal and output to weather.gif_falsecolor.gif. By default, gifpal.py appends _falsecolor.gif to the end of the input filename.

`python gifpal.py weather.gif falsecolor5.pal`

Replace the weather.gif palette to a false-color palette defined in falsecolor5.pal and output to clouds_falsecolor.gif.

`python gifpal.py weather.gif falsecolor5.pal clouds_falsecolor.gif`

Replace the palette of multiple gif files using the Unix xargs command.

`ls -1 *.gif | xargs -n1 -t -Ifile python gifpal.py file falsecolor5.pal`

### Palette files

Palette files are a simple CSV file. The first color of the palette is the first entry and so on.
