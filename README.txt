#### INSTALLATION ####

1. Get Python 2.7
	a. Windows and Mac: https://www.python.org/download/releases/2.7/
	b. Debian and Ubuntu: sudo apt-get install python
	c. Windows: Set the Python path https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7
2. Get pygame and fpdf 
	a. Windows: 
		easy_install pygame
		easy_install fpdf
	b. Mac and Linux:
		sudo easy_install pygame
		sudo easy_install fdf
3. Linux and Mac: make the script executable. In the terminal:
	cd /path/to/script
	chmod +x CardCreator.py

########

#### SETUP ####

1. Set up the config file
	header_font_size: Size of the header font
	header_font: File name for the header font (be sure to include the file extension). This file must be in Input/Fonts
	header_y: y (vertical) position of the the header text. 0 = the absolute top of the card.
	fg_y: y position of the foreground image.
	body_font_size: Size of the body font
	body_font: File name for the body font (be sure to include the file extension). This file must be in Input/Fonts
	body_y: y position of the body text.
	body_width_percent: The width of the body text as a percentage of the width of the card. (If this is less than 1, there will be some padding on the sides of the body text.)
	body_line_spacing: Spacing between lines of body text, as a percentage of the font size.
	output_to_pdf: 1 = create a pdf file
	dpi: Image resolution on the pdf
2. Add your foreground images to the foreground folder. They must all be .png
3. Add your background images to the background folder. They must all be .png
4. Add the text cards.csv (don't add file extensions)

########

#### RUN THE SCRIPT ####
Windows and Mac: in the terminal:
	cd /path/to/script
	python CardCreator.py
Linux and Mac:
	cd /path/to/script
	./CardCreator.py
	
########
