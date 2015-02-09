#!/usr/bin/env python

# This is a test script for HeliPlot module
from heliplot import kill, readPrestation, parseConfig,\
			parallelcwbQuery, pullTraces, freqResponse,\
			paralleldeconvFilter, magnifyData,\
			parallelplotVelocity, createThumbnails,\
			convertTime
import time

if __name__ == '__main__':
	# Main program for running each HeliPlot module and tracking times
	# **NOTE: readPrestation methods do not need to be run if stationNames
	# 	  text file remains the same

	# -------------------------
	# Set Variables	
	# -------------------------
	totalTime = 0
	keys = []	# keys for methodTime dict
	methodTime = {}	# stores all method times in a dictionary of method names 
	timelenprestation = 0
	timelenparse = 0
	timelencwb = 0
	timelentrace = 0
	timelenresp = 0
	timelendeconv = 0
	timelenmagnify = 0
	timelenplot = 0
	timelenthumb = 0

	# ---------------------------------------------------------------	
	# Populate station.cfg using prestation.cfg and stationNames.txt
	# Set user paths and station info
	# ---------------------------------------------------------------	
	readcfg = readPrestation.ReadPrestation()
	t1 = time.time()	
	readcfg.readConfig()
	readcfg.storeStations()
	readcfg.writeDefaultVariables()
	readcfg.writePaths()
	readcfg.writeFilterVariables()
	readcfg.writeStations()
	t2 = time.time()	
	timelenprestation = t2 - t1
	
	# -------------------------------------------	
	# Parse station.cfg and set execution time
	# User can set execute specific times using:
	# timeargs = {'year':, 'month':, ...}
	# pars.setExecTime{**timeargs}
	# -------------------------------------------	
	pars = parseConfig.ParseConfig()	# initialize parser object
	t1 = time.time()	
	pars.setStationData()
	'''	
	timeargs = {'year': 2015, 'month': 2, 'day': 5, 'hour': 16,
			'minute': 37, 'second': 0, 'microsecond': 0}
	timeargs = {'year': 2015, 'month': 2, 'day': 6, 'hour': 22,
			'minute': 02, 'second': 0, 'microsecond': 0}
	timeargs = {'year': 2015, 'month': 2, 'day': 3, 'hour': 14,
			'minute': 30, 'second': 57, 'microsecond': 0}
	timeargs = {'year': 2015, 'month': 2, 'day': 5, 'hour': 12,
			'minute': 30, 'second': 0, 'microsecond': 0}
	'''	
	#pars.setExecTime(**timeargs)
	pars.setExecTime()
	t2 = time.time()	
	timelenparse = t2 - t1
	keys.append('parse')	
	methodTime['parse'] = timelenparse

	# --------------------------------------	
	# Launch cwbQuery multiprocessing pool
	# --------------------------------------	
	query = parallelcwbQuery.ParallelCwbQuery()	# initialize parallel cwbQuery object
	t1 = time.time()	
	queryargs = {'stationinfo': pars.stationinfo, 'cwbquery': pars.cwbquery, 
			'cwbattempts': pars.cwbattempts, 'cwbsleep': pars.cwbsleep,
			'cwbtimeout': pars.cwbtimeout, 'datetimeQuery': pars.datetimeQuery,
			'duration': pars.duration, 'seedpath': pars.seedpath, 'ipaddress': pars.ipaddress}
	query.launchWorkers(**queryargs)
	t2 = time.time()
	timelencwb = t2 - t1
	keys.append('cwb')	
	methodTime['cwb'] = timelencwb

	# --------------------------------------	
	# Pull traces from cwbQuery and analyze
	# --------------------------------------	
	strm = pullTraces.PullTraces()
	t1 = time.time()	
	seedpath = pars.seedpath
	strm.analyzeRemove(seedpath)
	t2 = time.time()
	timelentrace = t2 - t1
	keys.append('trace')	
	methodTime['trace'] = timelentrace
	
	# ----------------------------------------------------	
	# Pull freq responses from queried stations and store
	# also store station filter types	
	# ----------------------------------------------------	
	resp = freqResponse.FreqResponse()
	t1 = time.time()	
	respargs = {'resppath': pars.resppath, 'stream': strm.stream, 
			'filelist': strm.filelist, 'streamlen': strm.streamlen, 
			'datetimeUTC': pars.datetimeUTC,
			'EHZfiltertype': pars.EHZfiltertype,
			'EHZhpfreq': pars.EHZhpfreq,
			'BHZfiltertype': pars.BHZfiltertype,
			'BHZbplowerfreq': pars.BHZbplowerfreq,
			'BHZbpupperfreq': pars.BHZbpupperfreq,
			'BHZnotchlowerfreq': pars.BHZnotchlowerfreq,
			'BHZnotchupperfreq': pars.BHZnotchupperfreq,
			'LHZfiltertype': pars.LHZfiltertype,
			'LHZbplowerfreq': pars.LHZbplowerfreq,
			'LHZbpupperfreq': pars.LHZbpupperfreq,
			'LHZnotchlowerfreq': pars.LHZnotchlowerfreq,
			'LHZnotchupperfreq': pars.LHZnotchupperfreq,
			'VHZfiltertype': pars.VHZfiltertype,
			'VHZlpfreq': pars.VHZlpfreq,
			'net_filterexc': pars.net_filterexc}
	resp.storeResps(**respargs)
	t2 = time.time()
	timelenresp = t2 - t1
	keys.append('resp')	
	methodTime['resp'] = timelenresp

	# -----------------------------------
	# Deconvolve/filter queried stations
	# -----------------------------------
	fltr = paralleldeconvFilter.ParallelDeconvFilter()
	t1 = time.time()	
	fltrargs = {'stream': resp.stream, 'streamlen': resp.streamlen,
			'response': resp.resp, 'filters': resp.filtertype}
	fltr.launchWorkers(**fltrargs)
	t2 = time.time()
	timelendeconv = t2 - t1
	keys.append('deconv')	
	methodTime['deconv'] = timelendeconv

	# -------------------	
	# Magnify trace data
	# -------------------	
	mag = magnifyData.MagnifyData()
	t1 = time.time()	
	magargs = {'flt_streams': fltr.flt_streams,
		'net_magnificationexc': pars.net_magnificationexc,
		'stat_magnificationexc': pars.stat_magnificationexc,
		'magnification_default': pars.magnification_default}
	magnified_streams = mag.magnify(**magargs)
	t2 = time.time()
	timelenmagnify = t2 - t1
	keys.append('magnify')	
	methodTime['magnify'] = timelenmagnify

	# --------------------------------	
	# Plot filtered/magnified streams
	# --------------------------------	
	plt = parallelplotVelocity.ParallelPlotVelocity()
	t1 = time.time()	
	pltargs = {'streams': magnified_streams, 'plotspath': pars.plotspath,
			'stationName': resp.stationName,
			'magnification': mag.magnification,
			'vertrange': pars.vertrange,
			'datetimePlotstart': pars.datetimePlotstart,
			'datetimePlotend': pars.datetimePlotend,
			'resx': pars.resx, 'resy': pars.resy, 'pix': pars.pix,
			'imgformat': pars.imgformat,
			'filters': resp.filtertype}
	plt.launchWorkers(**pltargs)
	t2 = time.time()
	timelenplot = t2 - t1
	keys.append('plot')	
	methodTime['plot'] = timelenplot

	# ----------------------------------	
	# Create thumbnails from heli plots 
	# ----------------------------------	
	thm = createThumbnails.CreateThumbnails()
	t1 = time.time()
	thmargs = {'thumbpath': pars.thumbpath, 'plotspath': pars.plotspath,
			'thumbscale': pars.thumbscale}	
	thm.convertImage(**thmargs)
	t2 = time.time()
	timelenthumb = t2 - t1
	keys.append('thumb')	
	methodTime['thumb'] = timelenthumb

	# -------------------------------------------------------------------
	# Get total time of all modules/methods (don't use linux 'time' cmd)
	# -------------------------------------------------------------------
	timeobj = convertTime.ConvertTime()	
	totalTime = (timelenparse + timelencwb + timelentrace +
			timelenresp + timelendeconv + timelenmagnify +
			timelenplot + timelenthumb)
	keys.append('total')	
	methodTime['total'] = totalTime

	# Print times from methodTime dictionary (keys are in order of methods)
	for key in keys:
		if methodTime.has_key(key):
			ntime,ext = timeobj.setTime(methodTime[key])
			if key == 'magnify':
				print "timelen %s:	%.4f%s" % (key, ntime, ext)
			else:	
				print "timelen %s:		%.4f%s" % (key, ntime, ext)
