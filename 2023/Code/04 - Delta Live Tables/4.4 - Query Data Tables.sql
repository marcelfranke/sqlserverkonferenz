-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
-- MAGIC </div>

-- COMMAND ----------

select count(*)
from iotdevkit.iotevents_bronze

-- COMMAND ----------

select *
from iotdevkit.iotevents_bronze

-- COMMAND ----------

select count(*)
from iotdevkit.iotevents_silver

-- COMMAND ----------

select *
from iotdevkit.iotevents_silver

-- COMMAND ----------

SELECT count(*)
FROM iotdevkit.iotevents_gold

-- COMMAND ----------

SELECT *
FROM iotdevkit.iotevents_gold
ORDER by deviceId, eventEnqueuedDate, eventEnqueuedDateHour

-- COMMAND ----------


