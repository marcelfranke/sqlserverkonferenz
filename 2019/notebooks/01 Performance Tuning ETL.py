# Databricks notebook source
# MAGIC %md <h2>Create widget to choose source data folder<h2>

# COMMAND ----------

dbutils.widgets.dropdown("SF", "10", [str(x) for x in (10, 100)])
dbutils.widgets.dropdown("Source", "Blob", [str(x) for x in ("Blob", "DataLake")])

# COMMAND ----------

#create a parameter for the widget
paramScaleFactor = dbutils.widgets.get("SF")
paramSource = dbutils.widgets.get("Source")

# COMMAND ----------

mountPointBlob = "/mnt/data"
mountPoinDataLake = "/mnt/datalake"
sourcePath = ""

if paramSource == "Blob":
  sourcePath = mountPointBlob
elif paramSource == "DataLake":
  sourcePath = mountPoinDataLake

print(paramScaleFactor)
print(paramSource)
print(sourcePath)

# COMMAND ----------

# MAGIC %md <h2>Disable dbio cache</h2>

# COMMAND ----------

# disable dbio cache
# https://docs.databricks.com/user-guide/databricks-io-cache.html
spark.conf.set("spark.databricks.io.cache.enabled", "false")

# COMMAND ----------

# MAGIC %md <h2>Load order data as csv</h2>

# COMMAND ----------

#load data from storage account
order = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load(sourcePath+'/SF'+paramScaleFactor+'/orders.tbl')
order.printSchema()

# COMMAND ----------

order.count()

# COMMAND ----------

#todo why is cache not faster
#todo dbfsio enable dbio enable
# https://forums.databricks.com/questions/6834/cache-table-advanced-before-executing-the-spark-sq.html#answer-6900
# https://docs.databricks.com/user-guide/databricks-io-cache.html
order2 = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load(sourcePath+'/SF'+paramScaleFactor+'/orders.tbl').cache()
order2.printSchema()

# COMMAND ----------

order2.count()

# COMMAND ----------

# MAGIC %md <h4>define column names</h4>

# COMMAND ----------

#define colum names
order = order.withColumnRenamed("_c0", "orderkey")
order = order.withColumnRenamed("_c1", "custkey")
order = order.withColumnRenamed("_c2", "orderstatus")
order = order.withColumnRenamed("_c3", "totalprice")
order = order.withColumnRenamed("_c4", "orderdate")
order = order.withColumnRenamed("_c5", "orderpriority")
order = order.withColumnRenamed("_c6", "clerk")
order = order.withColumnRenamed("_c7", "shippriority")
order = order.withColumnRenamed("_c8", "comment")

order = order.drop("_c9")

order.printSchema()

# COMMAND ----------

# MAGIC %md <h2>Export order data as parquet<h2>

# COMMAND ----------

#coalesce(Anzahl Files)
order.write.option("compression","none").mode("overwrite").parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test1.parquet")
order.coalesce(1).write.option("compression","none").mode("overwrite").parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test1.parquet")

# COMMAND ----------

parquetDF = spark.read.parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test1.parquet)
parquetDF.printSchema()
parquetDF.count()

# COMMAND ----------

order.write.option("compression","gzip").mode("overwrite").parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test2.parquet")

# COMMAND ----------

parquetDF = spark.read.parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test2.parquet")
parquetDF.printSchema()
parquetDF.count()

# COMMAND ----------

order.write.option("compression","snappy").mode("overwrite").parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test3.parquet")

# COMMAND ----------

parquetDF = spark.read.parquet(sourcePath+"/performance/SF"+paramScaleFactor+"/orders_test3.parquet")
parquetDF.printSchema()
parquetDF.count()

# COMMAND ----------

# MAGIC %scala
# MAGIC val df = spark.sql("select * from tpch.nation").createOrReplaceTempView("nationview")
# MAGIC sqlContext.cacheTable("nationview")