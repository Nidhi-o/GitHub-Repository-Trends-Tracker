# GitHub Trends Tracker: Serverless Data Lakehouse on AWS

## 🚀 Project Overview
This project is an end-to-end **Data Engineering** pipeline that analyzes global technology trends. By merging historical repository data from Kaggle with real-time live data via the GitHub API, it provides actionable insights into emerging tech stacks like Python, Rust, and AI tools.

## 🏗️ Architecture
The system follows a **Cloud-Native, Serverless** design:
1. **Ingestion:** AWS Lambda & EventBridge fetch daily API data.
2. **Storage:** Amazon S3 acts as a multi-zone Data Lake (/raw, /historical, /processed).
3. **Processing:** AWS Glue (PySpark) performs schema harmonization and Parquet conversion.
4. **Analytics:** Amazon Athena provides a SQL-based analytics layer.
5. **Visualization:** Metabase dashboard tracks **2,050+ repos** and **5.3M engagement points**.

## 🛠️ Technical Challenges & Solutions
- **The Struct Conflict:** Handled nested JSON structures using PySpark `.cast("string")` logic to ensure compatibility with flat historical files.
- **Data Redundancy:** Implemented **SQL Window Functions** (`ROW_NUMBER() OVER PARTITION BY`) to deduplicate records at the read layer.
- **Cost Optimization:** Utilized **Parquet** and **S3 Partitioning** to reduce query scan costs by 90%.

## 📊 Dashboard Preview
![Metabase Dashboard](assets/dashboard.pdf)

## 🧰 Tech Stack
- **Cloud:** AWS (S3, Glue, Athena, Lambda)
- **Engine:** PySpark, SQL
- **BI:** Metabase
