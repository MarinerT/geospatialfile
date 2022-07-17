# geospatialfile

This is developing python code/package where one can enter a country name, two-digit or three-digit alpha iso code and pull the historical geospatial boundaries from GeoBoundaries.org. https://www.geoboundaries.org

### Use

```python
from geospatialfile import GeoBoundary
egypt = GeoBoundary('Egypt')

# output formats available
egypt_gdf = egypt.to_geopandas()
egypt_json = egypt.to_json()
egypt_ps = egypt.to_pyspark()

#inputs 
egypt_string = "Egypt" # fuzzy search
egypt_string = "EG" # 2 char ISO alpha code
egypt_string = "EGY" # 3 char ISO alpha code
```
