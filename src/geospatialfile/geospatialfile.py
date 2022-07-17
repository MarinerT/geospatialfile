import requests
import pycountry
import geopandas as gpd
from datetime import date
from sedona.register import SedonaRegistrator 
from sedona.sql.types import GeometryType
from pyspark.sql.types import StructType, StructField, StringType
from requests.exceptions import HTTPError
import .module_spark as ms


spark = ms.spark

class Country:
    
    def __init__(self, string):
        self.string = string
    
    def get(self):
        codes = {2: "alpha_2", 3:"alpha_3"}
        key = codes[len(self.string)] if len(self.string) == 2 or len(self.string) == 3 else "name"
        setattr(self, key, self.string)
        delattr(self, 'string')
        
        try: 
            if key == "name":
                return pycountry.countries.search_fuzzy(self.__dict__['name'])[0]
            else:
                return pycountry.countries.get(**self.__dict__)
        except Exception as e:
            print(e)

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
            return r.json()[0]
        
class GeoFile:
    
    def __init__(self, string):
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
    
    def to_pyspark(self):
        SedonaRegistrator.registerAll(spark)
        
        gdf = self.to_geopandas()
        sparkGDF = spark.createDataFrame(gdf, schema = self.schema)
        return sparkGDF
    
    def schema(self):
        schema =  StructType([
            StructField('geometry', GeometryType())
            , StructField('shapeName', StringType())
            , StructField('shapeISO', StringType())
            , StructField('shapeID', StringType())
            , StructField('shapeGroup', StringType() )
            , StructField('shapeType', StringType())
        ])
        return schema
