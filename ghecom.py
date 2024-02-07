#!/usr/bin/env python

import re  # Importing the regular expression module to handle pattern matching
import os  # Importing the os module for operating system-related tasks
import glob  # Importing the glob module for file system operations
from mechanize import Browser  # Importing the Browser module from the mechanize library for web scraping

filename = 'links.txt'  # Define the filename for the output file

# Remove the file if it already exists and create a new empty file
if not os.path.exists(filename):
    pass
else:
    os.remove(filename)  
file(filename, 'w').close()

# Open the output file in append mode
f = open(filename, 'a')

# Iterate over all files with the .pdb extension in the current directory
for i in glob.glob('*pdb'):
    br = Browser()  # Create a new browser instance

    # Opening the URL of the webpage
    br.open("http://projects.biotec.tu-dresden.de/metapocket/")

    # Selecting the form to fill
    br.select_form(nr=0)

    # Adding input to the form
    br.form.add_file(open(i), 'text/plain', i)

    # Submitting the form
    req = br.submit()

    # Finding the result link
    result = br.find_link(text_regex=r'http://projects.biotec.tu-dresden.de/metapocket/result.*')

    # Writing the filename and result link to the output file
    f.write(i + ">" + result.text)
    f.write('\n')

    print "done", i  # Print status message

f.close()  # Close the output file

