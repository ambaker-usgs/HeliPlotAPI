#!/usr/bin/env python

# This is a test script for HeliPlot module
from heliplot import kill, readPrestation, parseConfig, parallelcwbQuery

# Populate station.cfg using prestation.cfg and stationNames.txt
# Set user paths and station info
readcfg = readPrestation.ReadPrestation()
readcfg.readConfig()
readcfg.storeStations()
readcfg.writeDefaultVariables()

'''
# Parse station.cfg and set execution time
pars = parseConfig.ParseConfig()	# initialize parser object
pars.setStationData()
timeargs = {'year': 2014, 'month': 04, 'day': 21, 'hour': 17, 
		'minute': 30, 'second': 0, 'microsecond': 0}
#pars.setExecTime(**timeargs)
pars.setExecTime()

# Launch cwbQuery multiprocessing pool
query = parallelcwbQuery.ParallelCwbQuery()	# initialize parallel cwbQuery object
queryargs = {'stationinfo': pars.stationinfo, 'cwbquery': pars.cwbquery, 
		'cwbattempts': pars.cwbattempts, 'cwbsleep': pars.cwbsleep,
		'cwbtimeout': pars.cwbtimeout, 'datetimeQuery': pars.datetimeQuery,
		'duration': pars.duration, 'seedpath': pars.seedpath, 'ipaddress': pars.ipaddress}
query.launchWorkers(**queryargs)
'''
