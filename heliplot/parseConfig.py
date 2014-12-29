#!/usr/bin/env python

# ----------------------------------------------------------------
# Author: Alejandro Gonzales
# Filename: parseConfig.py 
# ----------------------------------------------------------------
# Purpose: Reads in station.cfg file and sets/globalizes 
#	   station variables. Program also gets/sets the
#	   execution time for station queries, user has the
#	   option of setting their own time: 
#	   {year, month, day, hour, minute, second, microsecond} 
# ----------------------------------------------------------------
# Methods/Functions: 
#	   is_empty() - check if list/dict is empty
#	   setStationData() - sets vars from station.cfg
#	   setExecTime() - sets execution time for station queries
# ----------------------------------------------------------------
import os, re
from datetime import datetime, timedelta
from obspy.core.utcdatetime import UTCDateTime
	
def is_empty(structure):
	# ----------------------------------	
	# Check if list/dictionary is empty
	# ----------------------------------	
	if structure:
		return False
	else:
		return True

class ParseConfig(object):
	def setStationData(self):
		# -----------------------------------	
		# Set station info/locations/metadata 
		# -----------------------------------	
		self.stationdata = self.data['station']
		self.stationinfo = []
		self.stationlocation = []
		for s in self.stationdata:
			tmpstation = re.split('\t', s)
			self.stationinfo.append(tmpstation[0].strip())
			self.stationlocation.append(tmpstation[1].strip())

		# Split/store network filter exceptions list 
		tmpnetfilt = re.split(',', self.net_filterexc)
		self.net_filterexc = {}
		for i in range(len(tmpnetfilt)):
			tmpnetfilt[i] = tmpnetfilt[i].strip();
			tmpexc = re.split(':', tmpnetfilt[i])
			self.net_filterexc[tmpexc[0].strip()] = str(tmpexc[1].strip())

		# Split/store network magnification exceptions list
		tmpnetmag = re.split(',', self.net_magnificationexc)
		self.net_magnificationexc = {}
		for i in range(len(tmpnetmag)):
			tmpnetmag[i] = tmpnetmag[i].strip();
			tmpexc = re.split(':', tmpnetmag[i])
			self.net_magnificationexc[tmpexc[0].strip()] = float(tmpexc[1].strip())
		
		# Split/store station magnification exceptions list 
		tmpstatmag = re.split(',', self.stat_magnificationexc)
		self.stat_magnificationexc = {}	
		for i in range(len(tmpstatmag)):
			tmpstatmag[i] = tmpstatmag[i].strip();	
			tmpexc = re.split(':', tmpstatmag[i])
			self.stat_magnificationexc[tmpexc[0].strip()] = float(tmpexc[1].strip())

	def setExecTime(self, **kwargs): 	
		# ----------------------------------------------------	
		# Get/set current date/time and subtract a day
		# this will always pull the current time on the system
		# ----------------------------------------------------	
		
		# kwargs = {year, month, day, hour, minute, second, microsecond} (user input)	
		empty = is_empty(kwargs)	
		if empty:	
			self.time = datetime.utcnow() - timedelta(days=1)	
		else:	
			yr = kwargs['year']
			mn = kwargs['month']
			dy = kwargs['day']
			hr = kwargs['hour']
			min = kwargs['minute']
			sec = kwargs['second']
			ms = kwargs['microsecond']
			self.time = datetime(yr, mn, dy, hr, min, sec, ms) - timedelta(days=1)	
		time2 = self.time + timedelta(hours=1)
		time2str = time2.strftime("%Y%m%d_%H:00:00")
		time3 = time2 + timedelta(days=1)
		time3str = time3.strftime("%Y%m%d_%H:00:00")
		self.datetimePlotstart = UTCDateTime(time2str)
		self.datetimePlotend = UTCDateTime(time3str)
		print "datetimePlotstart:	%s" % str(self.datetimePlotstart)
		print "datetimePlotend: 	%s" % str(self.datetimePlotend)
		timestring = str(self.time)
		timestring = re.split("\\.", timestring)
		tmp = timestring[0]
		timedate = tmp.replace("-", "/")
		datetimeQuery = timedate.strip()
		#datetimeQuery = "2013/09/12 13:30:00"
		self.datetimeQuery = datetimeQuery
		tmpquery = re.split(' ', self.datetimeQuery)
		tmpdate = tmp[0].strip()
		tmptime = tmp[1].strip()
		print "datetimeQuery: 		%s" % str(self.datetimeQuery)
		print "queryDuration:		%s" % str(self.duration)	
		tmpUTC = datetimeQuery
		tmpUTC = tmpUTC.replace("/", "")
		tmpUTC = tmpUTC.replace(" ", "_")
		self.datetimeUTC = UTCDateTime(str(tmpUTC))
		print "datetimeUTC:		%s" % str(self.datetimeUTC) + "\n"
			
	# Read in main station config file (station.cfg)
	def __init__(self, **kwargs):
		#os.chdir('/home/asluser/HeliPlotAPI')
		home = os.getcwd()
		os.chdir(home)	
		self.home = home 
		self.data = {}
		self.data['station'] = []	# list for multiple stations
		STFLAG = False
		fin = open('station.cfg', 'r')
		for line in fin:
			if line[0] == '#':
				if line != '\n':
					newline = re.split('#', line)
					if "Station Data" in newline[1]:
						STFLAG = True
			elif line[0] != '#':
				if line != '\n':
					newline = re.split('#', line)	
					if STFLAG:
						self.data['station'].append(line.strip())
					elif "duration" in newline[1]:
						self.duration = float(newline[0].strip())
					elif "ipaddress" in newline[1]:
						self.ipaddress = str(newline[0].strip())
					elif "httpport" in newline[1]:
						self.httpport = int(newline[0].strip())
					elif "magnification default" in newline[1]:
						self.magnification_default = float(newline[0].strip())
					elif "xres" in newline[1]:
						self.resx = int(newline[0].strip())
					elif "yres" in newline[1]:
						self.resy = int(newline[0].strip())
					elif "pixels" in newline[1]:
						self.pix = int(newline[0].strip())
					elif "image format" in newline[1]:
						self.imgformat = str(newline[0].strip())
					elif "thumbscale" in newline[1]:
						self.thumbscale = float(newline[0].strip())
					elif "vertical" in newline[1]:
						self.vertrange = float(newline[0].strip())
					elif "cwbquery timeout" in newline[1]:
						self.cwbtimeout = int(newline[0].strip())
					elif "cwbquery attempts" in newline[1]:
						self.cwbattempts = int(newline[0].strip())
					elif "cwbquery sleep" in newline[1]:
						self.cwbsleep = int(newline[0].strip())
					elif "seed" in newline[1]:
						self.seedpath = str(newline[0].strip())
					elif "plots" in newline[1]:
						self.plotspath = str(newline[0].strip())
					elif "thumbnails" in newline[1]:
						self.thumbpath = str(newline[0].strip())
					elif "cwbquery" in newline[1]:
						self.cwbquery = str(newline[0].strip())
					elif "responses" in newline[1]:
						self.resppath = str(newline[0].strip())
					elif "EHZ filter" in newline[1]:
						self.EHZfiltertype = str(newline[0].strip())
					elif "EHZ highpass" in newline[1]:
						self.EHZhpfreq = float(newline[0].strip())
					elif "BHZ filter" in newline[1]:
						self.BHZfiltertype = str(newline[0].strip())
					elif "BHZ bplower" in newline[1]:
						self.BHZbplowerfreq = float(newline[0].strip())
					elif "BHZ bpupper" in newline[1]:
						self.BHZbpupperfreq = float(newline[0].strip())
					elif "BHZ notchlower" in newline[1]:
						self.BHZnotchlowerfreq = float(newline[0].strip())
					elif "BHZ notchupper" in newline[1]:
						self.BHZnotchupperfreq = float(newline[0].strip())
					elif "LHZ filter" in newline[1]:
						self.LHZfiltertype = str(newline[0].strip())
					elif "LHZ bplower" in newline[1]:
						self.LHZbplowerfreq = float(newline[0].strip())
					elif "LHZ bpupper" in newline[1]:
						self.LHZbpupperfreq = float(newline[0].strip())
					elif "LHZ notchlower" in newline[1]:
						self.LHZnotchlowerfreq = float(newline[0].strip())
					elif "LHZ notchupper" in newline[1]:
						self.LHZnotchupperfreq = float(newline[0].strip())
					elif "VHZ filter" in newline[1]:
						self.VHZfiltertype = str(newline[0].strip())
					elif "VHZ lowpass" in newline[1]:
						self.VHZlpfreq = float(newline[0].strip())	
					elif "network filter exceptions" in newline[1]:
						self.net_filterexc = newline[0].strip()
					elif "network magnification exceptions" in newline[1]:
						self.net_magnificationexc = newline[0].strip()
					elif "station magnification exceptions" in newline[1]:
						self.stat_magnificationexc = newline[0].strip()
		fin.close()	# close station.cfg
