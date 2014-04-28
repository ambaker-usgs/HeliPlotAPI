#!/usr/bin/env python

# New Package (test initialization for HeliPlot)
import os, re
from datetime import datetime, timedelta

# Read in main station config file (station.cfg)
os.chdir('/home/asluser/HeliPlot/')
fin = open('station.cfg', 'r')
data = {}
data['station'] = []	# list for multiple stations
STFLAG = False
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
				data['station'].append(line.strip())
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
			elif "EHZ notch" in newline[1]:
				self.EHZnotchfreq = float(newline[0].strip())
			elif "BHZ filter" in newline[1]:
				self.BHZfiltertype = str(newline[0].strip())
			elif "BHZ bplower" in newline[1]:
				self.BHZbplowerfreq = float(newline[0].strip())
			elif "BHZ bpupper" in newline[1]:
				self.BHZbpupperfreq = float(newline[0].strip())
			elif "LHZ filter" in newline[1]:
				self.LHZfiltertype = str(newline[0].strip())
			elif "LHZ bplower" in newline[1]:
				self.LHZbplowerfreq = float(newline[0].strip())
			elif "LHZ bpupper" in newline[1]:
				self.LHZbpupperfreq = float(newline[0].strip())
			elif "VHZ filter" in newline[1]:
				self.VHZfiltertype = str(newline[0].strip())
			elif "VHZ lowpass" in newline[1]:
				self.VHZlpfreq = float(newline[0].strip())	
			elif "magnification exceptions" in newline[1]:
				self.magnificationexc = newline[0].strip()

# Store station info/locations in variables
self.stationdata = data['station']
self.stationinfo = []
self.stationlocation = []
for s in self.stationdata:
	tmpstation = re.split('\t', s)
	self.stationinfo.append(tmpstation[0].strip())
	self.stationlocation.append(tmpstation[1].strip())

# Split/store magnification exception list
tmpmag = re.split(',', self.magnificationexc)
self.magnificationexc = {}
for i in range(len(tmpmag)):
	tmpexc = re.aplit(':', tmpmag[i])
	self.magnificationexc[tmpexc[0].strip()] = float(tmpexc[1].strip())

# Get current date/time and subtract a day
# this will always pull the current time on the system
#time = datetime.utcnow() - timedelta(days=1)	
# (year, month, day, hour, minute, second, microsecond)
time = datetime(2014, 4, 10, 15, 07, 0, 0) - timedelta(days=1)	# earthquake
time2 = time + timedelta(hours=1)
time2str = time2.strftime("%Y%m%d_%H:00:00")
time3 = time2 + timedelta(days=1)
time3str = time3.strftime("%Y%m%d_%H:00:00")
self.datetimePlotstart = UTCDateTime(time2str)
self.datetimePlotend = UTCDateTime(time3str)
print "datetimePlotstart:	%s" % str(self.datetimePlotstart)
print "datetimePlotend: %s" % str(self.datetimePlotend)
timestring = str(time)
timestring = re.split("\\.", timestring)
tmp = timestring[0]
timedate = tmp.replace("-", "/")
datetimeQuery = timedate.strip()
