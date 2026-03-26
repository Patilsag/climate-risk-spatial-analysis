import osmnx as ox
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Setup
path = "layers/raw/berlin_data.gpkg"
os.makedirs("results", exist_ok=True)
PLACE_NAME = "Mitte, Berlin, Germany"

print(f"🌍 Fetching and analyzing data for {PLACE_NAME}...")

# 2. Download Layers (Ensures they exist!)
# Get Boundary
boundary = ox.geocode_to_gdf(PLACE_NAME).to_crs(epsg=25833)

# Get Assets (Schools/Hospitals)
tags_assets = {"amenity": ["hospital", "school", "kindergarten"]}
assets = ox.features_from_place(PLACE_NAME, tags=tags_assets)
assets = assets[assets.geometry.type.isin(['Point', 'Polygon'])].to_crs(epsg=25833)
assets["geometry"] = assets.centroid

# Get Parks (Cooling Islands)
tags_parks = {"leisure": "park", "landuse": "grass"}
parks = ox.features_from_place(PLACE_NAME, tags=tags_parks)
parks = parks[parks.geometry.type.isin(['Polygon', 'MultiPolygon'])].to_crs(epsg=25833)

# 3. Save to GeoPackage (Refresh the file)
boundary.to_file(path, layer="boundary", driver="GPKG")
assets.to_file(path, layer="assets", driver="GPKG")
parks.to_file(path, layer="parks", driver="GPKG")

# 4. Spatial Analysis: Proximity to Cooling
print("📏 Calculating distance to nearest park...")
assets['dist_to_park_m'] = assets.geometry.apply(lambda x: parks.distance(x).min())

# Define Risk (German Planning Standard)
assets['risk_level'] = assets['dist_to_park_m'].apply(
    lambda x: 'Low' if x <= 150 else ('Medium' if x <= 300 else 'High')
)

# 5. Export Results
assets[['name', 'amenity', 'dist_to_park_m', 'risk_level']].to_csv("results/berlin_risk_report.csv", index=False)

# 6. Plotting the Risk Distribution
plt.figure(figsize=(10, 6))
colors = {'Low': 'forestgreen', 'Medium': 'orange', 'High': 'crimson'}
assets['risk_level'].value_counts().reindex(['Low', 'Medium', 'High']).plot(kind='bar', color=['forestgreen', 'orange', 'crimson'])
plt.title(f"Heat Risk Distribution in {PLACE_NAME}")
plt.ylabel("Number of Assets")
plt.xlabel("Risk Level (Distance to Park)")
plt.xticks(rotation=0)
plt.savefig("results/risk_distribution.png")

print(f"✅ Success! Check 'results/berlin_risk_report.csv' for the full list.")