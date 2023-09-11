-- Databricks notebook source
CREATE OR REFRESH LIVE TABLE iotevents_bronze
TBLPROPERTIES ("quality" = "bronze")
AS
SELECT
  *
FROM delta.`/mnt/datalake/raw/iotdevkit/`

-- COMMAND ----------


