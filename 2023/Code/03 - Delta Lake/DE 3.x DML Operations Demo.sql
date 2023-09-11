-- Databricks notebook source
-- MAGIC %md
-- MAGIC # CREATE DATABASE

-- COMMAND ----------

CREATE DATABASE IF NOT EXISTS DeepDiveIntoDeltaLake;

USE DeepDiveIntoDeltaLake;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # CREATE TABLE

-- COMMAND ----------

DROP TABLE IF EXISTS DimProduct;

CREATE TABLE DimProduct 
USING DELTA
--TBLPROPERTIES ('delta.autoOptimize.optimizeWrite'='true')
AS 
SELECT /*+ COALESCE(1) */ -- make sure the query is processed by one worker only so int only creates one file!
  col1 AS Product, 
  col2 AS price 
FROM VALUES ('Notebook', 900), ('PC', 1500), ('Tablet', 500);

SELECT *
FROM DimProduct

-- COMMAND ----------

SELECT * FROM json.`/user/hive/warehouse/deepdiveintodeltalake.db/dimproduct/_delta_log/00000000000000000000.json`

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # UPDATE

-- COMMAND ----------

UPDATE DimProduct
SET Price = 1300
WHERE Product = 'PC';

SELECT *
FROM DimProduct

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # DELETE

-- COMMAND ----------

DELETE FROM DimProduct
WHERE Product = 'PC';

SELECT *
FROM DimProduct

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # INSERT

-- COMMAND ----------

INSERT INTO DimProduct
VALUES ('Monitor', 200);

SELECT *
FROM DimProduct

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Analyze _delta_log

-- COMMAND ----------

-- MAGIC %python
-- MAGIC # managed tables are stored under /user/hive/warehouse/
-- MAGIC display(dbutils.fs.ls("/user/hive/warehouse/deepdiveintodeltalake.db/dimproduct/_delta_log"))

-- COMMAND ----------

SELECT 
  RIGHT(input_file_name(), 37) AS input_file_name, 
  add,
  remove
FROM json.`/user/hive/warehouse/deepdiveintodeltalake.db/dimproduct/_delta_log/*.json`
WHERE add IS NOT NULL OR remove IS NOT NULL
ORDER BY 1

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(dbutils.fs.ls("/user/hive/warehouse/deepdiveintodeltalake.db/dimproduct"))

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # VACUUM

-- COMMAND ----------

-- disable check to allow VACUUM of low retention periods  
SET spark.databricks.delta.retentionDurationCheck.enabled = false;

VACUUM DimProduct RETAIN 0 HOURS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # OPTIMIZE

-- COMMAND ----------

OPTIMIZE DimProduct

-- COMMAND ----------

DESCRIBE HISTORY DimProduct

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # RESTORE

-- COMMAND ----------

UPDATE DimProduct
SET Price = 1.400 -- wrong separator
WHERE Product = 'Notebook';

SELECT *
FROM DimProduct;

-- COMMAND ----------

DESCRIBE HISTORY DimProduct

-- COMMAND ----------

RESTORE DimProduct TO VERSION AS OF 6

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # CLONE

-- COMMAND ----------

CREATE TABLE DimProduct_Clone
SHALLOW CLONE DimProduct;

SELECT *
FROM DimProduct_Clone 

-- COMMAND ----------

UPDATE DimProduct_Clone
SET Price = 1.400 -- wrong separator
WHERE Product = 'Notebook';

SELECT *
FROM DimProduct_Clone;

-- COMMAND ----------

SELECT *
FROM DimProduct

-- COMMAND ----------

CREATE OR REPLACE TABLE DimProduct
DEEP CLONE DimProduct_Clone;



-- COMMAND ----------

DESCRIBE HISTORY DimProduct
