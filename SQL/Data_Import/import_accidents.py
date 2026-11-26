
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("Dataset/Processed/cleaned_indian_roads.csv")
df["festival"] = df["festival"].fillna("Non-Festival").replace("None", "Non-Festival")

df = df.rename(columns={"date": "accident_date", "time": "accident_time"})
columns = [
    "accident_id", "city", "state", "latitude", "longitude",
    "accident_date", "accident_time", "hour", "day_of_week", "is_weekend",
    "road_type", "lanes", "traffic_signal", "weather", "visibility",
    "temperature", "traffic_density", "cause", "accident_severity",
    "vehicles_involved", "casualties", "is_peak_hour", "festival", "risk_score",
]
df = df[columns]

password = quote_plus("MySQL@12345")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost:3306/smart_city_traffic")
df.to_sql("road_accidents", con=engine, if_exists="append", index=False, chunksize=1000)

print(f"Imported {len(df)} rows into smart_city_traffic.road_accidents.")
