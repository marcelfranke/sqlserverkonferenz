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

# MAGIC %md <h2>Call PowerBI API for each stream event</h2>

# COMMAND ----------

# MAGIC %scala
# MAGIC /*
# MAGIC direct streaming to power bi via Streaming API
# MAGIC //limit streaming data set
# MAGIC //map funktion im stream
# MAGIC 
# MAGIC // Limitation: https://docs.microsoft.com/en-us/power-bi/developer/api-rest-api-limitations
# MAGIC 
# MAGIC sample CURL call 
# MAGIC we need to make one call for each row that want to push to PowerBI streaming API
# MAGIC   e.g. in a map function which is execute on top of the streamint-dataframe (if this is possible)
# MAGIC curl --include \
# MAGIC   --request POST \
# MAGIC   --header "Content-Type: application/json" \
# MAGIC   --data-binary "[
# MAGIC   {
# MAGIC     \"DeviceID\" :\"AAAAA555555\",
# MAGIC     \"MessageID\" :98.6,
# MAGIC     \"Temperature\" :98.6,
# MAGIC     \"Humidity\" :98.6,
# MAGIC     \"EnqueuedTime\" :\"2019-01-15T10:53:35.838Z\"
# MAGIC   }
# MAGIC   ]" \
# MAGIC   "https://api.powerbi.com/beta/69389949-2078-4be9-8680-e499fac64209/datasets/b6347eb5-2f2b-429d-bb0a-8b6820d1be84/rows?key=oCK2yEl3KYChqYXGVPnCQYNUo2g3faDrO7U92rPWH%2F8RIrEGFbP81PuzAGjHqF4ZPzkIJF1laqqxOrqro2jO1A%3D%3D"

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC import org.apache.spark.sql.ForeachWriter
# MAGIC import sys.process._
# MAGIC import org.apache.log4j._ 
# MAGIC 
# MAGIC object Holder extends Serializable { 
# MAGIC     @transient lazy val log = Logger.getLogger(getClass.getName) }
# MAGIC     
# MAGIC val writer = new ForeachWriter[Row] {
# MAGIC   override def open(partitionId: Long, version: Long) = true
# MAGIC   
# MAGIC   override def process(value: Row) = {
# MAGIC     val deviceId = value(0)
# MAGIC     val messageId = value(1)
# MAGIC     val temperature = value(2) 
# MAGIC     val humidity = value(3)
# MAGIC     val enqueuedTime = value(4)
# MAGIC     
# MAGIC     //println(s"New test to PowerBI: $value")
# MAGIC     //val someRdd = Holder.log.info(">>> "+value)
# MAGIC     
# MAGIC     val command = """curl --include --request POST --header "Content-Type: application/json" --data-binary """ + 
# MAGIC     """"[{""" + 
# MAGIC     """\"DeviceID\": \"""" + deviceId + """\", """ + 
# MAGIC     """\"MessageID\": \"""" + messageId + """\", """ + 
# MAGIC     """\"Temperature\": \"""" + temperature + """\", """ + 
# MAGIC     """\"Humidity\": \"""" + humidity + """\", """ + 
# MAGIC     """\"EnqueuedTime\": \"""" + enqueuedTime + """\" """ + 
# MAGIC     """}]" "https://api.powerbi.com/beta/69389949-2078-4be9-8680-e499fac64209/datasets/b6347eb5-2f2b-429d-bb0a-8b6820d1be84/rows?key=oCK2yEl3KYChqYXGVPnCQYNUo2g3faDrO7U92rPWH%2F8RIrEGFbP81PuzAGjHqF4ZPzkIJF1laqqxOrqro2jO1A%3D%3D" """
# MAGIC     Seq("/bin/bash", "-c", command).!!
# MAGIC   }
# MAGIC   override def close(errorOrNull: Throwable) = {}
# MAGIC }

# COMMAND ----------

# MAGIC %scala
# MAGIC //val results = output.map(r => r.getString(0))
# MAGIC 
# MAGIC eventStream.writeStream
# MAGIC   .queryName("rest-api-processor")
# MAGIC   .foreach(writer)
# MAGIC   .start()

# COMMAND ----------

