CardCreator is a simple Python script to create custom playing cards. It takes text and image data from a csv spreadsheet and combines it all into a single .png file. CardCreator is much more primitive than any image editing program BUT it makes iterating on a card game VERY EASY. Rather than fussing around with every single image layer whenever you want to make a change, just edit the values of the csv and re-run the script. It can even output multiple copies of each card to pdf.

#### NOTES FOR NON-PROGRAMMERS ####
A lot of this looks a lot scarier than it is! But trust me, it might take a little while to setup, but it's easy to run afterwards.

A lot of the notes here require you to use terminal commands. For Windows users, this means going to the start menu, clicking the search bar, typing in "cmd" (without quotes), and hitting return. For Mac users, this means opening Terminal. For Linux, it depends on your setup.

Whenever there are commands, just type them in and press enter. If you see something like /path/to/file, I don't mean that *literally*. Replace everything after the first / with the location of the file (for example: /users/seth/Documents/CardCreator/)

Note that in Windows it doesn't matter whether you uPpeR CAse or not in the terminal, but it does on Mac or Linux.

#### INSTALLATION ####

1. Get Python 2.7
	a. Windows and Mac: https://www.python.org/download/releases/2.7/
	b. Debian and Ubuntu: sudo apt-get install python
	c. Windows: Set the Python path https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7
2. Get pygame
	a. Windows and Mac: https://www.pygame.org/download.shtml
	b. Linux: sudo easy_install fpdf
3. Get fpdf
	a. Windows: easy_install fpdf
	b. Mac and Linux:
		sudo easy_install pygame
		sudo easy_install fdf
3. Linux and Mac: make the script executable.
	cd /path/to/script
	chmod +x CardCreator.py

#### SETUP ####

TO USE THE SAMPLE FILES:
1. Move Sample_Input.zip into Input/
2. Extract Sample_Input.zip
3. Run the CardCreator.csv

TO MAKE YOUR OWN CARDS:
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

#### RUN THE SCRIPT ####
Windows and Mac: in the terminal:
	cd /path/to/script
	python CardCreator.py
Linux and Mac:
	cd /path/to/script
	./CardCreator.py
