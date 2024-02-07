#!/usr/bin/env python

import re  # Importing the regular expression module to handle pattern matching
from mechanize import Browser  # Importing the Browser module from the mechanize library for web scraping
import mechanize  # Importing the mechanize library for web automation
import time  # Importing the time module to introduce delays
import glob  # Importing the glob module for file system operations

# Iterate over all files with the .pdb extension in the current directory
for i in glob.glob('*pdb'):
    print i  # Print the filename

    # Open a file to append URLs
    fp = open('urls.txt','a')

    # Create a new browser instance
    br = Browser()
    br = mechanize.Browser(factory=mechanize.RobustFactory())

    # Opening the URL of the webpage
    br.open("http://mspc.bii.a-star.edu.sg/tankp/run_depth.html")

    # Selecting the form to fill
    br.select_form(nr=0)

    # Filling the form with input
    br['pdb_id'] = ''
    br.form.add_file(open(i), 'text/plain', i)
    br.form.set_all_readonly(False)
    req = br.submit()

    print 'done for :', i  # Print status message

    pdb_prefix = i[:-4]  # Extracting prefix from the filename

    temp = br.response().get_data()  # Getting the response data
    print temp  # Print the response data

    matchval = re.findall(r'\w+://.+\.html', temp)  # Find URLs in the response data
    print matchval  # Print the URLs
    print matchval[0]  # Print the first URL found

    # Write the filename and URL to the file
    fp.write(pdb_prefix + ':' + str(matchval[0]) + '\n')
    fp.close()  # Close the file

    # Uncomment the following block to handle downloading of files and time-outs
    # try:
    #     time.sleep(300)
    #     br.open(matchval[0])
    #     pdb_1 = br.find_link(url_regex=r'.*pdb-residue_depth.pdb')
    #     pdb_2 = br.find_link(url_regex=r'.*pdb.binary.pdb')
    #     pdb_3 = br.find_link(url_regex=r'.*pdb.pred.pdb')
    #     pdb_4 = br.find_link(url_regex=r'.*pdb_X.pdb')
    #     baseurl = pdb_1.base_url
    #     baseurl = '/'.join(baseurl.split('/')[0:-1])
    #     url1 = pdb_1.url
    #     url2 = baseurl + "/" + pdb_2.url
    #     url3 = baseurl + "/" + pdb_3.url
    #     url4 = pdb_4.url
    #     print "--------------------"
    #     print url1
    #     print url2
    #     print url3
    #     print url4
    #     file1 = br.retrieve(url1, reqpdb + '_1.pdb')[0]
    #     file2 = br.retrieve(url2, reqpdb + '_2.pdb')[0]
    #     file3 = br.retrieve(url3, reqpdb + '_3.pdb')[0]
    #     file4 = br.retrieve(url4, reqpdb + '_4.pdb')[0]
    #     print 'downloaded:', i
    # except:
    #     print reqpdb, 'Timed Out'

