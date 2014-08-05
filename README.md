HeliPlotAPI
===========

Splits HeliPlot program into separate class files to be used as an API package

###Directory Structure
    
    heliplot/  # directory containing HeliPlot class files (used in setup.py script)
    run_heli/  # directory containing user run scripts 

###Setup/Install

    Install HeliPlot package to python site-package
    
        python setup.py install

###Run Scripts
    
    Run scripts for producing heliplots and heliplot thumbnails
    
        ./HeliPlot.py      # produce heliplot images for stations in station.cfg
        ./run_heli_24hr.py # creates html files for each heliplot image produced by HeliPlot.py
        ./run_heli.pl      # perl script that runs HeliPlot.py & run_heli_24hr.py in a crontab 

###API Class Files

    init.py              # initializes the HeliPlot package (class files can be imported)
    kill.py              # kills subprocess and multiprocessing pools for cwbquery and filtering
    interrupt.py         # raises timeout and keyboard interrupts for try/catch blocks 
    readPrestation.py    # reads prestation.cfg and creates main station.cfg file
    parseConfig.py       # parses main station.cfg file and globalizes variables
    parallelcwbQuery.py  # launches pool of CWBQuery() workers to pull station data
    pullTraces.py        # pull trace stats from station data stream (removes traces with sr=0Hz)
    freqResponse.py          # pull frequency response for station
    paralleldeconvFilter.py  # launches pool of workers that deconvolves/filters data 
    magnifyData.py           # magnify filtered streams using magnification exception list
    parallelplotVelocity.py  # plot magnified/filtered data using multiprocessing
    createThumbnails.py      # create thumbnails from output plots
    convertTime.py           # convert python time module to min/sec for method timing
