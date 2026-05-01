# 🛠️ Technical Challenges & Resolutions

During the implementation of the **GitHub Trends Tracker**, several architectural and data-level hurdles were encountered. Below is a log of how these were resolved.

### 1. Data Heterogeneity (The "Struct vs. Long" Conflict)
- **Challenge:** The GitHub API returns stars and forks as nested JSON objects or strings, while the historical Kaggle archive provided them as flat integers. AWS Glue Crawlers initially failed to merge these due to schema inconsistency.
- **Resolution:** Developed a **PySpark ETL script** that uses explicit type casting. By casting the API fields to `string` first and then `int`, I "forced" the schema to align with the historical baseline.

### 2. Data Redundancy & Historical Overlap
- **Challenge:** Daily API fetches often captured repositories already present in the historical archive, causing "double-counting" in the Metabase dashboard.
- **Resolution:** Implemented a **"Deduplication at Read"** strategy using **SQL Window Functions** (`ROW_NUMBER() OVER PARTITION BY`). This ensures only the most recent entry for any specific repository is displayed in the analytics layer.

### 3. Cost & Performance Optimization
- **Challenge:** Querying raw JSON/CSV files in S3 via Athena was slow and potentially expensive as the dataset grew.
- **Resolution:** Transformed the entire Data Lake into **Apache Parquet** format and implemented **Hive-style Partitioning** by `fetch_date`. This reduced data scan volumes by ~90%, significantly optimizing performance and query costs.

### 4. BI Tool Integration (Unique Index Violation)
- **Challenge:** Encountered a "Unique Index Violation" when attempting to update Metabase dashboards after changing the underlying SQL logic.
- **Resolution:** Shifted from the Metabase GUI "Notebook" editor to **Native SQL Views** in Athena. This bypassed metadata conflicts and allowed for more robust semantic layering.
