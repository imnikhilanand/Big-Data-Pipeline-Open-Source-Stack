''' Preprocessing and migrating data from data lake to data warehouse'''

from functools import reduce
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.functions import split, col, monotonically_increasing_id, row_number
from pyspark.sql import functions as F
from pyspark.sql.functions import lit
from pyspark.sql import DataFrame
from pyspark.sql.window import Window

spark = SparkSession.builder.master("local").appName("hdfs_test").getOrCreate()
 
#orders_schema = StructType().add("_airbyte_ab_id", "string").add("_airbyte_emitted_at", "string").add("_airbyte_data", "json")

#orders_data=spark.read.csv("hdfs://localhost:9000/ecomm_data/data_lake/orders", schema=orders_schema)

orders_data = spark.read.text("src/batch/batch_processing/airbyte_test_data.csv")

orders_data = orders_data.filter("value not like '%_airbyte%'")

orders = orders_data.withColumn('order_id', split(orders_data['value'], ',').getItem(2)).withColumn('ordered_at', split(orders_data['value'], ',').getItem(3))

orders = orders.select(orders.order_id, orders.ordered_at)

orders = orders.withColumn('order_id', split(orders['order_id'], ':').getItem(1)).withColumn('ordered_at', split(orders['ordered_at'], '""').getItem(3))

orders.show(truncate=False)

