# 🌍 Urban Heat Risk Analysis: Berlin Mitte
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![GIS](https://img.shields.io/badge/GIS-Spatial%20Analysis-green.svg)](https://qgis.org/)

## 📌 Project Overview
This project identifies **Climate Vulnerability Hotspots** in Berlin, Germany. Specifically, it analyzes the proximity of "Vulnerable Assets" (Schools, Kindergartens, and Hospitals) to "Urban Cooling Islands" (Parks and Green Spaces) in the district of **Mitte**.

In dense urban environments, the **Urban Heat Island (UHI)** effect poses a significant health risk. This tool automates the identification of facilities that lack sufficient access to cooling infrastructure.

## 🛠️ Tech Stack & Methodology
- **Data Source:** OpenStreetMap (via `OSMNX`)
- **Projections:** Official German Reference System **ETRS89 / UTM zone 33N (EPSG:25833)**
- **Buffer Analysis:** 300m "Heat Risk" radius based on the international **3-30-300 rule**.
- **Libraries:** `GeoPandas`, `OSMNX`, `Shapely`, `Matplotlib`, `Contextily`.

## 📊 Key Results
- **Automated Risk Scoring:** Every asset is categorized as Low, Medium, or High risk based on its distance to the nearest park.
- **Visual Evidence:** - `results/berlin_heat_risk.png`: Spatial map of risk zones.
  - `results/risk_distribution.png`: Statistical breakdown of vulnerability.
- **Actionable Data:** `results/berlin_risk_report.csv` provides a prioritized list for urban planners to target for tree-planting initiatives.

## 🚀 How to Run
1. Clone the repo.
2. Create a venv and run `pip install -r requirements.txt`.
3. Run `python analyze_risk.py`.
