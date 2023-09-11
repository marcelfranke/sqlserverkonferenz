# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md
# MAGIC # Defining the Data Ingestion
# MAGIC
# MAGIC This notebook demonstrates using Delta Live Tables (DLT) to process raw data as Stream from an EventHub through a series of tables to drive analytic workloads in the lakehouse. Here we demonstrate a medallion architecture, where data is incrementally transformed and enriched as it flows through a pipeline. This notebook focuses on the SQL syntax of DLT rather than this architecture, but a brief overview of the design:
# MAGIC
# MAGIC * The bronze table contains raw records loaded from the EventHub
# MAGIC * The silver table ...
# MAGIC * The gold table ...
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC
# MAGIC By the end of this notebook, students should feel comfortable:
# MAGIC * Declaring Delta Live Tables
# MAGIC * Ingesting data via a Streaming Job
# MAGIC * Enforcing data quality with constraints
# MAGIC * Adding comments to tables
# MAGIC * Describing differences in syntax and execution of live tables and streaming live tables

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Streaming Ingestion with EventHubs
# MAGIC
# MAGIC Databricks offers two ways of data loading: Streaming or Batch ingestion. In this example we will have a look on a Streaming Job. The notebook connects to a Message Queue of an Azure EventHub and continously reads data into our Bronze layer.
# MAGIC
# MAGIC In the first step we need to define the configuration of the EventHub for the Streaming Job:
# MAGIC - Connection String: 
# MAGIC - Consumer Group: 
# MAGIC - Start Offset: 

# COMMAND ----------

connectionString = "Endpoint=sb://ehplaygroundeventhub.servicebus.windows.net/;SharedAccessKeyName=reader;SharedAccessKey="+dbutils.secrets.get(scope="key-vault-secrets",key="eventHubSecret")+";EntityPath=iotdevkit"
consumerGroup = "databricks"

# COMMAND ----------

ehConf = {}
ehConf['eventhubs.connectionString'] = connectionString
ehConf['eventhubs.consumerGroup'] = consumerGroup

# For 2.3.15 version and above, the configuration dictionary requires that connection string be encrypted."""
ehConf['eventhubs.connectionString'] = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Define the Event Starting Position
# MAGIC
# MAGIC Next we need to define the starting position to read from the Message Queue. In this case we start from the beginning

# COMMAND ----------

from datetime import datetime as dt
import json

# Start from beginning of stream
startOffset = "-1"

# Create the positions
startingEventPosition = {
  "offset": startOffset,  
  "seqNo": -1,            #not in use
  "enqueuedTime": None,   #not in use
  "isInclusive": True
}

# Put the positions into the Event Hub config dictionary
ehConf["eventhubs.startingPosition"] = json.dumps(startingEventPosition)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Create a Read Stream
# MAGIC
# MAGIC Spark offers the readStream function to create a new inputStream.

# COMMAND ----------

inputStream = spark \
  .readStream \
  .format("eventhubs") \
  .options(**ehConf) \
  .load()

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ##Create a Write Stream
# MAGIC
# MAGIC The write stream loads all data from the input stream in a delta format into the bronze layer of our Data Lake.

# COMMAND ----------

writeStream = inputStream \
    .writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("path", "/mnt/datalake/raw/iotdevkit/") \
    .option("checkpointLocation", "/mnt/datalake/raw/iotdevkit-checkpoint") \
    .trigger(processingTime="60 seconds") \
    .start()

# COMMAND ----------


