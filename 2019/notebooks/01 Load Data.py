# Databricks notebook source
# MAGIC %md <h2>Create widget to choose source data folder<h2>

# COMMAND ----------

dbutils.widgets.dropdown("SF", "10", [str(x) for x in (10, 100)])

# COMMAND ----------

#create a parameter for the widget
paramScaleFactor = dbutils.widgets.get("SF")

# COMMAND ----------

# MAGIC %md <h2>Load data from storage account<h2>

# COMMAND ----------

# MAGIC %md <h4>Load nation</h4>

# COMMAND ----------

#load data from storage account
nation = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/nation.tbl')
nation.printSchema()

# COMMAND ----------

display(nation)

# COMMAND ----------

#define colum names
nation = nation.withColumnRenamed("_c0", "nationkey")
nation = nation.withColumnRenamed("_c1", "name")
nation = nation.withColumnRenamed("_c2", "regionkey")
nation = nation.withColumnRenamed("_c3", "comment")

nation = nation.drop("_c4")

nation.printSchema()

# COMMAND ----------

nation.write.saveAsTable("tpch.nation")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.nation

# COMMAND ----------

# MAGIC %md <h4>Load part</h4>

# COMMAND ----------

#load data from storage account
part = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/part.tbl')
part.printSchema()

# COMMAND ----------

#define colum names
part = part.withColumnRenamed("_c0", "partkey")
part = part.withColumnRenamed("_c1", "name")
part = part.withColumnRenamed("_c2", "mfgr")
part = part.withColumnRenamed("_c3", "brand")
part = part.withColumnRenamed("_c4", "type")
part = part.withColumnRenamed("_c5", "size")
part = part.withColumnRenamed("_c6", "container")
part = part.withColumnRenamed("_c7", "retailprice")
part = part.withColumnRenamed("_c8", "comment")

part = part.drop("_c9")

part.printSchema()

# COMMAND ----------

#load data into table
part.write.saveAsTable("tpch.part")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.part

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.part
# MAGIC limit 100

# COMMAND ----------

# MAGIC %md <h4>Load part supp</h4>

# COMMAND ----------

#load data from storage account
partsupp = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/partsupp.tbl')
partsupp.printSchema()

# COMMAND ----------

#define colum names
partsupp = partsupp.withColumnRenamed("_c0", "partkey")
partsupp = partsupp.withColumnRenamed("_c1", "suppkey")
partsupp = partsupp.withColumnRenamed("_c2", "availqty")
partsupp = partsupp.withColumnRenamed("_c3", "supplycost")
partsupp = partsupp.withColumnRenamed("_c4", "comment")

partsupp = partsupp.drop("_c5")

partsupp.printSchema()

# COMMAND ----------

#load data into table
partsupp.write.saveAsTable("tpch.partsupp")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.partsupp

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.partsupp
# MAGIC limit 100

# COMMAND ----------

# MAGIC %md <h4>Load region</h4>

# COMMAND ----------

#load data from storage account
region = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/region.tbl')
region.printSchema()

# COMMAND ----------

#define colum names
region = region.withColumnRenamed("_c0", "regionkey")
region = region.withColumnRenamed("_c1", "name")
region = region.withColumnRenamed("_c2", "comment")

region = region.drop("_c3")

region.printSchema()

# COMMAND ----------

#load data into table
region.write.saveAsTable("tpch.region")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.region

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.region
# MAGIC limit 100

# COMMAND ----------

# MAGIC %md <h4>Load supplier</h4>

# COMMAND ----------

#load data from storage account
supplier = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/supplier.tbl')
supplier.printSchema()

# COMMAND ----------

#define colum names
supplier = supplier.withColumnRenamed("_c0", "suppkey")
supplier = supplier.withColumnRenamed("_c1", "name")
supplier = supplier.withColumnRenamed("_c2", "address")
supplier = supplier.withColumnRenamed("_c3", "nationkey")
supplier = supplier.withColumnRenamed("_c4", "phone")
supplier = supplier.withColumnRenamed("_c5", "acctbal")
supplier = supplier.withColumnRenamed("_c6", "comment")

supplier = supplier.drop("_c7")

supplier.printSchema()

# COMMAND ----------

#load data into table
supplier.write.saveAsTable("tpch.supplier")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.supplier

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.supplier
# MAGIC limit 100

# COMMAND ----------

# MAGIC %md <h4>Load customer</h4>

# COMMAND ----------

#load data from storage account
customer = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/customer.tbl')
customer.printSchema()

# COMMAND ----------

#define colum names
customer = customer.withColumnRenamed("_c0", "custkey")
customer = customer.withColumnRenamed("_c1", "name")
customer = customer.withColumnRenamed("_c2", "address")
customer = customer.withColumnRenamed("_c3", "nationkey")
customer = customer.withColumnRenamed("_c4", "phone")
customer = customer.withColumnRenamed("_c5", "acctbal")
customer = customer.withColumnRenamed("_c6", "mktsegment")
customer = customer.withColumnRenamed("_c7", "comment")

customer = customer.drop("_c8")

customer.printSchema()

# COMMAND ----------

#load data into table
customer.write.saveAsTable("tpch.customer")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.customer

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.customer
# MAGIC limit 100

# COMMAND ----------

# MAGIC %md <h4>Load order</h4>

# COMMAND ----------

#load data from storage account
order = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/orders.tbl')
order.printSchema()

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

#load data into table
order.write.saveAsTable("tpch.order")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.order

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.order
# MAGIC limit 100

# COMMAND ----------

# MAGIC %md <h4>Load lineitem</h4>

# COMMAND ----------

#load data from storage account
lineitem = sqlContext.read.format('csv').options(header='false', inferSchema='true', delimiter='|').load('/mnt/data/SF'+paramScaleFactor+'/lineitem.tbl')
lineitem.printSchema()

# COMMAND ----------

#define colum names
lineitem = lineitem.withColumnRenamed("_c0", "orderkey")
lineitem = lineitem.withColumnRenamed("_c1", "partkey")
lineitem = lineitem.withColumnRenamed("_c2", "suppkey")
lineitem = lineitem.withColumnRenamed("_c3", "linenumber")
lineitem = lineitem.withColumnRenamed("_c4", "quantity")
lineitem = lineitem.withColumnRenamed("_c5", "extendedprice")
lineitem = lineitem.withColumnRenamed("_c6", "discount")
lineitem = lineitem.withColumnRenamed("_c7", "tax")
lineitem = lineitem.withColumnRenamed("_c8", "returnflag")
lineitem = lineitem.withColumnRenamed("_c9", "linestatus")
lineitem = lineitem.withColumnRenamed("_c10", "shipdate")
lineitem = lineitem.withColumnRenamed("_c11", "commitdate")
lineitem = lineitem.withColumnRenamed("_c12", "receiptdate")
lineitem = lineitem.withColumnRenamed("_c13", "shipinstruct")
lineitem = lineitem.withColumnRenamed("_c14", "shipmnode")
lineitem = lineitem.withColumnRenamed("_c15", "comment")

lineitem = lineitem.drop("_c16")

lineitem.printSchema()

# COMMAND ----------

#load data into table
lineitem.write.saveAsTable("tpch.lineitem")

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*)
# MAGIC from tpch.lineitem

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from tpch.lineitem
# MAGIC limit 100