-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
-- MAGIC </div>

-- COMMAND ----------

CREATE OR REFRESH LIVE TABLE iotevents_bronze
TBLPROPERTIES ("quality" = "bronze")
AS
SELECT
  *
FROM delta.`/mnt/datalake/raw/iotdevkit/`

-- COMMAND ----------

CREATE OR REFRESH LIVE TABLE iotevents_silver
TBLPROPERTIES ("quality" = "silver")
AS
SELECT
  string(body) AS body,
  string(body):IoTHub:ConnectionDeviceId AS connectionDeviceId,
  string(body):deviceId AS deviceId,
  cast(string(body):messageId AS integer) AS messageId,
  cast(string(body):temperature AS double) AS temperature,
  cast(string(body):humidity AS double) AS humidity,
  to_timestamp(string(body):EventProcessedUtcTime) AS eventProcessedUtcTime,
  to_timestamp(string(body):EventEnqueuedUtcTime) AS eventEnqueuedUtcTime,
  to_timestamp(string(body):EnqueuedTime) AS enqueuedTime,
  cast(partitionKey AS integer) AS partitionKey,
  cast(partition AS integer) AS partition,
  cast(sequenceNumber AS integer) AS sequenceNumber,
  cast(offset AS integer) AS offset,
  publisher,
  properties,
  systemProperties
FROM live.iotevents_bronze

-- COMMAND ----------

CREATE OR REFRESH LIVE TABLE iotevents_gold
TBLPROPERTIES ("quality" = "gold")
AS
SELECT
  connectionDeviceId,
  deviceId,
  to_date(eventEnqueuedUtcTime) as eventEnqueuedDate,
  hour(eventEnqueuedUtcTime) as eventEnqueuedDateHour,
  avg(temperature) as temperatureAvg,
  min(temperature) as temperatureMin,
  max(temperature) as temperatureMax,
  avg(humidity) as humidityAvg,
  min(humidity) as humidityMin,
  max(humidity) as humidityMax
FROM live.iotevents_silver
GROUP BY
  connectionDeviceId,
  deviceId,
  to_date(EventEnqueuedUtcTime),
  hour(EventEnqueuedUtcTime)

-- COMMAND ----------


