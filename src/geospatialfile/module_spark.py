import shutil, os
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

def get_db_utils(spark):
    '''
    input: spark session
    output: an object
    description: returns a callable class to perform Databricks 
                 utility commands outside of a DB environment
    '''
    
    dbutils = None
    if spark.conf.get("spark.databricks.service.client.enabled") == "true":
        from pyspark.dbutils import DBUtils
        dbutils = DBUtils(spark)
    else:
        import IPython
        dbutils = IPython.get_ipython().user_ns["dbutils"]
    return dbutils

# initiate the session to use it local functions
dbutils = get_db_utils(spark)
