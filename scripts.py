import osmnx as ox
import geopandas as gdf
import os

# 1. Setup Folders
folders = ["layers/raw", "layers/processed", "results"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# 2. Define Study Area
PLACE_NAME = "Mitte, Berlin, Germany"
print(f"🇩🇪 Fetching spatial data for {PLACE_NAME}...")

# 3. Get Administrative Boundary
city_boundary = ox.geocode_to_gdf(PLACE_NAME)
city_boundary = city_boundary.to_crs(epsg=25833) # Project FIRST
city_boundary.to_file("layers/raw/berlin_data.gpkg", layer="boundary", driver="GPKG")

# 4. Get Vulnerable Assets (Hospitals & Schools)
tags = {"amenity": ["hospital", "school", "kindergarten"]}
# --- FETCH DATA FIRST ---
vulnerable_assets = ox.features_from_place(PLACE_NAME, tags=tags)

# --- THEN PROCESS ---
# Filter to keep only points and polygons (cleaning the data)
vulnerable_assets = vulnerable_assets[vulnerable_assets.geometry.type.isin(['Point', 'Polygon'])]

# Project to UTM 33N (Meters) so the Centroid calculation is accurate
vulnerable_assets = vulnerable_assets.to_crs(epsg=25833)

# Calculate the Center Point (Centroid) for each building
vulnerable_assets["geometry"] = vulnerable_assets.centroid

# 5. Save to the same GeoPackage
vulnerable_assets.to_file("layers/raw/berlin_data.gpkg", layer="assets", driver="GPKG")

print("✅ Success! Berlin data saved to layers/raw/berlin_data.gpkg")