# Databricks notebook source
# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS streaming.events

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS streaming.events
# MAGIC     USING PARQUET
# MAGIC     LOCATION "/mnt/data/IoTDevKitPowerBI"

# COMMAND ----------

