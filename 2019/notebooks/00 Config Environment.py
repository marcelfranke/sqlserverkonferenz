# Databricks notebook source
# MAGIC %md <h2>List secret scopes</h2>

# COMMAND ----------

dbutils.secrets.help()

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

dbutils.secrets.list("key-vault-secrets")

# COMMAND ----------

# MAGIC %md <h2>Create storage account mountpoint</h2>

# COMMAND ----------

storageAccountName = "sqlserverkonferenz2019"
containerName = "data"
confKey = "fs.azure.account.key." + storageAccountName + ".blob.core.windows.net"

dbutils.fs.mount(
  source = "wasbs://"+containerName+"@"+storageAccountName+".blob.core.windows.net",
  mount_point = "/mnt/data",
  extra_configs = {confKey:dbutils.secrets.get(scope = "key-vault-secrets", key = "sqlconfstorageaccountkey")})

# COMMAND ----------

dbutils.fs.ls("/mnt/data")

# COMMAND ----------

# MAGIC %md <h2>Create database</h2>

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE TPCH