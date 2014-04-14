HeliPlotAPI
===========

Splits HeliPlot program into separate class files to be used as an API-similar package

Class Files
============

1. __init__.py
 * Initializes the HeliPlot package (class files can be imported)
2. parallelcwbQuery.py
 * Launches pool of CWBQuery() workers to pull station data
3. pullTraces.py
 * Pull trace stats from station data stream (removes traces with sr=0Hz)
4. freqResponse.py
 * Pull frequency response for station
5. parallelfreqDeconvFilter.py
 * Launches pool of workers that deconvolves/filters data
6. magnifyData.py
 * Magnify streams by specified magnification factor
7. parallelPlotVelocity.py
 * Launch pool of workers to plot filtered/magnified station data
8. createThumbnails.py
 * Create thumbnail images from full sized station plots
