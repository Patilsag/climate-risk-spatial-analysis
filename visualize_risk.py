import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

# 1. Load the data we saved
path = "layers/raw/berlin_data.gpkg"
boundary = gpd.read_file(path, layer="boundary")
assets = gpd.read_file(path, layer="assets")

# 2. Create the "Risk Zone" (Buffer)
# Since we are in EPSG:25833 (Meters), we can just say '500' for 500 meters
assets_buffer = assets.copy()
assets_buffer["geometry"] = assets_buffer.buffer(500)

# 3. Create a Professional Plot
fig, ax = plt.subplots(figsize=(12, 10))

# Plot the 500m Risk Buffers (Transparent Red)
assets_buffer.plot(ax=ax, color='red', alpha=0.2, edgecolor='red', label="Heat Risk Zone (500m)")

# Plot the actual Schools/Hospitals (Solid Points)
assets.plot(ax=ax, color='blue', markersize=15, label="Vulnerable Assets")

# Plot the City Boundary
boundary.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=2)

# 4. Add the Background Map (The "Context")
# This pulls the actual streets of Berlin automatically!
cx.add_basemap(ax, crs=assets.crs.to_string(), source=cx.providers.CartoDB.Positron)

plt.title("Climate Risk Analysis: Berlin Mitte\nHeat Vulnerability Zones (500m Radius)", fontsize=15)
plt.legend()
plt.tight_layout()
# Add this to your scripts.py
tags_parks = {"leisure": "park", "landuse": "grass"}
parks = ox.features_from_place("Mitte, Berlin, Germany", tags=tags_parks)
parks = parks[parks.geometry.type.isin(['Polygon', 'MultiPolygon'])]
parks = parks.to_crs(epsg=25833)
parks.to_file("layers/raw/berlin_data.gpkg", layer="parks", driver="GPKG")
print("🌳 Parks added to GeoPackage!")
# Save the result for your GitHub
plt.savefig("results/berlin_heat_risk.png", dpi=300)
print("✅ Risk Map saved to results/berlin_heat_risk.png")
plt.show()