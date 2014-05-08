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
import os, re

class FreqResponse(object):
	def storeResps(self, resppath, filelist, streamlen, datetimeUTC):
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
		self.networkID = networkID
		self.stationID = stationID
		self.locationID = locationID
		self.channelID = channelID

		try:
			# Loop through stations and get responses
			print "Get/set station responses...\n"	
			stationName = []	# station names for output plots
			self.resp = []		# station freq responses for deconvolution
			for i in range(streamlen):
				# Check for empty loc codes, replace "__" with ""
				if locationID[i] == "__":
					locationID[i] = ""
				resfilename = ("RESP."+networkID[i]+"."+stationID[i]+"."+
					locationID[i]+"."+channelID[i])	# response file
				#print "resfilename: " + str(resfilename)
				tmpname = re.split('RESP.', resfilename)
				stationName.append(tmpname[1].strip())
				self.stationName = stationName	# store station names

				resp = {'filename': resfilename, 'date': datetimeUTC,
					'units': 'VEL'}	# freq response of data (velocity)
				self.resp.append(resp)
				#print "datetimeUTC: " + str(datetimeUTC)
			print "-------freqResponse() Complete-------\n\n"	
		except KeyboardInterrupt:
			print "KeyboardInterrupt freqResponse(): terminating freqResponse() method"
			sys.exit(0)
			print "Method freqResponse() is terminated!"
		except Exception as e:
			print "Exception freqResponse(): " + str(e)
			sys.exit(0)
			print "Method freqResponse() is terminated!"
