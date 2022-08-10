from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Pulls geospatial data from GeoBoundaries'

setup(
        name="geospatialfile", 
        version=VERSION,
        author="Todd Marino",
        author_email="<marino.todd@gmail.com>",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=['pycountry', 'apache-sedona', 'pyspark', 'geopandas' ],
        keywords=['python', 'geospatial']
    
)