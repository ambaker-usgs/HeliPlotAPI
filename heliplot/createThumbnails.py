#!/usr/bin/env python

# ---------------------------------------------------------------
# Author: Alejandro Gonzales
# Filename: createThumbnails.py 
# ---------------------------------------------------------------
# Purpose: Create thumbnails from heli output plots (350x262) 
# ---------------------------------------------------------------
# Methods:
#	   convertImage() - creates thumbnail image 
# ---------------------------------------------------------------
import os, glob, re
import matplotlib.image as img

class CreateThumbnails(object):
	def convertImage(self, thumbpath, plotspath, thumbscale):
		os.chdir(thumbpath)	# cd into thumbnails dir
		if (thumbpath == plotspath):
			print "Image/thumbnail paths match: NOT removing previous thumbnails..."
		else:
			print "Image/thumbnail paths DO NOT match: removing previous thumbnails..."
			thmfiles = glob.glob(thumbpath+"*")
			for f in thmfiles:
				os.remove(f)	# rm tmp thumbnails from Thumbnails dir

		# read from output plots dir
		imgfiles = glob.glob(plotspath+"*")
		print "thumbscale = " + str(thumbscale) + "\n"	
		for f in imgfiles:
			tmp = re.split('/', f)
			tmplen = len(tmp)
			fname = tmp[tmplen-1].strip()	# pull image name
			tmp = re.split('\.', fname)
			fout = tmp[1].strip()	# pull station name
			fout = fout + "_24hr.png"	# append png
			img.thumbnail(f, fout, scale=thumbscale)
