import pytest
from geospatialfile import Country, GeoBoundary, Response, GeoFile

def test_country_2():
    two = "EG"
    assert Country(two) == "EGY"
      
def test_country_3():
    three = "EGY"
    assert Country(three) == "EGY"
    
def test_country():
    country = "egypt"
    assert Country(country) == "EGY"
