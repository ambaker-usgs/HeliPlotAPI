#!/usr/bin/env python

# -----------------------------------------------------------
# Author: Alejandro Gonzales 
# Filename: parallelcwbQuery.py
# -----------------------------------------------------------
# Purpose: Creates multiprocessing pool to run multiple 
#	   instances of CWBQuery.jar. CWBQuery pulls station
#	   seed files from specified server (Golden/ASL)
# -----------------------------------------------------------
import multiprocessing
from multiprocessing import Manager, Value
import os, sys, string, subprocess
import time

# Necessary vars from main __init__ in HeliPlot.py
'''
self.seedpath
self.stationinfo
'''

# Exception classes and cwbQuery() unpack function
class KeyboardInterruptError(Exception): pass	
class TimeoutExpiredError(Exception): pass	

class ParallelCwbQuery(object):
	def launchWorkers(self):
		# ---------------------------------------------
		# Initialize all vars needed to run cwbQuery()
		# ---------------------------------------------
		print "------cwbQuery() Pool------\n"
		self.home = os.getcwd()

