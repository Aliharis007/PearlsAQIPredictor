import hopsworks
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Fetch Data
project = hopsworks.login(api_key_value=os.getenv("HOPSWORKS_API_KEY"))
fs = project.get_feature_store()
df = fs.get_feature_group("aqi_features", version=1).read()

# 2. Train Model
X = df[['hour', 'day', 'month', 'temp', 'humidity']]
y = df['aqi']
model = RandomForestRegressor().fit(X, y)

# 3. Register Model
joblib.dump(model, 'aqi_model.pkl')
mr = project.get_model_registry()
model_obj = mr.python.create_model("aqi_model", description="AQI Predictor")
model_obj.save('aqi_model.pkl')