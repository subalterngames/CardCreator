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

1. Set up the config file (see code for what each line does)
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
