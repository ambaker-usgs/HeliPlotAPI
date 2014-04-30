#!/usr/bin/env python

# This is a test script for HeliPlot module
from heliplot import kill, parseConfig

obj = parseConfig.ParseConfig()	# initialize parser object
print obj.duration
print obj.cwbattempts
print obj.seedpath
print obj.BHZfiltertype
print obj.LHZfiltertype

obj.setStationData()
for info in obj.stationinfo:
	print info
for loc in obj.stationlocation:
	print loc 
if obj.magnificationexc is not None:
	for key, val in obj.magnificationexc.iteritems():
		print "%s = %f" % (key, val)

kwargs = {'year': 2014, 'month': 04, 'day': 21, 'hour': 17, 
		'minute': 30, 'second': 0, 'microsecond': 0}
#obj.setExecTime(**kwargs)
obj.setExecTime()
print obj.datetimeQuery
