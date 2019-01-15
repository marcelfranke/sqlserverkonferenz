# Databricks notebook source
# MAGIC %sql
# MAGIC select count(*) from tpch.customer

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.customer where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.lineitem

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.lineitem where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.nation

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.nation where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.order

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.order where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.part

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.part where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.partsupp

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.partsupp where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.region

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.region where 1=1

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from tpch.supplier

# COMMAND ----------

# MAGIC %sql
# MAGIC cache select * from tpch.supplier where 1=1