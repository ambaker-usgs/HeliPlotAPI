HeliPlotAPI
===========

Splits HeliPlot program into separate class files to be used as an API package

###Directory Structure
    * heliplot/  - directory containing HeliPlot class files (used in setup.py script)
    * run_heli/  - directory containing user run scripts 

###Setup/Install

    Install HeliPlot package to python site-package:
        python setup.py install

Run Scripts
==========================

1. _/run_heli/_ - directory containing user run scripts
2. _HeliPlot.py_ - main python script, calls heliplot modules to produce station plots
3. _run_heli_24hr.py_ - creates html files for each heliplot image produced by _HeliPlot.py_ 
4. _run_heli.pl_ - perl script that runs _HeliPlot.py_/_run_heli_24hr.py_ in a crontab 

API Class Files
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
10. _magnifyData.py_ - magnify filtered streams using magnification exception list
11. _parallelplotVelocity.py_ - plot magnified/filtered data using multiprocessing
12. _createThumbnails.py_ - create thumbnails from output plots
13. _convertTime.py_ - convert python time module to min/sec for method timing
