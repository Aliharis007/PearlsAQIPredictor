import os
import requests
import pandas as pd
import datetime
from dotenv import load_dotenv
import hopsworks

load_dotenv()

def fetch_and_store():
    # 1. Fetch from AQICN API
    url = f"https://api.waqi.info/feed/karachi/?token={os.getenv('AQICN_TOKEN')}"
    response = requests.get(url).json()
    
    if response['status'] == 'ok':
        data = response['data']
        now = datetime.datetime.now()
        
        # 2. Compute Features
        df = pd.DataFrame([{
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": now.hour,
            "day": now.day,
            "month": now.month,
            "aqi": data['aqi'],
            "temp": data['iaqi'].get('t', {}).get('v', 0),
            "humidity": data['iaqi'].get('h', {}).get('v', 0)
        }])
        
        # 3. Store in Hopsworks
        project = hopsworks.login(api_key_value=os.getenv("HOPSWORKS_API_KEY"))
        fs = project.get_feature_store()
        aqi_fg = fs.get_or_create_feature_group(name="aqi_features", version=1, primary_key=["timestamp"])
        aqi_fg.insert(df)
        print("Features pushed to Hopsworks!")

if __name__ == "__main__":
    fetch_and_store()