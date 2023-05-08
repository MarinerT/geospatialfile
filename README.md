# geoboundaries

This is developing python code/package where one can enter a country name, two-digit or three-digit alpha iso code and pull the historical geospatial boundaries from GeoBoundaries.org. https://www.geoboundaries.org

### Use

``` bash
pip install git+https://github.com/marinert/geospatialfile.git
```

#### **<span style="color:blue">class</span> Country**

Country is an extension of the pycountry package found [here on Pypi](https://pypi.org/project/pycountry/). One enters a two character or three character ISO or a name and it returns the Country namedtuple-like response from pycountry. If the ISO codes are not found then it returns a ValueError. Any other character length, it'll find the most similar.

```python

from geoboundaries import Country

country = Country("EGY").fetch 
# Example of the Return > Country(alpha_2='EG', alpha_3='EGY', flag='🇪🇬', name='Egypt', numeric='818', official_name='Arab Republic of Egypt')
```

#### **<span style="color:blue">class</span> Response**

```
from geospatialfile import GeoBoundary
egypt = GeoBoundary('Egypt')

# output formats available
egypt_gdf = egypt.to_geopandas()
egypt_json = egypt.to_json()
egypt_ps = egypt.to_pyspark(spark) # requires a spark environment like Databricks & Apache-Sedona .jar installed on the cluster.

#inputs 
egypt_string = "Egypt" # fuzzy search
egypt_string = "EG" # 2 char ISO alpha code
egypt_string = "EGY" # 3 char ISO alpha code
```
#### How to create your own package

try these tutorials:
https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html