#!/usr/bin/python
# -*- coding: cp1252 -*-

import pygame
import os
import time
import csv
from shutil import copyfile
from fpdf import FPDF
import getopt
import sys
from Differ import OutputDifferences

# Centers text within a box
def CenterText(lbl,x,y,w,h):
    lblw=lbl.get_width()
    lblh=lbl.get_height()

    padx=(w-lblw)/2
    pady=(h-lblh)/2
    pos=[x+padx,y+pady]
    return pos

def CenterTexts(lbls, x, y, w, h):
    lblw = 0
    lblh = 0
    for lbl in lbls:
        lblw += lbl.get_width()
        lblh += lbl.get_height()

    padx=(w-lblw)/2
    pady=(h-lblh)/2

    # Get the first position
    positions=[]
    pos_x = x + padx
    pos_y = y + pady
    for lbl in lbls:
        positions.append((pos_x, pos_y))
        pos_x += lbl.get_width()

    return positions

def Usage():
    args = [("--help","Print this message"), ("-b","Output backs of cards"), ("-c <integer>", "Output only this many cards to PDF"), ("-C", "Print the Crone card"), ("-d", "Output only cards different from those on master"),
            ("-F", "Frogboard only"),("-w", "Witches only"), ("-g", "Grimoire (Print only 1 copy of each card)"), ("-i", "Blit images and symbols"), ("-p","Output to PDF"), ("-s","Blit symbols")]
    for arg in args:
        print '{0:<12} {1:>8}'.format(*arg)

# Get and parse arguments.
try:
    opts, args = getopt.getopt(sys.argv[1:], "FbwpdgsiCc:", ["help"])
except getopt.GetoptError as err:
    print str(err)
    Usage()
    sys.exit(2)
output_backs = False
output_pdf = False
output_only_some_to_pdf = False
num_to_pdf = -1
output_only_diff = False
is_grimoire = False
blit_images = False
blit_symbols = False
print_frog_board = True
print_witch = True
output_crone = False
for o, a in opts:
    if o == "-b":
        output_backs = True
    elif o == "-d":
        output_only_diff = True
    elif o == "-p":
        output_pdf = True
    elif o == "-c":
        output_pdf = True
        output_only_some_to_pdf = True
        num_to_pdf = int(a)
    elif o == "-C":
        output_crone = True
    elif o == "-g":
        is_grimoire = True
    elif o == "-i":
        blit_images = True
        blit_symbols = True
    elif o == "-s":
        blit_symbols = True
    elif o == '-w':
        print_frog_board = False
    elif o == '-F':
        print_witch = False
    elif o == "--help":
        Usage()
        sys.exit(2)

black = pygame.Color(0,0,0,255)
white = pygame.Color(255,255,255,255)

# Get the directory of templates.
template_dir = os.path.dirname(os.path.abspath(__file__)) + "/Templates/"

font_dir = os.path.dirname(os.path.abspath(__file__)) + "/Fonts/"

dist_dir = os.path.dirname(os.path.abspath(__file__)) + "/dist/"

crone_dir = os.path.dirname(os.path.abspath(__file__)) + "/Crone/"

urw_din_dir = "din/urw/URW DIN Complete/"
bouwsma_dir = "[CAN] Bouwsma/"

# Create the dist directory if it does not exist.
if not os.path.isdir(dist_dir):
    os.makedirs(dist_dir)

data_dir = os.path.dirname(os.path.abspath(__file__)) + "/Data/"

# Image for 4-5 players
four_five_players = pygame.image.load(template_dir + "4-5_players.png")

# Font definitions
junction_bold = "Junction-bold.otf"
junction_regular = "Junction-regular.otf"
junction_light = "Junction-light.otf"
goudy_medieval = "Goudy Mediaeval Regular.ttf"
im_fell_regular = "FeENrm28C.otf"
im_fell_italic = "FeENit27C.otf"
prociono = "Prociono.otf"
molot = "Molot.otf"
spartan = "LeagueSpartan-Bold.otf"
audimat_bold = "AUDIMB__.ttf"
audimat = "AUDIMRG_.ttf"
macondo = "Macondo-Regular.ttf"
monopol_semibold = "Monopol SemiBold.ttf"
monopol_medium = "Monopol Medium.ttf"
ff_din_conds_black = "din/ff-din-pro-condensed-black-5963be75a40cf.otf"
ff_din_conds_bold = "din/ff-din-pro-condensed-bold-5963bd5a11142.otf"
ff_din_conds_medium = "din/ff-din-pro-condensed-medium-italic-5963be493257e.otf"
ff_din_conds_regular = "din/ff-din-pro-condensed-regular-5963be65c84d0.otf"
pf_din_text_medium = "din/pf-din-text-pro-medium-5963d1bd79344.otf"
pf_din_text_bold ="din/pf-din-text-pro-bold-5963d32da2180.otf"
urw_din_conds_demi = urw_din_dir + "URW++ - URWDINCond-Demi.otf"
urw_din_semi_conds_medium = urw_din_dir + "URW++ - URWDINSemiCond-Medium.otf"
urw_din_semi_conds_bold = urw_din_dir + "URW++ - URWDINSemiCond-Bold.otf"
bouwsma_text_bold = bouwsma_dir + "Bouwsma Text Bold.otf"
bouwsma_text_semi_bold = bouwsma_dir + "Bouwsma Text SemiBold.ttf"
bouwsma_text_medium = bouwsma_dir + "Bouwsma Text Medium.otf"
bouwsma_text_regular = bouwsma_dir + "Bouwsma Text.ttf"
of_font = "HEXaDecimateLigature-Regular.otf"

witch_combo_font_file = bouwsma_text_semi_bold
witch_effect_font_file = bouwsma_text_regular
witch_header_font_file = bouwsma_text_regular
frogboard_header_font_file = urw_din_conds_demi
frogboard_effect_font_file = urw_din_semi_conds_medium
frogboard_combo_font_file = urw_din_semi_conds_bold
frogboard_four_five_font_file = urw_din_semi_conds_bold

# How many copies of each card should be printed.
copies ={'WITCH':3,'SIGIL':4,'OPERATION':1}

def GetCards():
    rows = []
    data_path = data_dir + "cards.csv"
    #read CSV data
    with open(data_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        count = 0
        for row in reader:
            if count > 0:
                rows.append(row)
            count += 1
    return rows

cards = []
if output_only_diff:
    cards = OutputDifferences()
else:
    cards = GetCards()

pygame.init()

def GetCardByName(name):
    # Make sure we have all of the cards.
    rows = cards
    if output_only_diff:
        rows = GetCards()
    for card in rows:
        if card[0] == name.strip():
            return card
    return None

def GetCardColor(card):
    if card[7] == "":
        return black
    else:
        return pygame.Color(int(card[7]), int(card[8]), int(card[9]))

def truncline(text, font, maxwidth):
        real=len(text)
        stext=text
        l=font.size(text)[0]
        cut=0
        a=0
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)
            done=0
        return real, done, stext

def wrapline(text, font, maxwidth):
    done=0
    wrapped=[]

    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        stext = stext.strip()
        if stext != "":
            wrapped.append(stext.strip())
            text=text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

def GetFrogBoardFonts(text, font):
    lines = wrapline(text, font, text_box_width)
    fonts = []
    for line in lines:
        f = font.render(line, True, black)
        fonts.append(f)
    return fonts

# Load the fonts
witch_header_font = pygame.font.Font(font_dir + witch_header_font_file, 54)
witch_of_font_header = pygame.font.Font(font_dir + of_font, 54)
frogboard_header_font = pygame.font.Font(font_dir + frogboard_header_font_file, 82)
witch_effect_font = pygame.font.Font(font_dir + witch_effect_font_file, 30)
frogboard_effect_font = pygame.font.Font(font_dir + frogboard_effect_font_file,40)
witch_combos_font = pygame.font.Font(font_dir + witch_combo_font_file, 30)
witch_combos_of_font = pygame.font.Font(font_dir + of_font, 30)
frogboard_combos_font = pygame.font.Font(font_dir + frogboard_combo_font_file, 40)
frogboard_four_five_font = pygame.font.Font(font_dir + frogboard_four_five_font_file, 40)

# Line spacing defines
line_height_witch = 14
line_height_frog = 14
line_height_double_witch = 24
line_height_double_frog = 24

text_box_width = 680

def BlitImageGeneric(surface, image_name, image_pos, directory):
    image_path = os.path.dirname(os.path.abspath(__file__)) + directory + image_name + ".png"
    if os.path.isfile(image_path):
        image = pygame.image.load(image_path)
        surface.blit(image, image_pos)
    return surface


# Blit an image to the surface.
def BlitImage(surface, image_name):
    directory = "/Images/Final/"
    image_path = os.path.dirname(os.path.abspath(__file__)) + directory + image_name + ".png"
    if not os.path.isfile(image_path):
        directory = "/Images/Placeholder/"
    return BlitImageGeneric(surface, image_name, (58, 148), directory)

def BlitIconLarge(surface, image_name, is_witch_jess):
    if is_witch_jess:
        pos = (30, 10)
    else:
        pos = (30, 20)
    return BlitImageGeneric(surface, image_name, pos, "/Ikons/")

def BlitIconSmall(surface, image_name, x, y):
   return BlitImageGeneric(surface, image_name, (x, y), "/Ikons/")

def BlitComboTextWithIcon(background, combos_font, name, x, y, text):
    card = GetCardByName(name)
    color = black
    icon_name = ""
    if card != None and card[6] != "":
        icon_name = card[6] + "_small"
        color = GetCardColor(card)
    # Icon
    background = BlitIconSmall(background, icon_name, x, y)
    x += 80

    if " OF " in text:
        words = text.split(" OF ")
        labels = []
        first = combos_font.render(words[0] + " ", True, color)
        background.blit(first, (x, y))
        x += first.get_width()
        of = witch_combos_of_font.render("n", True, color)
        background.blit(of, (x, y))
        x += of.get_width()
        second = combos_font.render(" " + words[1], True, color)
        background.blit(second, (x, y))
        x += second.get_width() + 8
        return background, x
    else:
        # name
        name_txt = combos_font.render(text, True, color)
        # Blit the name. Offset the y a bit.
        background.blit(name_txt, (x, y))
        x += name_txt.get_width() + 8
    return background, x

# Blender color mode for the color of the card.
def PrintSpecialColoring(background, row):
    hsla = GetCardColor(row).hsla
    for y in range(147, 1415):
        for x in range(828):
            # Exclude the inner box
            if x > 53 and x < 770 and y > 789 and y < 1355:
                continue
            pixel = background.get_at((x,y))
            pixel.hsla = (hsla[0], hsla[1], pixel.hsla[2], pixel.hsla[3])
            background.set_at((x,y), pixel)

    return background

def GetHeader(is_witch, header_text, row, header_y, header_font):
    if not is_witch:
        # Center FrogBoard text.
        header = header_font.render(header_text, True, GetCardColor(row))
        header_pos = CenterText(header, 0, header_y, 831, 54)
        return [(header, header_pos)]
    elif " OF " in header_text:
        color = GetCardColor(row)
        # Include "of" in between the two words.
        words = header_text.split(" OF ")
        labels = []
        labels.append(header_font.render(words[0] + " ", True, color))
        labels.append(witch_of_font_header.render("n", True, color))
        labels.append(header_font.render(" " + words[1], True, color))
        positions = CenterTexts(labels, 0, 120, 831, 54)
        headers = []
        for lbl, position in zip(labels, positions):
            headers.append((lbl, position))
        return headers
    else:
        # If there is no "of", center text.
        header = header_font.render(header_text, True, GetCardColor(row))
        header_pos = CenterText(header, 0, header_y, 831, 54)
        return [(header, header_pos)]


def PrintCard(row):
    num_witch = 0
    num_frog = 0
    is_witch = row[3] == 'WITCH'
    if not is_witch and not print_frog_board:
        return num_witch, num_frog
    elif is_witch and not print_witch:
        return num_witch, num_frog
    bg_filename = ""

    # Check if there is a full-image card thast Jess made.
    image_jess_path = os.path.dirname(os.path.abspath(__file__)) + "/Images/Jess/" + row[5] + ".png"
    image_filipe_path = os.path.dirname(os.path.abspath(__file__)) + "/Images/Filipe/" + row[5] + ".png"
    is_frog_filipe = os.path.isfile(image_filipe_path)
    is_witch_jess = os.path.isfile(image_jess_path)

    if is_witch_jess:
        background = pygame.image.load(image_jess_path)
    elif is_frog_filipe:
        background = pygame.image.load(image_filipe_path)
    else:
        # Get the correct background.
        if is_witch:
            bg_filename = "tarot_witch.png"
        elif row[3] == "OPERATION":
            bg_filename = "tarot_operation.png"
        else:
            bg_filename = "tarot_frog.png"
        # Load the background.
        background = pygame.image.load(template_dir + bg_filename)
        # Color the card to the background.
        if is_witch:
            background = PrintSpecialColoring(background,row)

    # Render the labels
    header_font = witch_header_font
    effect_font = witch_effect_font
    combos_font = witch_combos_font
    if not is_witch:
        header_font = frogboard_header_font
        effect_font = frogboard_effect_font
        combos_font = frogboard_combos_font

    header_text = row[0]
    # If this is a witch card, the header is capitalized.
    if is_witch:
        header_text = row[0].upper()

    if is_witch_jess:
        header_y = 15
    elif is_frog_filipe:
        header_y = 45
    else:
        header_y = 55
    headers = GetHeader(is_witch, header_text, row, header_y, header_font)

    for h in headers:
        background.blit(h[0], h[1])

    # Get the rules and the combos.
    combos = row[1].split('\n')
    rules = row[2].split('\n')
    c_x = 90
    if is_witch_jess or is_frog_filipe:
        c_y = 950
    else:
        c_y = 840
    # When wrapping lines, compensate for the icon width.
    icon_offset = 0
    if is_witch:
        icon_offset = 70
    line_height = line_height_frog
    if is_witch:
        line_height = line_height_witch

    # Add a marker for 4-5 players, if applicable.
    is_4_5_only = row[10] == "1"
    if (is_4_5_only):
        four_five_font = frogboard_four_five_font.render("4" + u'\u2013' + "5 Witches", True, black)
        four_five_pos = CenterText(four_five_font, 0, c_y - four_five_font.get_height(), 831, 70)
        background.blit(four_five_font, four_five_pos)
        c_y += four_five_font.get_height() + line_height

    for c, r in zip(combos,rules):
        # Add a space after the combo
        if (c != ""):
            c += " "

        # Render the combo starter.
        combo_starter = c
        # Print "Otherwise"
        if is_witch and c.strip() == "Otherwise":
            combo_starter = c.upper()
        c_font = combos_font.render(combo_starter, True, black)

        line_x = 0
        start_x = c_x
        # If this is a witch card, offset starting x from the icon.
        if is_witch:
            start_x = c_x + icon_offset
        # Blit the first line with the icon.
        if is_witch and blit_symbols and c.strip() != "Otherwise":
            background, line_x = BlitComboTextWithIcon(background, combos_font, c, c_x, c_y, c.upper())
        else:
            # The witch combo fonts should be slightly lower.
            combo_y = c_y
           # if is_witch:
             #   combo_y += 4
            # Blit the combo
            c_x_x = c_x + icon_offset
            # If this is "Otherwise", indent a little more.
            if is_witch:
                c_x_x += 8
            c_pos = (c_x_x, combo_y)
            background.blit(c_font, c_pos)
            # Get the wrapped lines.
            line_x = c_x_x + c_font.get_width()
        # Get the maximum x value on the card (for line wrapping)
        max_x = text_box_width - line_x + icon_offset
        if not is_witch:
            max_x += 60
        lines = wrapline(r, effect_font, max_x)
        # Blit the first line.
        first_line = lines[0]
        r_font = effect_font.render(first_line, True, black)
        r_pos =  (line_x, c_y)
        # Blit the line
        background.blit(r_font, r_pos)
        c_y += r_font.get_height() + line_height
        # Blit the other lines.
        r = r.replace(first_line, "")

        if is_witch:
            start_x += 8

        lines_width = text_box_width - c_x
        if not is_witch:
            lines_width = text_box_width

        lines = wrapline(r, effect_font, lines_width)
        for line in lines:
            r_font = effect_font.render(line, True, black)
            r_pos =  (start_x, c_y)
            # Blit the line
            background.blit(r_font, r_pos)
            c_y += r_font.get_height() + line_height
        line_height_double = line_height_double_frog
        if is_witch:
            line_height_double = line_height_double_witch
        c_y += line_height_double

    # Output those files.
    prefix = "f_"
    if row[3] == "WITCH":
        prefix = "w_"
    if blit_images and not is_witch_jess and not is_frog_filipe:
        # Blit the image
        background = BlitImage(background, row[5])
    if blit_symbols:
        # Blit the icon.
        background = BlitIconLarge(background, row[6] + "_large", is_witch_jess)
    # Get the correct number of copies. A grimoire has only 1 copy.
    num_copies = copies[row[3]]
    if is_grimoire:
        num_copies = 1
    # Print multiple copies.
    for i in range(num_copies):
        if row[3] == "WITCH":
            num_witch += 1
        else:
            num_frog += 1
        filename = dist_dir + prefix + row[4] + "_" + str(i) + ".png"
        pygame.image.save(background, filename)
    print row[0]
    return num_witch, num_frog

# Remove all dist files.
filesToRemove = [f for f in os.listdir(dist_dir) if f.endswith(".png") or f.endswith("pdf")]
for f in filesToRemove:
    os.remove(dist_dir + f)

num_witch = 0
num_frog = 0
for card in cards:
    w, f = PrintCard(card)
    num_witch += w
    num_frog += f
print "Number of witch cards: " + str(num_witch) + "\nNumber of frog cards: " + str(num_frog)

pygame.quit()

# Output the backs of cards. There should be a back image for ever card.
def PrintBacks():
    # Get copies of the backs of cards.
    witch_back_template = template_dir + "tarot_witch_back.png"
    frog_back_template = template_dir + "tarot_frog_back.png"
    for i in range(num_witch):
        filename = "w__back_" + str(i) + ".png"
        copyfile(witch_back_template, dist_dir + filename)
    for i in range(num_frog):
        filename = "f__back_" + str(i) + ".png"
        copyfile(frog_back_template, dist_dir + filename)
    print "Created backs of cards"

# Print the Crone card. Just copy the images to the dist directory.
def PrintCrone():
    right_file = "crone_right.png"
    left_file = "crone_left.png"
    right_path = crone_dir + right_file
    left_path = crone_dir + left_file
    copyfile(right_path, dist_dir + right_file)
    copyfile(left_path, dist_dir + left_file)
    print "Created Crone card"

# Export to pdf.
def ToPDF():
    print "\n###Exporting to PDF###\n"
    card_w = 70
    card_h = 120
    pdf = FPDF(orientation = 'L', unit = 'mm',format = 'A3')
    pdf.add_page()
    pdf.set_margins(2,10)
    # Get all of the images.
    images = os.listdir(dist_dir)

    num_total = len(images)
    if output_only_some_to_pdf:
        num_total = num_to_pdf
    start_x = 12
    start_y = 12
    rows = 2
    cols = 5

    current_row = 0
    current_col = 0
    for i, image in zip(range(num_total), images):
        x = start_x + (70 * current_col)
        y = start_y + (120 * current_row)
        # Print to pdf.
        image_path = dist_dir + image
        pdf.image(image_path, x = x, y = y, w = card_w, h = card_h)
        print "Added image " + image + " " + str(x) + " " + str(y)

        current_col += 1
        if current_col > cols - 1:
            current_col = 0
            current_row += 1

        if current_row > rows - 1:
            current_row = 0
            current_col = 0
            print "New page"
            pdf.add_page()

    filename = "cards.pdf"
    if is_grimoire:
        filename = "grimoire.pdf"
    dest = dist_dir + filename
    pdf.output(dest, "F")
    print "Exported to PDF"

if output_backs:
    PrintBacks()
if output_crone:
    PrintCrone()
if output_pdf:
    ToPDF()
