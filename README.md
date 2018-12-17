# CardCreator

CardCreator is a simple Python script to create custom playing cards. It takes text and image data from a csv spreadsheet and combines it all into a single .png file. CardCreator is much more primitive than any image editing program BUT it makes iterating on a card game very fast. Rather than fussing around with every single image layer whenever you want to make a change, just edit the values of the csv and re-run the script. It can even output multiple copies of each card to pdf.

## Instructions for non-programmers
A lot of this looks a lot scarier than it is! But trust me, it might take a little while to setup, but it's easy to run afterwards.

A lot of the notes here require you to use terminal commands. For Windows users, this means going to the start menu, clicking the search bar, typing in `powershell` (without quotes), and hitting return. For Mac users, this means opening `terminal`. For Linux, it depends on your setup.

Whenever there are commands, just type them in and press enter. If you see something like `/path/to/file`, I don't mean that *literally*. Replace everything after the first `/` with the location of the file (for example: `/users/seth/Documents/CardCreator/`)

Note that in Windows it doesn't matter whether you `uPpeR CAse` or not in the terminal, but it does on Mac or Linux.

## Installation

1. Get Python 2.7
    a. Windows and Mac: https://www.python.org/download/releases/2.7/
    b. Debian and Ubuntu: sudo apt-get install python
    c. Windows: Set the Python path https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7
2. Get pygame
    a. Windows and Mac: https://www.pygame.org/download.shtml
    b. Linux: `sudo easy_install pygame`
3. Get fpdf:
    a. Windows: `pip install fpdf`
    b. Mac and Linux: `sudo pip install fpdf`
4. Linux and Mac: make the script executable.
```bash
cd /path/to/script
chmod +x CardCreator.py
```

## Setup

### How to use the sample files.
1. Move `Sample_Input.zip` into `Input/`
2. Extract `Sample_Input.zip`

### How to make your own cards.

#### 1. Set up the config file

| Parameter | Description |
| --- | --- |
| `header_font_size` | Size of the header font. |
| `header_font` | File name for the header font (be sure to include the file extension). This file must be in `Input/Fonts` |
| `header_y` | y (vertical) position of the the header text. 0 = the absolute top of the card.|
| `fg_y` | y position of the foreground image.|
| `body_font_size` | Size of the body font |
| ` body_font` | File name for the body font (be sure to include the file extension). This file must be in `Input/Fonts` |
| `body_y` | y position of the body text.
| `body_width_percent` | The width of the body text as a percentage of the width of the card. (If this is less than 1, there will be some padding on the sides of the body text.) |
| `body_line_spacing` | Spacing between lines of body text, as a percentage of the font size. |
| `output_to_pdf` | 1 = create a pdf file |
| `dpi` | Image resolution on the pdf |

#### 2. Add foreground images

Place them in the `Images/Foregrounds` folder. They must all be .png

#### 3. Add background images.

Place them in the `Images/Backgrounds` folder. They must all be .png

#### 4. Add some words to cards.csv

See the example for the correct format. _Don't_ add file extensions (.png) to the image names

## How to run the program

Run the following commands:

| Windows | OS X  and Linux |
| --- | --- |
| `cd /path/to/script` | `cd /path/to/script` |
| `python CardCreator.py` | `./CardCreator.py` |
