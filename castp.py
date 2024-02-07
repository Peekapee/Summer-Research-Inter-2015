#!/usr/bin/env python

import re  # Importing the regular expression module for pattern matching
import commands  # Importing the commands module for executing shell commands
from mechanize import Browser  # Importing the Browser module from the mechanize library for web scraping
import mechanize  # Importing the mechanize library for web automation
import time  # Importing the time module to introduce delays
import glob  # Importing the glob module for file system operations
from BeautifulSoup import MinimalSoup  # Importing MinimalSoup for HTML parsing

class PrettifyHandler(mechanize.BaseHandler):
    def http_response(self, request, response):
        if not hasattr(response, "seek"):
            response = mechanize.response_seek_wrapper(response)
        # only use BeautifulSoup if response is html
        if response.info().dict.has_key('content-type') and ('html' in response.info().dict['content-type']):
            soup = MinimalSoup(response.get_data())
            response.set_data(soup.prettify())
        return response

for g in glob.glob('*pdb'):
    print g  # Print the filename
    # Open the file for appending URLs
    fp = open('urls.txt', 'a')
    br = Browser()  # Create a new browser instance
    br = mechanize.Browser(factory=mechanize.RobustFactory())
    br.add_handler(PrettifyHandler())

    # Open the URL of the webpage
    resp = br.open("http://sts.bioe.uic.edu/castp/calculation.php")

    count = 0  # Initialize counter for forms
    for i in br.forms():
        print "------"
        count += 1
    br.select_form(nr=0)
    br.form.set_all_readonly(False)
    br.form.new_control('file', 'userfile', {'value': ''})
    br.form.new_control('text', 'pradius2', {'value': ''})
    br.form.new_control('text', 'visual', {'value': ''})
    br.form.new_control('submit', 'submit_file', {'value': 'Submit'})
    br.form.fixup()

    br.form.add_file(open(g), 'text/plain', g)

    br['pradius2'] = '1.4'
    br['visual'] = 'jmol'

    req = br.submit()
    print req
    print 'done for :', g

    pdb_prefix = g[:-4]

    print br.geturl()
    fp.write(pdb_prefix + '>' + br.geturl() + '\n')
    fp.close()  # Close the file
