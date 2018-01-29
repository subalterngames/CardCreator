#!/usr/bin/python

import pygame
import os
import csv
from shutil import copyfile
from fpdf import FPDF
import getopt
import sys

# Returns the x value for a centered surface, given the background.
def get_surface_centered_x(bg, surface):
    bg_width = bg.get_width()
    surface_width = surface.get_width()
    return (bg_width - surface_width) / 2

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

def wrap_line(text, font, maxwidth):
    done=0
    wrapped=[]

    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        stext = stext.strip()
        if stext != "":
            wrapped.append(stext.strip())
            text=text[nl:]
    return wrapped

def get_wrapped_labels(text, font, maxwidth):
    text_chunks = text.split("\n")
    fonts = []
    for chunk in text_chunks:
        lines = wrap_line(chunk, font, maxwidth)
        for line in lines:
            f = font.render(line, True, black)
            fonts.append(f)
    return fonts

# Init pygame.
pygame.init()

# Set the directories.
# root_dir is the directory of this file.
root_dir = os.path.dirname(os.path.abspath(__file__))
# All input files will be found here.
input_root_dir = root_dir + "/Input/"
# All output files will be found here.
output_root_dir = root_dir + "/Output/"
# Fonts directory
fonts_dir = input_root_dir + "Fonts/"
# Images directory
images_dir = input_root_dir + "Images/"
# Backgrounds directory
images_bg_dir = images_dir + "Backgrounds/"
# Foregrounds directory
images_fg_dir = images_dir + "Foregrounds/"
# Config file path
config_path = root_dir + "config.ini"
# The csv file path
csv_path = input_root_dir + "cards.csv"

# Read the config file
config_file = open(config_path, 'r')
config_lines = config_file.readlines()
config_file.close()
# Parse the lines of the config file
config_data = dict()
for line in config_lines:
    # Split the at the = sign
    split_line = line.split("=")
    # Strip the later value of the escape character.
    split_line[1] = split_line[1].replace('\n', '')
    # Add the data to the dict.
    config_data.update({split_line[0]:split_line[1]})
# Read the data from the config file.
# Font size of the header text.
header_font_size = int(config_data["header_font_size"])
# Filename of the header font.
header_font_file = config_data["header_font"]
# Margin from the top of the card to the header text.
header_pad_y = int(config_data["header_pad_y"])
# Margin from the header text to the foreground image
fg_pad_y = int(config_data["fg_pad_y"])
# Font size of the body text.
body_font_size = int(config_data["body_font_size"])
# Filename of the body font.
body_font_file = config_data["body_font"]
# Padding between the edge of the card and the body text.
body_pad_x = int(config_data["body_pad_x"])
# Padding between the bottom of the foreground image and the body text.
body_pad_y = int(config_data["body_pad_y"])
# Spacing between lines.
body_line_spacing = int(config_data["body_line_spacing"])
# Whether or not to output to pdf.
output_to_pdf = config_data["output_to_pdf"] == '1'
dpi = int(config_data["dpi"])

# Define colors.
black = pygame.Color(0,0,0,255)

# Set the fonts.
header_font = pygame.font.Font(fonts_dir + header_font_file, header_font_size)
body_font = pygame.font.Font(fonts_dir + body_font_file, body_font_size)

# Read the CSV file.
card_rows = []
with open(csv_path, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    count = 0
    for row in reader:
        # Ignore the first row.
        if count > 0:
            card_rows.append(row)
        count += 1
      
# Remove all output files.
filesToRemove = [f for f in os.listdir(output_root_dir) if f.endswith(".png") or f.endswith("pdf")]
for f in filesToRemove:
    os.remove(output_root_dir + f)

card_data = []

# Read the cards.
for card_row in card_rows:
    # Parse the card data.
    header_text = card_row[0]
    body_text = card_row[1]
    fg_image_file = card_row[2]
    bg_image_file = card_row[3]
    num_copies = int(card_row[4])
    filename = card_row[5]

    # Create the card.
    # Load the background.
    bg = pygame.image.load(images_bg_dir + bg_image_file + ".png")
    # Create the header label.
    header_label = header_font.render(header_text, True, black)
    header_label_y = header_pad_y
    header_label_x = get_surface_centered_x(bg, header_label)
    header_pos = (header_label_x, header_label_y)
    # Blit the header onto the background.
    bg.blit(header_label, header_pos)
    # Load the foreground.
    fg = pygame.image.load(images_fg_dir + fg_image_file + ".png")
    # The foreground y position is the y position of the header, the height of the header, and the fg padding.
    fg_y = header_label_y + header_label.get_height() + fg_pad_y
    fg_x = get_surface_centered_x(bg, fg)
    fg_pos = (fg_x, fg_y)
    # Blit the foreground onto the background.
    bg.blit(fg, fg_pos)
    # Create the body labels
    body_width = bg.get_width() - (body_pad_x * 2)
    body_labels = get_wrapped_labels(body_text, body_font, body_width)
    body_x = body_pad_x
    # The body y position starts at the foreground y position plus the foreground's height plus padding.
    body_y = fg_y + fg.get_height() + body_pad_y
    # Blit each body label onto the background.
    for body_label in body_labels:
        body_label_pos = (body_x, body_y)
        bg.blit(body_label, body_label_pos)
        # Update the y position.
        body_y += body_line_spacing
    # Output the card a certain number of times.
    filepath_base = output_root_dir + filename
    # Store the card a given number of times.
    for i in range(num_copies):
        filepath = filepath_base + "_" + str(i) + ".png"
        # Output the filepath.
        pygame.image.save(bg, filepath)
        # Store the data.
        card_data.append((filepath, bg.get_width(), bg.get_height()))
        print "Wrote: " + filepath

# Close pygame.
pygame.quit()

# Render to pdf
if output_to_pdf:
    print "\n###Exporting to PDF###\n"
    # Set the pdf
    pdf = FPDF(orientation = 'P', unit = 'in',format = 'A4')
    pdf.add_page()
    pdf.set_margins(2,10)
    # Get all of the image filepaths.
    images = os.listdir(output_root_dir)
    start_x = 1
    start_y = 1
    x = start_x
    y = start_y

    for card in card_data:
        path = card[0]
        width = card[1] / dpi
        height = card[2] / dpi    
        if x + width >= 8:
            x = start_x
            y += height
            if y > 8:
                y = start_y
                pdf.add_page()
        pdf.image(path, x = x, y = y, w = width, h = height)
        x += width
        print "Added " + path + " to pdf"
    dest = output_root_dir + "cards.pdf"
    pdf.output(dest, "F")
    print "Exported to pdf"
