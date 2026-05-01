# 🚀 Project Setup & Replication Guide

Follow these steps to deploy the **GitHub Trends Tracker** infrastructure on AWS.

### Prerequisites
- An AWS Account with **IAM Administrator** access.
- A **GitHub Personal Access Token** (for the Lambda scraper).
- **Metabase** (running locally via JAR or Docker).

### Step 1: Data Lake Initialization
1. Create an S3 Bucket named `github-trends-tracker-[your-id]`.
2. Create three core directories:
   - `/raw/daily/` (for API landing).
   - `/historical/` (for the Kaggle CSV).
   - `/processed/` (for the final Parquet output).

### Step 2: Ingestion Layer (Lambda)
1. Deploy the Python script in `src/lambda/` to an **AWS Lambda** function.
2. Set **Environment Variables**: `GITHUB_TOKEN` and `BUCKET_NAME`.
3. Create an **EventBridge** rule to trigger the function daily.

### Step 3: Transformation Layer (Glue)
1. Run a **Glue Crawler** on the `/raw` and `/historical` folders to populate the Data Catalog.
2. Create a **Glue ETL Job** using the PySpark script in `src/glue/`.
3. Ensure the IAM Role for Glue has `S3FullAccess` and `AWSGlueServiceRole` permissions.

### Step 4: Analytics Layer (Athena)
1. Open the **Amazon Athena** console.
2. Run the SQL scripts in `src/sql/athena_views.sql` to create the semantic views for reporting.

### Step 5: Visualization (Metabase)
1. Connect Metabase to Athena using the **JDBC Driver**.
2. Select the `github_trends_view` or `daily_trending_repos` views as your data source.
3. Build the dashboard components as shown in the `assets/` folder.
