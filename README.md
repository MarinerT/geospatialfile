# geoboundaries

This is developing python code/package where one can enter a country name, two-digit or three-digit alpha iso code and pull the historical geospatial boundaries from GeoBoundaries.org. https://www.geoboundaries.org

### Use

```python
from geoboundaries import GeoBoundary
egypt = GeoBoundary('Egypt')
egypt_gdf = egypt.to_geopandas()
```

```python
from geoboundaries import GeoBoundary
egypt = GeoBoundary('EG')
egypt_gdf = egypt.to_geopandas()
```

```python
from geoboundaries import GeoBoundary
egypt = GeoBoundary('EGY')
egypt_gdf = egypt.to_geopandas()
```
