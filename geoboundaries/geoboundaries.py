import requests
import pycountry
import geopandas as gpd
from datetime import date
from sedona.register import SedonaRegistrator 
from sedona.sql.types import GeometryType
from pyspark.sql.types import StructType, StructField, StringType
from requests.exceptions import HTTPError

class Country:
    
    def __init__(self, string) -> None:
        self.string = string
    
    def __decipher_string(self) -> str:
        ''' takes the given string and figures out if it's 2 character
        3 character ISO, and if not 2 or 3 characters, then looks up Name'''
        codes = {2: "alpha_2", 3:"alpha_3"}
        string_length = len(self.string)
        key = codes[string_length] if string_length == 2 or string_length == 3 else "name"
        return key

    def __set(self):
        key = self.__decipher_string()
        setattr(self, key, self.string)
        delattr(self, 'string')

    @property
    def fetch(self) -> str:
        '''looks up the country info based on on the set up''' 
        self.__set()
        try: 
            if "name" in self.__dict__:
                return pycountry.countries.search_fuzzy(self.__dict__['name'])[0]
            else:
                return pycountry.countries.get(**self.__dict__)
        except ValueError as e:
            print("No results found in 2 or 3 character ISO code or name for the given input.")

class Response:
    def set_params(self, kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        return self

    def format_request(self, archive):
        self.adm = "ADM1" if 'adm' not in self.__dict__ else self.adm
        
        if archive:
            return f"https://www.geoboundaries.org/gbRequest.html?ISO={self.alpha_3}&ADM={self.adm}"
        else:
            return f"https://www.geoboundaries.org/api/current/gbOpen/{self.alpha_3}/{self.adm}"

    def get(self, archive=True):
        request = self.format_request(archive)
        try:
            r = requests.get(request)
            r.raise_for_status()
        except HTTPError as http_err:
            logger.  error(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            logger.error(f'Other error occurred: {err}')  
        else:
            results = r.json()
            
        if archive:
            return results[0]
        return results
        
class GeoFile:
    
    def __init__(self, string, adm="ADM1"):
        self.adm = adm
        self.alpha_3 = Country(string).get().alpha_3
        self.response = Response().set_params({"alpha_3": self.alpha_3}).get()

        
class GeoBoundary(GeoFile):
  
    def set_params(self, kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        return self

    def get(self, request):
        try:
            r = requests.get(request)
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            print(f'Other error occurred: {err}')  
        else:
            return r  

    def to_json(self):
        return self.get(self.response['gjDownloadURL']).json()

    def to_geopandas(self):
        boundaries = self.to_json()
        gdf = gpd.GeoDataFrame.from_features(boundaries)
        return gdf
    
    def to_pyspark(self, spark):
        
        SedonaRegistrator.registerAll(spark)
        
        schema = StructType([
            StructField('geometry', GeometryType())
            , StructField('shapeName', StringType())
            , StructField('shapeISO', StringType())
            , StructField('shapeID', StringType())
            , StructField('shapeGroup', StringType() )
            , StructField('shapeType', StringType())
        ])
        
        gdf = self.to_geopandas()
        sparkGDF = spark.createDataFrame(gdf, schema = schema)
        return sparkGDF
