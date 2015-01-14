#!/usr/bin/env python

# --------------------------------------------------------------
# Author: Alejandro Gonzales 
# Filename: parallelplotVelocity.py 
# --------------------------------------------------------------
# Purpose: Plots velocity data (filtered/magnified stream) 
# ---------------------------------------------------------------
# Methods:
#	   launchWorkers() - multiprocessing pool for plotting 
#	   plotVelocity() - plots filtered/magnified streams 
# ---------------------------------------------------------------
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt	# will use title, figure, savefig methods
import matplotlib.image as img

import multiprocessing
from multiprocessing import Manager, Value
import os, sys, string, subprocess
import time, signal, glob, re

from kill import Kill 
from interrupt import KeyboardInterruptError, TimeoutExpiredError

# Unpack self from parallel method args and call method plotVelocity()
def unwrap_self_plotVelocity(args, **kwargs):
	return ParallelPlotVelocity.plotVelocity(*args, **kwargs)

class ParallelPlotVelocity(object):
	def __init__(self):
		# Initializes kill object for pool
		self.killproc = Kill()

	def plotVelocity(self, stream, stationName, filters):
		# --------------------------------	
		# Plots filtered/magnified streams	
		# --------------------------------	
		try:
			print "Plotting velocity data for station: " + str(stationName)
			streamID = stream[0].getId()	
			magnification = self.magnification[streamID] # magnification for station[i]
			trspacing = self.vertrange/magnification * 1000.0	# trace spacing
			# Get filter coefficients for every station	
			if streamID in filters['streamID']:
				filtertype = filters['filtertype']
				freqX = filters['freqX']
				freqY = filters['freqY']
			
				# set bounds x-label
				if filtertype == "highpass":
					bounds = str(freqX)
				elif filtertype == "bandpass":
					bounds = str(freqX) + "-" + str(freqY)	
				elif filtertype == "bandstop":
					bounds = str(freqX) + "-" + str(freqY)	
				elif filtertype == "lowpass":
					bounds = str(freqX)

			# pass explicit figure instance to set correct title and attributes
			dpl = plt.figure()
			titlestartTime = self.datetimePlotstart.strftime("%Y/%m/%d %H:%M")
			titlestartTime = titlestartTime + " UTC"
			plotstart = self.datetimePlotstart	
			plotend = self.datetimePlotend	
			
			# Trim stream to starttime of plot
			# Round up to the nearest sample, this will take care
			# of sample drift for non-Q330 signals
			oldtime = stream[0].stats.starttime	
			stream.trim(starttime=plotstart, nearest_sample=False)
			newtime = stream[0].stats.starttime	
			print stream 
			stream.plot(startime=plotstart,
				endtime=plotend,
				type='dayplot', interval=60,
				vertical_scaling_range=self.vertrange,
				right_vertical_labels=False, number_of_ticks=7,
				one_tick_per_line=True, color=['k'], fig=dpl,
				show_y_UTC_label=True, size=(self.resx,self.resy),
				dpi=self.pix, title_size=-1)

			# set title, x/y labels and tick marks
			plt.title(streamID + "  " + "Start: " + 
				str(titlestartTime), fontsize=12)
			plt.xlabel('Time [m]\n(%s: %sHz  Trace Spacing: %.2e mm/s)' %
				(str(filtertype), str(bounds), trspacing), fontsize=10)
			plt.ylabel('Time [h]', fontsize=10)
			locs, labels = plt.yticks()	# pull current locs/labels
			hours = [0 for i in range(len(labels))]
			for i in range(len(labels)):	# extract hours from labels
				tmptime = re.split(':', labels[i].get_text())
				hours[i] = int(tmptime[0])
			posilist = [i+0.5 for i in range(24)]	# create tick position list
			posilist = posilist[::-1]		# reverse list
			timelist = [0 for i in range(24)]	# timelist for tick hours
			timelen = len(timelist)
			starthr = hours[0]	# start hour
			if starthr <= 23:
				startlen = 23 - starthr + 1	# hours are from 0-23
			else:
				startlen = 0	
			startlist = range(starthr, starthr+startlen)	# start of list 0-23
			startlen = len(startlist)
			timelist[0:startlen] = startlist	# end of start should be 23
			timelist[startlen:timelen] = range(0, timelen-startlen)	# 0 to end time
			for i in range(len(timelist)):
				timelist[i] = str(timelist[i]) + ":00"
			plt.yticks(posilist, timelist, fontsize=9)	# times in position
			#dpi=self.pix, size=(self.resx,self.resy))
			plt.savefig(stationName+"."+self.imgformat)
			plt.close(dpl)	
			print	
		except KeyboardInterrupt:
			print "KeyboardInterrupt plotVelocity(): terminate workers..."
			raise KeyboardInterruptError()
			return	# return to plotVelocity() pool
		except Exception as e:
			print "UnknownException plotVelocity(): " + str(e)
			return

	def launchWorkers(self, streams, plotspath, stationName,
			  magnification, vertrange, datetimePlotstart,
			  datetimePlotend, resx, resy, pix, imgformat,
			  filters):
		# ------------------------	
		# Pool of plotting workers	
		# ------------------------	
		print "------plotVelocity() Pool------\n"
		self.magnification = magnification	
		self.vertrange = vertrange	
		self.datetimePlotstart = datetimePlotstart
		self.datetimePlotend = datetimePlotend
		self.resx = resx
		self.resy = resy
		self.pix = pix
		self.imgformat = imgformat	

		streamlen = len(streams)	
		# clear output plots dir
		os.chdir(plotspath)
		imgfiles = glob.glob(plotspath+"*")
		for f in imgfiles:
			os.remove(f)	# remove tmp png files from OutputPlots dir

		# Initialize multiprocessing pools for plotting
		PROCESSES = multiprocessing.cpu_count()
		print "PROCESSES:	" + str(PROCESSES)
		print "streamlen:	" + str(streamlen) + "\n"	
		pool = multiprocessing.Pool(PROCESSES)
		try:
			self.poolpid = os.getpid()
			self.poolname = "plotVelocity()"
			#print "pool PID:	" + str(self.poolpid) + "\n"
			pool.map(unwrap_self_plotVelocity, zip([self]*streamlen,
				streams, stationName, filters))	# thread plots
			pool.close()
			pool.join()
			print "------plotVelocity() Pool Complete------\n\n"
		except KeyboardInterrupt:
			print "KeyboardInterrupt parallelplotVelocity(): terminating pool..."
			# find/kill all child processes
			killargs = {'pid': self.poolpid, 'name': self.poolname}
			self.killproc.killPool(**killargs)
		except Exception as e:
			print "Exception parallelplotVelocity(): terminating pool: " + str(e)
			killargs = {'pid': self.poolpid, 'name': self.poolname}
			self.killproc.killPool(**killargs)
		else:
			# cleanup (close pool of workers)
			pool.close()
			pool.join()
