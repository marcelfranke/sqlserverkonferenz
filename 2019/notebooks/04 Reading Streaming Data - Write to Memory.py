# Databricks notebook source
# MAGIC %scala
# MAGIC 
# MAGIC import org.apache.spark.eventhubs.{ ConnectionStringBuilder, EventHubsConf, EventPosition }
# MAGIC import org.apache.spark.sql.functions.{ explode, split }
# MAGIC 
# MAGIC // To connect to an Event Hub, EntityPath is required as part of the connection string.
# MAGIC // Here, we assume that the connection string from the Azure portal does not have the EntityPath part.
# MAGIC 
# MAGIC val connectionString = ConnectionStringBuilder()
# MAGIC   .setNamespaceName("iothub-ns-playground-1036140-e653ea73fa")
# MAGIC   .setEventHubName("playgroundiothub2")
# MAGIC   .setSasKeyName("service")
# MAGIC   .setSasKey(dbutils.secrets.get(scope = "key-vault-secrets", key = "EventHubSasKey"))
# MAGIC   .build

# COMMAND ----------

# MAGIC %scala
# MAGIC import java.time.Duration
# MAGIC 
# MAGIC val eventHubsConf = EventHubsConf(connectionString)
# MAGIC   .setStartingPosition(EventPosition.fromEndOfStream)
# MAGIC   //.setStartingPosition(EventPosition.fromEnqueuedTime(Instant.now))
# MAGIC   .setConsumerGroup("databricks")
# MAGIC   .setReceiverTimeout(Duration.ofSeconds(60))

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC val inputStream = spark.readStream
# MAGIC   .format("eventhubs")
# MAGIC   .options(eventHubsConf.toMap)
# MAGIC   .load()

# COMMAND ----------

# MAGIC %scala
# MAGIC inputStream.printSchema

# COMMAND ----------

# MAGIC %scala
# MAGIC display(inputStream)

# COMMAND ----------

# MAGIC %md <h2>Define schema for body</h2>

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC import org.apache.spark.sql.types.{StructType, StructField, StringType, IntegerType, DoubleType};
# MAGIC 
# MAGIC val schema = new StructType()
# MAGIC   .add("deviceId", StringType)
# MAGIC   .add("messageId", StringType)
# MAGIC   .add("temperature", StringType)
# MAGIC   .add("humidity", StringType)
# MAGIC   
# MAGIC /*
# MAGIC {
# MAGIC     "deviceId": "AZ3166",
# MAGIC     "messageId": 3,
# MAGIC     "temperature": 28,
# MAGIC     "humidity": 59.900002
# MAGIC }
# MAGIC */

# COMMAND ----------

# MAGIC %scala
# MAGIC import org.apache.spark.sql.functions._
# MAGIC 
# MAGIC val eventStream = inputStream
# MAGIC   .select(inputStream("body").cast("string"),inputStream("enqueuedTime").cast("timestamp"))
# MAGIC   .select(from_json('body, schema) as 'message, 'enqueuedTime as 'enqueuedTime)
# MAGIC   .select(
# MAGIC      'message.getItem("deviceId").cast("string") as 'deviceId
# MAGIC     ,'message.getItem("messageId").cast("integer") as 'messageId
# MAGIC     ,'message.getItem("temperature").cast("double") as 'machineTemperature
# MAGIC     ,'message.getItem("humidity").cast("double") as 'ambientHumidity
# MAGIC     ,'enqueuedTime
# MAGIC     ,date_format('enqueuedTime, "yyyyMMdd") as 'enqueuedDate
# MAGIC   )

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC display(eventStream)

# COMMAND ----------

# MAGIC %md <h2>Write a query for event stream into memory</h2>

# COMMAND ----------

# MAGIC %scala
# MAGIC //spark.conf.set("spark.sql.shuffle.partitions", "2")
# MAGIC 
# MAGIC val query = (
# MAGIC   eventStream
# MAGIC     .writeStream
# MAGIC     .format("memory")
# MAGIC     .queryName("events")
# MAGIC     .outputMode("append")  // complete = all the counts should be in the table
# MAGIC     .start()
# MAGIC )

# COMMAND ----------

# MAGIC %sql
# MAGIC select *
# MAGIC from events

# COMMAND ----------

