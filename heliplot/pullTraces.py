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
	def analyzeRemove(self, seedpath):
		# ---------------------------------------	
		# Read MSEED files from query and analyze
		# ---------------------------------------	
		print "------pullTraces() Start------\n"	
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
	
		# Remove traces with sample rate = 0.0Hz => NFFT = 0 
		try:
			print "Removing traces with 0.0Hz sampling rate from stream..."
			streamlen = len(stream)	# number of streams (ie stream files)
			self.streamlen = streamlen	
			RM = False	
			print "streamlen = %s\n" % str(streamlen)	
			for i in range(streamlen):
				tracelen = stream[i].count()	# number of traces in stream
				id = stream[i][0].getId()	# trace ID	
				if tracelen == 1:
					tr = stream[i][0]	# tmp trace
					if tr.stats['sampling_rate'] == 0.0:
						stream[i].remove(tr)
				elif tracelen > 1:
					j = 0	# stream will change sizes when trace is removed
					while j < range(stream[i].count()):
						if j == stream[i].count():	
							break	# index = num traces 
						tr = stream[i][j]	# tmp trace
						if tr.stats['sampling_rate'] == 0.0:
							if not RM:	
								print "Removing empty traces:"	
								print stream[i]
								print	
								RM = True 
							stream[i].remove(tr)	# rm empty trace
							j = 0	# reset index for new size
						else:
							j = j + 1	# mv to next element	
					if RM:
						print "Final stream with removed traces:"
						print stream[i]
						print	
						RM = False
			self.stream = stream	# new stream with removed traces	
			print "-------pullTraces() Complete-------\n\n"	
		except KeyboardInterrupt:
			print "KeyboardInterrupt pullTraces(): terminating analyzeRemove() method"
			sys.exit(0)
			print "Method pullTraces() is terminated!"
		except Exception as e:
			print "Exception pullTraces(): " + str(e)
			sys.exit(0)
			print "Method pullTraces() is terminated!"
