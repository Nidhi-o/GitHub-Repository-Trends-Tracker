-- ============================================================
-- ATHENA VIEWS FOR GITHUB TRENDS ANALYTICS
-- Purpose: Creating a semantic layer for Metabase Visualization
-- ============================================================

-- 1. General Summary View
-- Cleaned dataset for general exploration, filtering out null languages
CREATE OR REPLACE VIEW github_trends_summary AS
SELECT 
    name, 
    language, 
    stargazers_count, 
    forks_count, 
    fetch_date
FROM "processed"
WHERE language IS NOT NULL;

-- 2. Time-Series Analytics View
-- Standardizing the fetch_date to a DATE type for time-series trend lines
CREATE OR REPLACE VIEW github_trends_view AS
SELECT 
    name,
    language,
    stargazers_count,
    forks_count,
    CAST(fetch_date AS DATE) as report_date
FROM "processed"
WHERE language IS NOT NULL;

-- 3. Keyword & Discovery View
-- Optimized for word-cloud visualizations by ensuring descriptions are populated
CREATE OR REPLACE VIEW keyword_cloud_view AS
SELECT 
    name,
    description,
    language,
    stargazers_count
FROM "processed"
WHERE description IS NOT NULL AND description != '';

-- 4. Top 50 Leaderboard
-- A snapshot of the high-impact repositories sorted by community engagement
CREATE OR REPLACE VIEW daily_trending_repos AS
SELECT 
    name,
    language,
    stargazers_count,
    fetch_date
FROM "processed"
ORDER BY stargazers_count DESC
LIMIT 50;
