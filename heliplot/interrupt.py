#!/usr/bin/env python

# --------------------------------------------------------------
# Author: Alejandro Gonzales 
# Filename: interrupt.py 
# --------------------------------------------------------------
# Purpose: Interrupt error classes for parallel routines 
# ---------------------------------------------------------------
# Classes:
#	   KeyboardInterruptError() 
#	   TimeoutExpiredError() 
# ---------------------------------------------------------------

class KeyboardInterruptError(Exception): pass
class TimeoutExpiredError(Exception): pass
