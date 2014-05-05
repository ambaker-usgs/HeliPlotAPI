#!/usr/bin/env python

# ---------------------------------------------------------------
# Author: Alejandro Gonzales
# Filename: pullTraces.py
# ---------------------------------------------------------------
# Purpose: Open seed files from cwbQuery and pull traces stats
#	   from the data stream. If trace has sample rate = 0Hz
#	   remove that trace from the data stream
# ---------------------------------------------------------------
# Methods:
#	   analyzeRemove() - look for 0Hz traces and remove
# ---------------------------------------------------------------
import os, sys
from obspy.core.stream import read

class PullTraces(object):
	# Read MSEED files from query and analyze
	def analyzeRemove(self, seedpath):
		os.chdir(seedpath)
		filelist = sorted(os.listdir(seedpath), key=os.path.getctime)
		self.filelist = filelist
		filelen = len(filelist)
		stream = [0 for x in range(filelen)]	# multidim streams list, streams for each file contain multiple traces so streams = [][] where the second entry denotes the trace index
		i = filelen - 1
		while i >= 0:
			try:
				stream[i] = read(filelist[i])	# read MSEED files from query
			except Exception as e:
				print "Exception pullTraces() (read(MSEED)): " + str(e)
				sys.exit(0)
				print "Method analyzeRemove() is terminated!"
			i = i - 1

		# Loop through stream traces, if trace has sample rate 0.0Hz
		# => NFFT = 0, then this trace will be removed 
		try:
			streamlen = len(stream)	# number of streams (ie mseed files)
			self.streamlen = streamlen
			print "streamlen: " + str(self.streamlen)
			print "Removing traces with 0.0Hz sampling rate from stream...\n"
			trace = {}	# dict of traces for each stream
			for i in range(streamlen):
				strsel = stream[i]	# selected stream
				tracelen = strsel.count()
				tmp_trace_id = strsel[0].getId()
				index = str(i)
				if tracelen == 1:	# single trace stream
					#trace[index] = strsel[0]	# trace 0 in stream[i]
					tr = stream[i][0]	
					if tr.stats['sampling_rate'] == 0.0:
						stream[i].remove(tr)
				elif tracelen > 1:	# multiple trace stream
					#trace[index] = []	# list in dict
					for j in range(tracelen):
						#trace[index].append(strsel[j])	
							

		except KeyboardInterrupt:
			print "KeyboardInterrupt pullTraces(): terminating analyzeRemove() method"
			sys.exit(0)
			print "Method pullTraces() is terminated!"
		except Exception as e:
			#print "Exception pullTraces(): " + str(e)
			print e	
			sys.exit(0)
			print "Method pullTraces() is terminated!"
