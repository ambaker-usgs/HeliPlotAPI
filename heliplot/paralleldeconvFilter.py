#!/usr/bin/env python

# --------------------------------------------------------------
# Author: Alejandro Gonzales 
# Filename: paralleldeconvFilter.py
# --------------------------------------------------------------
# Purpose: Simulates/filters station data stream. Simulating
#	   produces a deconvolved signal. Pre-filter bandpass
#	   corner frequencies eliminate end frequency spikes
#	   (ie H(t) = F(t)/G(t), G(t) != 0)
#
#	   *NOTE: Currently LHZ/BHZ/VHZ/EHZ have different 
#	   filter designs, higher freq channels will need to
#	   use a notch or high freq filter later on
# ---------------------------------------------------------------
# Methods:
#	   launchWorkers() - multiprocessing pool for filters
#	   deconvFilter() - deconvolve/filter station data 
# ---------------------------------------------------------------
import multiprocessing
import os, sys, string, subprocess
import time, signal, glob, re
import numpy as np

from multiprocessing import Manager, Value
from kill import Kill 
from interrupt import KeyboardInterruptError, TimeoutExpiredError

# Unpack self from parallel method args and call deconvFilter()
def unwrap_self_deconvFilter(args, **kwargs):
	return ParallelDeconvFilter.deconvFilter(*args, **kwargs)

class ParallelDeconvFilter(object):
	def __init__(self):
		# Initialize kill object for class
		self.killproc = Kill()

	def deconvFilter(self, stream, response):
		# ----------------------------------------
		# Deconvolve/filter each station, filters
		# are based on channel IDs	
		# ----------------------------------------
		tmpstr = re.split("\\.", stream[0].getId())
		namestr = tmpstr[1].strip()
		nameloc = tmpstr[2].strip()
		namechan = tmpstr[3].strip()
		nameres = response['filename'].strip()
		if namechan == "EHZ":
			filtertype = self.EHZfiltertype
			hpfreq = self.EHZhpfreq
			notchfreq = self.EHZnotchfreq	# notch fltr will be implemented later
		elif namechan == "BHZ":
			filtertype = self.BHZfiltertype
			bplowerfreq = self.BHZbplowerfreq
			bpupperfreq = self.BHZbpupperfreq
		elif namechan == "LHZ":
			filtertype = self.LHZfiltertype
			bplowerfreq = self.LHZbplowerfreq
			bpupperfreq = self.LHZbpupperfreq
		elif namechan == "VHZ":
			filtertype = self.VHZfiltertype
			lpfreq = self.VHZlpfreq

		# Try/catch block for sensitivity subprocess
		try:
			print "Filter stream " + namestr + " and response " + nameres
			print namechan + " filtertype = " + str(filtertype)

			# Deconvolution (removes sensitivity)
			sensitivity = "Sensitivity:"	# pull sensitivity from RESP file
			grepSensitivity = ("grep " + '"' + sensitivity + '"' + " " +
				nameres + " | tail -1")
			self.subprocess = True	# flag for exceptions (if !subprocess return)
			subproc = subprocess.Popen([grepSensitivity], stdout=subprocess.PIPE,
				stderr=subprocess.PIPE, shell=True)
			(out, err) = subproc.communicate(timeout=10)	# waits for child proc

			# Store/print pids for exception kills
			self.parentpid = os.getppid()
			self.childpid = os.getpid()
			self.gchildpid = subproc.pid
			#print "parent pid: " + str(self.parentpid)
			#print "child  pid: " + str(self.childpid)
			#print "gchild pid: " + str(self.gchildpid)

			# Pull sensitivity from subproc
			tmps = out.strip()
			tmps = re.split(':', tmps)
			s = float(tmps[1].strip())
			#print "sensitivity: " + str(s)
			sys.stdout.flush()
			sys.stderr.flush()
			self.subprocess = False	# subprocess finished

			# deconvolution (this will be a flag for the user)
			# stream.simulate(paz_remove=None, pre_filt=(c1, c2, c3, c4), 
			# 	seedresp=response, taper='True') 

			# Remove transient response and decimate signals to SR=1Hz 
			decfactor = int(stream[0].stats.sampling_rate)
			stream.detrend('demean')	# removes mean in data set
			#stream.taper(max_percentage=0.01/2.0, type='cosine')	# cos tapers beginning/end to remove transient resp
			stream.decimate(decfactor, no_filter=True, strict_length=False)	

			# Filter stream based on channel (remove sensitivity) 
			if filtertype == "bandpass":
				print "Bandpass filter: %.3f-%.3fHz" % (bplowerfreq, bpupperfreq)
				maxval = np.amax(stream[0].data) 
				stream.filter(filtertype, freqmin=bplowerfreq,
					freqmax=bpupperfreq, corners=4)	# bp filter 
				stream[0].data = stream[0].data / s
			elif filtertype == "lowpass":
				print "Lowpass filter: %.2f" % lpfreq
				stream.filter(filtertype, freq=lpfreq, corners=4) # lp filter 
				stream[0].data = stream[0].data / s
			elif filtertype == "highpass":
				print "Highpass filter: %.2f" % hpfreq
				stream.filter(filtertype, freq=hpfreq, corners=4) # hp filter
				stream[0].data = stream[0].data / s
			print "Filtered stream: " + str(stream) + "\n"
			return stream
		except subprocess.TimeoutExpired:
			print "TimeoutExpired deconvFilter(): terminate workers..."
			if self.subprocess:
				signum = signal.SIGKILL
				killargs = {'childpid': self.childpid,
					    'gchildpid': self.gchildpid,
					    'signum': signum}
				self.killproc.killSubprocess(**killargs)
			sys.stdout.flush()
			sys.stdout.flush()
			raise TimeoutExpiredError()
			return	# return to deconvFilter pool
		except KeyboardInterrupt:
			print "KeyboardInterrupt deconvFilter(): terminate workers..."
			if self.subprocess:
				signum = signal.SIGKILL
				killargs = {'childpid': self.childpid,
					    'gchildpid': self.gchildpid,
					    'signum': signum}
				self.killproc.killSubprocess(**killargs)
			raise KeyboardInterruptError()
			return
		except Exception as e:
			print "UnknownException deconvFilter(): " + str(e)
			if self.subprocess:
				signum = signal.SIGKILL
				killargs = {'childpid': self.childpid,
					    'gchildpid': self.gchildpid,
					    'signum': signum}
				self.killproc.killSubprocess(**killargs)
			return

	def launchWorkers(self, stream, streamlen, response,
			  EHZfiltertype, EHZhpfreq, EHZnotchfreq,
			  BHZfiltertype, BHZbplowerfreq, BHZbpupperfreq,
			  LHZfiltertype, LHZbplowerfreq, LHZbpupperfreq,
			  VHZfiltertype, VHZlpfreq):
		# ---------------------------------
		# Simulate/filter queried stations
		# ---------------------------------
		print "-------deconvFilter() Pool-------\n"
		# initialize vars
		self.EHZfiltertype = EHZfiltertype
		self.EHZhpfreq = EHZhpfreq
		self.EHZnotchfreq = EHZnotchfreq
		self.BHZfiltertype = BHZfiltertype
		self.BHZbplowerfreq = BHZbplowerfreq
		self.BHZbpupperfreq = BHZbpupperfreq
		self.LHZfiltertype = LHZfiltertype
		self.LHZbplowerfreq = LHZbplowerfreq
		self.LHZbpupperfreq = LHZbpupperfreq
		self.VHZfiltertype = VHZfiltertype
		self.VHZlpfreq = VHZlpfreq

		# Merge traces to eliminate small data lengths, 
		# method 0 => no overlap of traces (i.e. overwriting
		# of previous trace data, gaps fill overlaps)
		# method 1 => fill overlaps using interpolation for
		# values between both vectors for x num of samples
		for i in range(streamlen):
			stream[i].merge(method=1, fill_value='interpolate',
				interpolation_samples=100)

		# Deconvolution/Prefilter
		# Initialize multiprocessing pools
		PROCESSES = multiprocessing.cpu_count()
		print "PROCESSES:	" + str(PROCESSES)
		print "streamlen:	" + str(streamlen) + "\n"	
		pool = multiprocessing.Pool(PROCESSES)
		try:
			self.poolpid = os.getpid()
			self.poolname = "deconvFilter()"
			flt_streams = pool.map(unwrap_self_deconvFilter,
				zip([self]*streamlen, stream, response))
			pool.close()
			pool.join()
			self.flt_streams = flt_streams
			print "-------deconvFilter() Pool Complete-------\n\n"
		except TimeoutExpiredError:
			print "\nTimeoutExpiredError parallelDeconvFilter(): terminating pool..."
			# find/kill all child processes
			killargs = {'pid': self.poolpid, 'name': self.poolname}
			self.killproc.killPool(**killargs)
		except KeyboardInterrupt:
			print "\nKeyboardInterrupt parallelDeconvFilter(): terminating pool..."
			killargs = {'pid': self.poolpid, 'name': self.poolname}
			self.killproc.killPool(**killargs)
		else:
			# cleanup (close pool of workers)
			pool.close()
			pool.join()
