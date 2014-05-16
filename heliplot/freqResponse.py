#!/usr/bin/env python

# ---------------------------------------------------------------
# Author: Alejandro Gonzales
# Filename: freqResponse.py 
# ---------------------------------------------------------------
# Purpose: Pull/store frequency responses for queried stations 
# ---------------------------------------------------------------
# Methods:
#	   storeResps() - store responses for each station 
# ---------------------------------------------------------------
import os, sys, re

class FreqResponse(object):
	def storeResps(self, resppath, stream, filelist, streamlen, datetimeUTC):
		print "-------freqResponse() Start-------\n"	
		os.chdir(resppath)
		networkID = []
		stationID = []
		locationID = []
		channelID = []

		# Need stations listed in SeedFiles directory
		for i in range(streamlen):
			tmpstation = filelist[i]
			stationindex = tmpstation.index('_')
			networkID.append(str(tmpstation[0:2]))
			stationID.append(str(tmpstation[2:stationindex]))
			locationindex = len(tmpstation)-11
			channelindex = len(tmpstation)-14
			locationID.append(str(tmpstation[locationindex:locationindex+2]))
			channelID.append(str(tmpstation[channelindex:channelindex+3]))

		try:
			print "Get/set station responses..."	
			stationName = []	# station names for output plots
			self.resp = []		# station freq responses for deconvolution
			print "streamlen = %d\n" % streamlen
		
			# Loop through stations and get responses (if no resp, rm station)
			i = 0
			while i < range(len(stream)):
				if i == len(stream):
					break	# index = num of streams
				
				# Check for empty loc codes, replace "__" with ""
				if locationID[i] == "__":
					locationID[i] = ""
				resfilename = ("RESP."+networkID[i]+"."+stationID[i]+"."+
					locationID[i]+"."+channelID[i])	# response file

				if not os.path.isfile(resfilename):
					# if no response remove station from stream list
					statid = stream[i][0].getId()
					print "------------------------------------------"	
					print "No response: %s" % resfilename
					print "Removing stream[%d]: %s" % (i,statid)
					stream.pop(i)
					networkID.pop(i)
					stationID.pop(i)
					locationID.pop(i)
					channelID.pop(i)
					print "stream[%d] removed..." % i
					print "------------------------------------------\n"	
					i = i 
				else:
					tmpname = re.split('RESP.', resfilename)
					stationName.append(tmpname[1].strip())
					resp = {'filename': resfilename, 'date': datetimeUTC,
						'units': 'VEL'}	# freq response of data (vel)
					self.resp.append(resp)
					i = i + 1
		
			self.networkID = networkID
			self.stationID = stationID
			self.locationID = locationID
			self.channelID = channelID
			self.stationName = stationName	# store station names
			self.stream = stream	# store new stream	
			self.streamlen = len(self.stream)	# store new streamlen	
			print "new stationName len = %d" % len(self.stationName)	
			print "new stream len = %d\n" % self.streamlen 
			print "-------freqResponse() Complete-------\n\n"	
		except KeyboardInterrupt:
			print "KeyboardInterrupt freqResponse(): terminating freqResponse() method"
			sys.exit(0)
			print "Method freqResponse() is terminated!"
		except Exception as e:
			print "Exception freqResponse(): " + str(e)
			sys.exit(0)
			print "Method freqResponse() is terminated!"
