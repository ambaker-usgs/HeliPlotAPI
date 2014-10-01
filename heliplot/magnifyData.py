#!/usr/bin/env python

# --------------------------------------------------------------
# Author: Alejandro Gonzales 
# Filename: magnifyData.py 
# --------------------------------------------------------------
# Purpose: Magnify streams by specified magnification factor 
# ---------------------------------------------------------------
# Methods:
#	   magnify() - magnifies data   
# ---------------------------------------------------------------
import os, sys, re

class MagnifyData(object):
	def magnify(self, flt_streams, magnificationexc, magnification_default):
		# ---------------------------	
		# Magnifies filtered streams 	
		# ---------------------------	
		print "------magnifyData() Start------\n"
		streams = flt_streams
		streamlen = len(streams)
		print "Num filtered streams: " + str(streamlen)
		self.magnification = {}	# dict containing magnifications for each station
		try:
			for i in range(streamlen):
				tr = streams[i][0]	# single trace within stream
				data = tr.data		# data samples from single trace
				datalen = len(data)
				tmpID = re.split("\\.", tr.getId())	# stream ID
				networkID = tmpID[0].strip()		# network ID
				stationID = tmpID[1].strip()		# station ID
				netstationID = networkID + stationID	# network/station

				print "Magnifying stream: " + str(tr.getId())
				if netstationID in magnificationexc:
					magnification = magnificationexc[netstationID]
				else:
					magnification = magnification_default
				print "magnification = " + str(magnification) + "\n"
				self.magnification[tr.getId()] = magnification
				streams[i][0].data = streams[i][0].data * magnification
			
			print "------magnifyData() Complete------\n\n"
			return streams
		except KeyboardInterrupt:
			print "KeyboardInterrupt magnifyData(): terminating magnify() method"
			sys.exit(0)
			print "Method magnify() is terminated!"
		except Exception as e:
			print "Exception magnifyData(): " + str(e)
			sys.exit(0)
			print "Method magnifyData() is terminated!"
