import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, lit, current_date
from awsglue.dynamicframe import DynamicFrame

# --- CONFIGURATION (Easier for others to adapt) ---
DATABASE_NAME = "github_trends_db"
DAILY_TABLE = "daily"
HISTORICAL_TABLE = "historical"
S3_OUTPUT_PATH = "s3://YOUR_S3_BUCKET_NAME/processed/" # Changed to placeholder
# --------------------------------------------------

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# 1. READ SOURCES
# Pulling from the Glue Data Catalog
df_daily = glueContext.create_dynamic_frame.from_catalog(database=DATABASE_NAME, table_name=DAILY_TABLE).toDF()
df_hist = glueContext.create_dynamic_frame.from_catalog(database=DATABASE_NAME, table_name=HISTORICAL_TABLE).toDF()

# 2. ALIGN DAILY (Handling Nested JSON Structs)
# Casting to string then int to resolve Struct conflicts
df_daily_final = df_daily.select(
    col("name").alias("repo_name"),
    col("owner.login").cast("string").alias("owner_name"),
    col("language").cast("string"),
    col("stargazers_count").cast("string").cast("int").alias("stars"),
    col("forks_count").cast("string").cast("int").alias("forks"),
    current_date().alias("fetch_date")
)

# 3. ALIGN HISTORICAL (Merging Kaggle Data)
df_hist_final = df_hist.select(
    col("repo_name").cast("string"),
    col("owner").cast("string").alias("owner_name"),
    col("language").cast("string"),
    col("stars").cast("string").cast("int"),
    col("forks").cast("string").cast("int"),
    lit("2025-01-01").alias("fetch_date")
)

# 4. MERGE AND CLEAN
# Union datasets and remove duplicates for the same fetch date
df_combined = df_daily_final.union(df_hist_final).dropDuplicates(["repo_name", "fetch_date"])
dynamic_df = DynamicFrame.fromDF(df_combined, glueContext, "dynamic_df")

# 5. WRITE OUTPUT (Partitioned Parquet for Performance)
# Using Parquet format and Partitioning to optimize Athena query costs
glueContext.write_dynamic_frame.from_options(
    frame = dynamic_df,
    connection_type = "s3",
    connection_options = {"path": S3_OUTPUT_PATH, "partitionKeys": ["fetch_date"]},
    format = "parquet"
)
job.commit()
