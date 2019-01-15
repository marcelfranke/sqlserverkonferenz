# Databricks notebook source
# MAGIC %md <h2>Create widget to choose source data folder<h2>

# COMMAND ----------

dbutils.widgets.dropdown("SF", "10", ["10", "100"])

# COMMAND ----------

#create a parameter for the widget
paramScaleFactor = dbutils.widgets.get("SF")

rootFolder = '/mnt/data/SF'+paramScaleFactor+'/'

databaseName = "tpch_" + paramScaleFactor

print("RootFolder: " + rootFolder)
print("DatabaseName: " + databaseName)

# COMMAND ----------

# MAGIC %md <h2>Create external tables on over data in Storage Account<h2>

# COMMAND ----------

#Create Database
sqlCmd = "CREATE DATABASE IF NOT EXISTS TPCH_" + paramScaleFactor;
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %md <h4>Create table date</h4>

# COMMAND ----------

tableName = "date"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)

sqlCmd = """
CREATE TABLE """ + fullTableName + """ (`DateSID` INT, `DateKey` INT, `DateName` STRING, `DateValue` TIMESTAMP, `YearKey` INT, `YearName` INT, `HalfYearKey` INT, `HalfYearName` STRING, `HalfYearNumberKey` INT, `HalfYearNumberName` STRING, `QuarterKey` INT, `QuarterName` STRING, `QuarterNumberKey` INT, `QuarterNumberName` STRING, `MonthKey` INT, `MonthName` STRING, `MonthNumberKey` INT, `MonthNumberName` STRING, `WeekKey` INT, `WeekName` STRING, `WeekNumberKey` INT, `WeekNumberName` STRING, `DayOfWeekNumberKey` INT, `DayOfWeekNumberName` STRING, `ISOWeekKey` INT, `ISOWeekName` STRING, `ISOWeekNumberKey` INT, `ISOWeekNumberName` STRING, `ISOYearKey` INT, `ISOYearName` INT, `ISODayOfWeekNumberKey` INT, `ISODayOfWeekNumberName` STRING, `DayOfYearNumberKey` INT, `DayOfYearNumberName` INT, `DayOfMonthNumberKey` INT, `DayOfMonthNumberName` INT)
USING parquet
LOCATION '/mnt/data/Date.snappy.parquet'"""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %md <h4>Create table nation</h4>

# COMMAND ----------

tableName = "csv_nation"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (nationkey int, name string, regionkey int, comments string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/nation.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_nation

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_nation LIMIT 10

# COMMAND ----------

tableName = "pqt_nation"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (nationkey int, name string, regionkey int, comments string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/nation.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch_10.pqt_nation

# COMMAND ----------

# MAGIC %md <h4>Create table part</h4>

# COMMAND ----------

tableName = "csv_part"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (partkey int, name string, mfgr string, brand string, type string, size integer, container string, retailprice double, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/part.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_part

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_part LIMIT 10

# COMMAND ----------

tableName = "pqt_part"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (partkey int, name string, mfgr string, brand string, type string, size integer, container string, retailprice double, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/part.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch_10.pqt_part

# COMMAND ----------

# MAGIC %md <h4>Create table part supp</h4>

# COMMAND ----------

tableName = "csv_partsupp"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (partkey integer, suppkey integer, availqty integer, supplycost double, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/partsupp.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_partsupp

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_partsupp LIMIT 10

# COMMAND ----------

tableName = "pqt_partsupp"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (partkey integer, suppkey integer, availqty integer, supplycost double, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/partsupp.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch_10.pqt_partsupp

# COMMAND ----------

# MAGIC %md <h4>Create table region</h4>

# COMMAND ----------

tableName = "csv_region"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (regionkey integer, name string, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/region.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_region

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_region LIMIT 10

# COMMAND ----------

tableName = "pqt_region"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (regionkey integer, name string, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/region.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch_10.pqt_region

# COMMAND ----------

# MAGIC %md <h4>Create table supplier</h4>

# COMMAND ----------

tableName = "csv_supplier"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (suppkey integer, name string, address string, nationkey integer, phone string, acctbal double, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/supplier.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_supplier

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_supplier LIMIT 10

# COMMAND ----------

tableName = "pqt_supplier"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (suppkey integer, name string, address string, nationkey integer, phone string, acctbal double, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/supplier.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch_10.pqt_supplier

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from tpch_10.pqt_supplier

# COMMAND ----------

# MAGIC %md <h4>Create table customer</h4>

# COMMAND ----------

tableName = "csv_customer"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (custkey integer, name string, address string, nationkey integer, phone string, acctbal double, mktsegment string, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/customer.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_customer

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_customer LIMIT 10

# COMMAND ----------

tableName = "pqt_customer"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (custkey integer, name string, address string, nationkey integer, phone string, acctbal double, mktsegment string, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/customer.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.pqt_customer

# COMMAND ----------

# MAGIC %md <h4>Create table order</h4>

# COMMAND ----------

tableName = "csv_order"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (orderkey integer, custkey integer, orderstatus string, totalprice double, orderdate timestamp, orderpriority string, clerk string, shippriority integer, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/orders.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_order

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_order LIMIT 10

# COMMAND ----------

tableName = "pqt_order"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (orderkey integer, custkey integer, orderstatus string, totalprice double, orderdate timestamp, orderpriority string, clerk string, shippriority integer, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/orders.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.pqt_order

# COMMAND ----------

tableName = "pqt_order_part"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (orderkey integer, custkey integer, orderstatus string, totalprice double, orderdate timestamp, orderpriority string, clerk string, shippriority integer, comment string) USING PARQUET PARTITIONED BY (orderdate) OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/orders.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %md <h4>Create table lineitem</h4>

# COMMAND ----------

tableName = "csv_lineitem"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (orderkey integer, partkey integer, suppkey integer, linenumber integer, quantity integer, extendedprice double, discount double, tax double, returnflag string, linestatus string, shipdate timestamp, commitdate timestamp, receiptdate timestamp, shipinstruct string, shipmnode string, comment string) USING CSV OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "/lineitem.tbl\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.csv_lineitem

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM tpch_10.csv_lineitem LIMIT 10

# COMMAND ----------

tableName = "pqt_lineitem"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (orderkey integer, partkey integer, suppkey integer, linenumber integer, quantity integer, extendedprice double, discount double, tax double, returnflag string, linestatus string, shipdate timestamp, commitdate timestamp, receiptdate timestamp, shipinstruct string, shipmnode string, comment string) USING PARQUET OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/lineitem.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM tpch_10.pqt_lineitem

# COMMAND ----------

tableName = "pqt_lineitem_part"
fullTableName = databaseName + "." + tableName

# drop table if exists
sqlCmd = "DROP TABLE IF EXISTS " + fullTableName
sqlContext.sql(sqlCmd)
# craete table 
sqlCmd = "CREATE TABLE " + fullTableName + " (orderkey integer, partkey integer, suppkey integer, linenumber integer, quantity integer, extendedprice double, discount double, tax double, returnflag string, linestatus string, shipdate timestamp, commitdate timestamp, receiptdate timestamp, shipinstruct string, shipmnode string, comment string) USING PARQUET PARTITIONED BY (commitdate) OPTIONS (header \"false\", inferSchema \"false\", delimiter \"|\") LOCATION \"/mnt/data/SF" + paramScaleFactor + "parquet/lineitem.parquet\""
sqlContext.sql(sqlCmd)

# COMMAND ----------

