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
from obspy.core.utcdatetime import UTCDateTime
from datetime import datetime, timedelta
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
		
			# Need to check for streams that have a start time greater
			# than the query time, then trim based on the nearest hour
			streamstart = stream[0].stats.starttime.datetime
			streamstart = streamstart.strftime("%Y%m%d_%H:%M:00")
			streamstart = UTCDateTime(streamstart)	
			if (streamstart.datetime <= plotstart.datetime):
				# Trim stream to starttime of plot
				# Round up to the nearest sample, this will take care
				# of sample drift for non-Q330 signals
				stream.trim(starttime=plotstart, endtime=plotend, nearest_sample=True)	# selects sample nearest trim time 
				print "Plotting "+stationName+" [Trimmed times: start = " + str(stream[0].stats.starttime.datetime) + ", end = " + str(stream[0].stats.endtime.datetime)+"]"
			elif (streamstart.datetime > plotstart.datetime):
				# Trim stream to nearest hour when
				# the plot start time is less than 
				# the stream start time 
				tmp = re.split(' ', str(streamstart.datetime))	
				date = tmp[0]
				time = tmp[1]
				tmpdate = re.split('-', str(date))	
				tmptime = re.split(':', str(time))
				year = int(tmpdate[0])	# stream stats (date/time) 
				month = int(tmpdate[1])
				day = int(tmpdate[2])
				hour = int(tmptime[0]) 
				minute = 0	# 00 to account for shift
				second = int(tmptime[2])
				currtime = datetime(year, month, day, hour, minute, second, 0)
				if int(hour) != 23:	
					# increase trim time to next hour if h != 23 	
					trimtime = currtime + timedelta(hours=1)	
					trimtime = UTCDateTime(trimtime)	
				else:	
					# trim to next day if h = 23 	
					hour = 0	# set time to 00:00:00 
					minute = 0
					second = 0
					trimtime = datetime(year, month, day, hour, minute, second, 0) + timedelta(days=1)
					trimtime = UTCDateTime(trimtime)	
				stream.trim(starttime=trimtime, endtime=plotend, nearest_sample=True)	# selects sample nearest trim time	
				print "Plotting "+stationName+" [Trimmed times: start = " + str(stream[0].stats.starttime.datetime) + ", end = " + str(stream[0].stats.endtime.datetime)+"]"	
	
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

			# If missing data, fill in beginning hours	
			hours = [0 for i in range(24)]	# 24 hours
			if len(labels) < len(hours):
				tmptime = re.split(':', labels[0].get_text())
				starthour = int(tmptime[0])
				lastindex = len(hours) - len(labels)	
				i = len(hours) - len(labels) 
				while (i > 0):
					hours[lastindex-i] = str(starthour-i)+":00"
					i = i - 1	
				i = 0	
				for i in range(len(labels)):
					tmptime = re.split(':', labels[i].get_text())
					hours[i+lastindex] = str(tmptime[0])+":00"
			elif len(labels) == len(hours):
				for i in range(len(labels)):	# extract hours from labels
					tmptime = re.split(':', labels[i].get_text())
					hours[i] = str(tmptime[0])+":00"
			
			# Create tick position list
			position = [i+0.5 for i in range(24)]	
			position = position[::-1]		# reverse list
			plt.yticks(position, hours, fontsize=9)	# times in position
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
