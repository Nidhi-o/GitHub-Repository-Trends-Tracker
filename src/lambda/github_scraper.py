import json
import boto3
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from datetime import datetime, timedelta

# Use Environment Variables for Security
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')  
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'github-trends-tracker-23it109')               

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Dynamic Date: Get repos created in the last 30 days
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    params = {
        "q": f"created:>{thirty_days_ago} sort:stars-desc",
        "per_page": 50
    }
    
    url = "https://api.github.com/search/repositories?" + urlencode(params)
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHub-Trends-Tracker"
    }
    
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))["items"]
        
        # 2. Hive-Style Partitioning for S3
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        
        # Path structure: raw/daily/year=YYYY/month=MM/day=DD/data.json
        filename = f"raw/daily/year={year}/month={month}/day={day}/trending_{now.strftime('%H%M')}.json"
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json.dumps(data, indent=2)
        )
        
        print(f"✅ SUCCESS: Fetched {len(data)} repos → {filename}")
        return {"status": "success", "path": filename}
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise e
