#!/usr/bin/env python

import re
from mechanize import Browser
import glob

#opening the input file
for i in glob.glob('*pdb'):
	print i
	outputdir = "output"
	br = Browser()
	br.open("http://altair.sci.hokudai.ac.jp/g6/service/pocasa/")
	br.select_form(nr = 0)
	#input as pdb id and selecting the radio button
	br.form['input'] = ['file']
	br.form.add_file(open(i), 'text/plain',i)
	req = br.submit()
	print 'done for :',i
	pdb_prefix = i[:-4]
	#get the url of the output page
	baseurl = 'http://altair.sci.hokudai.ac.jp/g6/service/pocasa'
	br._factory.is_html = True
	for link in br.links():
		d = re.search('.*Pocket_DepthCenters.pdb', link.text)
		e = re.search('.*TopN_pockets.pdb', link.text)
		if d is not None:
			depth_centers = baseurl + link.url[1:]
		if e is not None:
			top_n_centers = baseurl + link.url[1:]
	file1_name = outputdir + "/" + pdb_prefix + '_1.pdb'
	file2_name = outputdir + "/" + pdb_prefix + '_2.pdb'
	file1 = br.retrieve(depth_centers, file1_name)[0]
	file2 = br.retrieve(top_n_centers, file2_name)[0]

