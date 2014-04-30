# Setup file describing all metadata about package
# Required fields: name, version, and packages
from distutils.core import setup

setup(
    name='heliplot',
    version='1.0dev',
    description='Heli plot generation of stations in the GSN/ANSS networks',
    author='Alejandro Gonzales',
    author_email='agonzales@usgs.gov',
    url='https://github.com/agonzales-usgs/HeliPlotAPI',
    license='Licensed by USGS Albuquerque Seismological Laboratory (ASL)',
    packages=['heliplot',],
)
