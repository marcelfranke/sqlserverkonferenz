# Databricks notebook source
# MAGIC %md <h2>Query 1: Pricing Summary Report Query</h2>

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC   returnflag,
# MAGIC   linestatus,
# MAGIC   sum(quantity) as sum_qty,
# MAGIC   sum(extendedprice) as sum_base_price,
# MAGIC   sum(extendedprice*(1-discount)) as sum_disc_price,
# MAGIC   sum(extendedprice*(1-discount)*(1+tax)) as sum_charge,
# MAGIC   avg(quantity) as avg_qty,
# MAGIC   avg(extendedprice) as avg_price,
# MAGIC   avg(discount) as avg_disc,
# MAGIC   count(*) as count_order
# MAGIC from tpch_10.pqt_lineitem
# MAGIC where shipdate <= date '1998-12-01' -- interval - '[DELTA]' day (3)
# MAGIC group by
# MAGIC   returnflag,
# MAGIC   linestatus
# MAGIC order by
# MAGIC   returnflag,
# MAGIC   linestatus

# COMMAND ----------

# MAGIC %md <h2>Query 2: Minimum Cost Supplier Query</h2>

# COMMAND ----------

spark.conf.set("spark.sql.crossJoin.enabled", "false")

# COMMAND ----------

# MAGIC %sql
# MAGIC REFRESH TABLE tpch_10.pqt_supplier

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC select
# MAGIC   s.acctbal,
# MAGIC   s.name,
# MAGIC   n.name,
# MAGIC   p.partkey,
# MAGIC   p.mfgr,
# MAGIC   s.address,
# MAGIC   s.phone,
# MAGIC   s.comment
# MAGIC from tpch_10.pqt_partsupp ps
# MAGIC inner join tpch_10.pqt_part p on ps.partkey = p.partkey
# MAGIC inner join tpch_10.pqt_supplier s on ps.suppkey = s.suppkey
# MAGIC inner join tpch_10.pqt_nation n on s.nationkey = n.nationkey
# MAGIC inner join tpch_10.pqt_region r on n.regionkey = r.regionkey
# MAGIC where 1=1
# MAGIC   and r.name = 'EUROPE'
# MAGIC   and p.size = 15
# MAGIC   and p.type like 'STANDARD%'
# MAGIC   /*and ps.supplycost = 
# MAGIC   (
# MAGIC     select min(ps.supplycost)
# MAGIC     from tpch_10.pqt_partsupp ps
# MAGIC     inner join tpch_10.pqt_supplier s on ps.suppkey = s.suppkey
# MAGIC     inner join tpch_10.pqt_nation n on  s.nationkey = n.nationkey
# MAGIC     inner join tpch_10.pqt_region r on n.regionkey = r.regionkey
# MAGIC     where r.name = 'EUROPE'
# MAGIC   )*/
# MAGIC order by
# MAGIC   s.acctbal desc,
# MAGIC   n.name,
# MAGIC   s.name,
# MAGIC   p.partkey

# COMMAND ----------

# MAGIC %md <h2>Query 3: Shipping Priority Query</h2>

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC select
# MAGIC   l.orderkey,
# MAGIC   sum(l.extendedprice*(1-l.discount)) as revenue,
# MAGIC   o.orderdate,
# MAGIC   o.shippriority
# MAGIC from tpch_10.pqt_customer c
# MAGIC inner join tpch_10.pqt_order o on c.custkey = o.custkey
# MAGIC inner join tpch_10.pqt_lineitem l on o.orderkey = l.orderkey
# MAGIC where c.mktsegment = 'AUTOMOBILE'
# MAGIC and o.orderdate < '1995-03-15'
# MAGIC and l.shipdate > '1995-03-15'
# MAGIC group by
# MAGIC   l.orderkey,
# MAGIC   o.orderdate,
# MAGIC   o.shippriority
# MAGIC order by
# MAGIC   revenue desc,
# MAGIC   o.orderdate;

# COMMAND ----------

# MAGIC %md <h2>Query 4: Order Priority Checking Query</h2>

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC select
# MAGIC   o.orderpriority,
# MAGIC   count(*) as order_count
# MAGIC from tpch_10.pqt_order o
# MAGIC where o.orderdate >= '1993-07-01'
# MAGIC and o.orderdate < '1997-07-01' + interval '3' month
# MAGIC and exists 
# MAGIC   (
# MAGIC     select *
# MAGIC     from tpch_10.pqt_lineitem l
# MAGIC     where l.orderkey = o.orderkey
# MAGIC     and l.commitdate < l.receiptdate
# MAGIC   )
# MAGIC group by o.orderpriority
# MAGIC order by o.orderpriority;

# COMMAND ----------

