#!/usr/bin/env python

# ----------------------------------------------------------------
# Author: Alejandro Gonzales
# Filename: readPrestation.py 
# ----------------------------------------------------------------
# Purpose: Reads in stationNames.txt file and prestation.cfg
# 	   and creates a station.cfg file to be used by main
#	   HeliPlot programs 
# ----------------------------------------------------------------
# Methods:
#	* readConfig() - read/parse prestation.cfg file
#	* storeStations() - store stations/locations in lists
#	* writeDefaultVariables() - write defaults to station.cfg
#	* writePaths() - write paths to station.cfg
#	* writeFilterVariables() - write filters to station.cfg
#	* writeStations() - write station list to station.cfg
# ----------------------------------------------------------------
import os, re, string

class ReadPrestation(object):
	def __init__(self):
		# ---------------------------------
		# Open and read list of stations
		# ---------------------------------
		#os.chdir('/home/asluser/HeliPlotAPI/')	
		home = os.getcwd()	
		os.chdir(home)	
		self.stations = []	# list of stations
		self.stationlist = []	# list for edited station names
		self.locations = []	# list of locations for each station
		self.skipstations = []	# list of network/stations with len > 6
		fin = open('stationNames.txt', 'r')
		for line in fin:
			count = 0
			line = line.strip()
			for i in range(len(line)):
				if line[i] == ' ':
					count = count + 1
					if count == 2:
						station = line[0:i].strip()
						station = station.replace(" ", "")
						location = line[i:len(line)].strip()
						self.stations.append(station)
						self.locations.append(location)
					elif count > 2:
						break
		fin.close()	# close stationNames.txt

	def storeStations(self):
		# --------------------
		# Store station names
		# --------------------
		stationlen = len(self.stations)
		for i in range(stationlen):
			stringlen = len(self.stations[i])
			
			# Channel/location IDs for station exceptions
			if self.channelexc.has_key(self.stations[i]) == 1:
				channelID = self.channelexc[self.stations[i]]
			else:
				channelID = self.channelID
			if self.locationexc.has_key(self.stations[i]) == 1:
				locationID = self.locationexc[self.stations[i]]
			else:
				locationID = self.locationID
			
			# Station IDs have a max size of 6, if (size < 6) 
			# then pad station ID with (6-size+1) spaces
			if stringlen == 5:
				tmpstation = self.stations[i] + "  " + channelID + locationID +\
						"\t" + self.locations[i]
				self.stationlist.append(tmpstation)
			elif stringlen == 6:
				tmpstation = self.stations[i] + " " + channelID + locationID +\
						"\t" + self.locations[i]
				self.stationlist.append(tmpstation)
			else:
				self.skipstations.append(self.stations[i])
	
	def writeDefaultVariables(self):
		# ---------------------------
		# Server variables can change
		# ---------------------------
		print "\nwriteDefaultVariables()"	
		self.cfgout = open('station.cfg', 'w')	# closed in writeStations()
		cfgout = self.cfgout
		cfgout.write(self.cfgcmt)
		cfgout.write("\n")
		cfgout.write("# Default variables\n")
		cfgout.write(self.duration + "\t" + self.durationcmt + "\n")
		cfgout.write(self.ipaddress + "\t" + self.ipaddresscmt + "\n")
		cfgout.write(self.httpport + "\t" + self.httpportcmt + "\n")
		cfgout.write(self.magnification_default + "\t" + self.magnification_defaultcmt + "\n")
		cfgout.write(self.resx + "\t" + self.resxcmt + "\n")
		cfgout.write(self.resy + "\t" + self.resycmt + "\n")
		cfgout.write(self.pix + "\t" + self.pixcmt + "\n")
		cfgout.write(self.imgformat + "\t" + self.imgformatcmt + "\n")
		cfgout.write(self.thumbscale + "\t" + self.thumbscalecmt + "\n")	
		cfgout.write(self.vertrange + "\t" + self.vertrangecmt + "\n")
		cfgout.write(self.cwbwait + "\t" + self.cwbwaitcmt + "\n")
		cfgout.write(self.cwbattempts + "\t" + self.cwbattemptscmt + "\n")
		cfgout.write(self.cwbretrysleep + "\t" + self.cwbretrysleepcmt + "\n\n")
	
	def writePaths(self):
		# --------------------------------------------------	
		# Create file paths for SeedFiles and OutputPlots
		# Print station info/location to config file
		# --------------------------------------------------	
		print "writePaths()"	
		cfgout = self.cfgout	
		if not os.path.exists(self.seedpath):
			print self.seedpath + " DNE, creating path..."
			os.makedirs(self.seedpath)
		if not os.path.exists(self.plotspath):
			print self.plotspath + " DNE, creating path..."
			os.makedirs(self.plotspath)
		if not os.path.exists(self.thumbpath):
			print self.thumbpath + " DNE, creating path..."
			os.makedirs(self.thumbpath)
		if not os.path.exists(self.helihtmlpath):
			print self.helihtmlpath + " DNE, creating path..."
			os.makedirs(self.helihtmlpath)
		cfgout.write("# Directory paths for seedfiles, plots, responses, etc.\n")
		cfgout.write(self.seedpath + "\t" + self.seedpathcmt + "\n")
		cfgout.write(self.plotspath + "\t" + self.plotspathcmt + "\n")
		cfgout.write(self.thumbpath + "\t" + self.thumbpathcmt + "\n")	
		cfgout.write(self.helihtmlpath + "\t" + self.helihtmlpathcmt + "\n")	
		cfgout.write(self.cwbquery + "\t" + self.cwbquerycmt + "\n")
		cfgout.write(self.resppath + "\t" + self.resppathcmt + "\n\n")

	def writeFilterVariables(self):
		print "writeFilterVariables()"	
		cfgout = self.cfgout
		cfgout.write("# Filter Designs (unique to channelID)\n")
		cfgout.write("# *NOTE: Filter frequencies will change depending\n")
		cfgout.write("# on the channel being used (i.e. higher/lower freq channels)\n")

		# EHZ Filter Design
		cfgout.write(self.EHZfiltertype + "\t" + self.EHZfiltertypecmt + "\n")
		cfgout.write(self.EHZhpfreq + "\t" + self.EHZhpfreqcmt + "\n")
		cfgout.write(self.EHZnotchfreq + "\t" + self.EHZnotchfreqcmt + "\n\n")

		# BHZ Filter Design
		cfgout.write(self.BHZfiltertype + "\t" + self.BHZfiltertypecmt + "\n")
		cfgout.write(self.BHZbplowerfreq + "\t" + self.BHZbplowerfreqcmt + "\n")
		cfgout.write(self.BHZbpupperfreq + "\t" + self.BHZbpupperfreqcmt + "\n\n")

		# LHZ Filter Design
		cfgout.write(self.LHZfiltertype + "\t" + self.LHZfiltertypecmt + "\n")
		cfgout.write(self.LHZbplowerfreq + "\t" + self.LHZbplowerfreqcmt + "\n")
		cfgout.write(self.LHZbpupperfreq + "\t" + self.LHZbpupperfreqcmt + "\n\n")

		# VHZ Filter Design
		cfgout.write(self.VHZfiltertype + "\t" + self.VHZfiltertypecmt + "\n")
		cfgout.write(self.VHZlpfreq + "\t" + self.VHZlpfreqcmt + "\n\n")

		# Write magnification exception list for specific stations
		cfgout.write(str(self.magnificationexc) + "\t" + self.magnificationexccmt + "\n\n")

	def writeStations(self):
		print "writeStations()\n"
		cfgout = self.cfgout
		cfgout.write(self.stationcmt + "\n")
		for i in range(len(self.stationlist)):
			cfgout.write(self.stationlist[i] + "\n")
		self.cfgout.close()	# close station.cfg

	def readConfig(self):
		# ---------------------------------------------
		# Read in data from prestation.cfg, this file
		# contains channel/location, datetime/duration, etc.
		# ---------------------------------------------
		fin = open('prestation.cfg', 'r')
		for line in fin:
			if (line[0] != '#'):
				if line != '\n':
					newline = re.split('=', line)
					# Default variables
					# ---------------------------
					if "channelID" in newline[0]:
						self.channelID = newline[1].strip()
					elif "locationID" in newline[0]:
						self.locationID = newline[1].strip()
					elif "duration" in newline[0]:
						self.duration = newline[1].strip()
					elif "ipaddress" in newline[0]:
						self.ipaddress = newline[1].strip()
					elif "httpport" in newline[0]:
						self.httpport = newline[1].strip()
					elif "magnification_default" in newline[0]:
						self.magnification_default = newline[1].strip()
					elif "resx" in newline[0]:
						self.resx = newline[1].strip()
					elif "resy" in newline[0]:
						self.resy = newline[1].strip()
					elif "pix" in newline[0]:
						self.pix = newline[1].strip()
					elif "imgformat" in newline[0]:
						self.imgformat = newline[1].strip()
					elif "thumbscale" in newline[0]:
						self.thumbscale = newline[1].strip()
					elif "vertrange" in newline[0]:
						self.vertrange = newline[1].strip()
					elif "cwbwait" in newline[0]:
						self.cwbwait = newline[1].strip()
					elif "cwbattempts" in newline[0]:
						self.cwbattempts = newline[1].strip()
					elif "cwbretrysleep" in newline[0]:
						self.cwbretrysleep = newline[1].strip()
					
					# System paths
					# ---------------------------
					elif "cwbquery" in newline[0]:
						self.cwbquery = newline[1].strip()
					elif "resppath" in newline[0]:
						self.resppath = newline[1].strip()
					elif "seedpath" in newline[0]:
						self.seedpath = newline[1].strip()
					elif "plotspath" in newline[0]:
						self.plotspath = newline[1].strip()
					elif "thumbpath" in newline[0]:
						self.thumbpath = newline[1].strip()
					elif "helihtmlpath" in newline[0]:
						self.helihtmlpath = newline[1].strip()
					
					# Filter Designs
					# ---------------------------
					elif "EHZfiltertype" in newline[0]:
						self.EHZfiltertype = newline[1].strip()
					elif "EHZhpfreq" in newline[0]:
						self.EHZhpfreq = newline[1].strip()
					elif "EHZnotchfreq" in newline[0]:
						self.EHZnotchfreq = newline[1].strip()
					elif "BHZfiltertype" in newline[0]:
						self.BHZfiltertype = newline[1].strip()
					elif "BHZbplowerfreq" in newline[0]:
						self.BHZbplowerfreq = newline[1].strip()
					elif "BHZbpupperfreq" in newline[0]:
						self.BHZbpupperfreq = newline[1].strip()
					elif "LHZfiltertype" in newline[0]:
						self.LHZfiltertype = newline[1].strip()
					elif "LHZbplowerfreq" in newline[0]:
						self.LHZbplowerfreq = newline[1].strip()
					elif "LHZbpupperfreq" in newline[0]:
						self.LHZbpupperfreq = newline[1].strip()
					elif "VHZfiltertype" in newline[0]:
						self.VHZfiltertype = newline[1].strip()
					elif "VHZlpfreq" in newline[0]:
						self.VHZlpfreq = newline[1].strip()

					# Exception lists
					# ---------------------------
					elif "rmnetwork" in newline[0]:
						self.rmnetwork = newline[1].strip()
					elif "channelexc" in newline[0]:
						self.channelexc = newline[1].strip()
					elif "locationexc" in newline[0]:
						self.locationexc = newline[1].strip()
					elif "magnificationexc" in newline[0]:
						self.magnificationexc = newline[1].strip()
		fin.close()	# close prestation.cfg

		# Split/store exception channels, locations, magnifications
		tmpchan = re.split(',', self.channelexc)	# split/store channelexc
		self.channelexc = {}
		for i in range(len(tmpchan)):	
			tmpexc = re.split(':', tmpchan[i])
			self.channelexc[tmpexc[0].strip()] = tmpexc[1].strip()

		tmploc = re.split(',', self.locationexc)	# split/store locationexc
		self.locationexc = {}	
		for i in range(len(tmploc)):
			tmploc[i] = tmploc[i].strip()	
			tmpexc = re.split(':', tmploc[i])
			tmpexc[1] = tmpexc[1].strip()
			if tmpexc[1][0] == '"':	# empty loc codes will be assigned '--'
				tmpexc[1] = '--'
			netstatID = tmpexc[0]
			locationID = tmpexc[1]
			self.locationexc[netstatID] = locationID
		
		'''
		tmpmag = re.split(',', self.magnificationexc)	# split magnifcation excepts
		self.magnificationexc = {}
		for i in range(len(tmpmag)):	# split/store magnificationexc
			tmpexc = re.split(':', tmpmag[i])
			self.magnificationexc[tmpexc[0].strip()] = float(tmpexc[1].strip())
		'''

		# Comments associated with each var
		# Default variables	
		self.durationcmt = "# duration"
		self.ipaddresscmt = "# ipaddress of query server"
		self.httpportcmt = "# httpport of query server"
		self.magnification_defaultcmt = "# magnification default"
		self.resxcmt = "# xresolution"
		self.resycmt = "# yresolution"
		self.pixcmt = "# pixels per inch"
		self.imgformatcmt = "# image format (*.jpg, *.png, etc.)"
		self.thumbscalecmt = "# thumbscale for thumbnail sizing"	
		self.vertrangecmt = "# vertical scaling range"
		self.cwbwaitcmt = "# wait time for cwbquery timeout"
		self.cwbattemptscmt = "# number of cwbquery attempts before exiting"
		self.cwbretrysleepcmt = "# cwbquery sleep time for retry"

		# Directory paths
		self.seedpathcmt = "# temporary seed path"
		self.plotspathcmt = "# temporary plots path"
		self.thumbpathcmt = "# temporary thumbnails path"
		self.helihtmlpathcmt = "# temporary heli html path"
		self.cwbquerycmt = "# cwbquery jar file"
		self.resppathcmt = "# responses path"
	
		# Filter designs
		self.EHZfiltertypecmt = "# EHZ filter type"
		self.EHZhpfreqcmt = "# EHZ highpass frequency"
		self.EHZnotchfreqcmt = "# EHZ notch frequency"
		self.BHZfiltertypecmt = "# BHZ filter type"
		self.BHZbplowerfreqcmt = "# BHZ bplower freq"
		self.BHZbpupperfreqcmt = "# BHZ bpupper freq"
		self.LHZfiltertypecmt = "# LHZ filter type"
		self.LHZbplowerfreqcmt = "# LHZ bplower freq"
		self.LHZbpupperfreqcmt = "# LHZ bpupper freq"
		self.VHZfiltertypecmt = "# VHZ filter type"
		self.VHZlpfreqcmt = "# VHZ lowpass frequency"

		# Other comments (stations/magnifications/summary)
		self.stationcmt = "# Station Data"
		self.magnificationexccmt = "# magnification exceptions list"
		self.cfgcmt = "# ---------------------------------------------------\n# Config file is populated by readStations.py\n# station info will be read from station list\n# execution times will depend on cronjob or an\n# external time file that lists times for each station\n# ---------------------------------------------------\n# **NOTE: Each filter design has 4 prefilter corner freqs\n# ---------------------------------------------------\n"
