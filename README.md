HeliPlotAPI
===========

Splits HeliPlot program into separate class files to be used as an API-similar package

Class Files
============

1. _init.py_ - initializes the HeliPlot package (class files can be imported)
2. _parallelcwbQuery.py_ - launches pool of CWBQuery() workers to pull station data
3. _pullTraces.py_ - pull trace stats from station data stream (removes traces with sr=0Hz)
4. _freqResponse.py_ - pull frequency response for station
5. _parallelfreqDeconvFilter.py_ - launches pool of workers that deconvolves/filters data
6. _magnifyData.py_ - magnify streams by specified magnification factor
7. _parallelPlotVelocity.py_ - launch pool of workers to plot filtered/magnified station data
8. _createThumbnails.py_ - create thumbnail images from full sized station plots

Build Files/Install
===================

1. _setup.py_ - packages HeliPlot class files using python build structure
2. _python_ _setup.py_ _sdist_ - hard links programs to distribution directory and creates tarball
3. _python_ _setup.py_ _install_ - install HeliPlot package to python site-packages
