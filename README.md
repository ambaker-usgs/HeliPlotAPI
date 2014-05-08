HeliPlotAPI
===========

Splits HeliPlot program into separate class files to be used as an API-similar package

Class Files
============

1. _init.py_ - initializes the HeliPlot package (class files can be imported)
2. _kill.py_ - kills subprocess and multiprocessing pools for cwbquery and filtering
3. _interrupt.py_ - raises timeout and keyboard interrupts for try/catch blocks 
4. _readPrestation.py_ - reads prestation.cfg and creates main station.cfg file
5. _parseConfig.py_ - parses main station.cfg file and globalizes variables
6. _parallelcwbQuery.py_ - launches pool of CWBQuery() workers to pull station data
7. _pullTraces.py_ - pull trace stats from station data stream (removes traces with sr=0Hz)
8. _freqResponse.py_ - pull frequency response for station
9. _paralleldeconvFilter.py_ - launches pool of workers that deconvolves/filters data 

Build Files/Install
===================

1. _setup.py_ - packages HeliPlot class files using python build structure
2. _python_ _setup.py_ _sdist_ - hard links programs to distribution directory and creates tarball
3. _python_ _setup.py_ _install_ - installs HeliPlot package to python site-packages
4. _testHeliPlot.py_ - test program for HeliPlot classes (./_testHeliPlot.py_ to run)
