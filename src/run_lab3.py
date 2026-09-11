import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import shapely
from shapely.geometry import Polygon
from pyproj import Geod

from spatial import Point, PointSet, SpatialObject, Parcel


# ----------------------------
# Paths
# ----------------------------
DATA_PATH = "data/points.csv"
OUTPUT_DIR = "output"
SUMMARY_PATH = os.path.join(OUTPUT_DIR, "lab3_report.json")
PLOT_PATH = os.path.join(OUTPUT_DIR, "lab3_preview.png")


# ---------- Points of Interest ---------------------
MainLib_pt = Point("M", 121.071161525309, 14.6551117158583, name="MainLib", tag="POI")
Engg_pt = Point("E", 121.069620411672, 14.6566025074174, name="Engg", tag="POI")

#---wrong point tested
# Wrong_pt = Point("X", 121.069620411672, 114.6566025074174, name="Engg", tag="POI")
# error msg obtained:  raise ValueError("Latitude must be between -90 and 90")

print("POI Bounding Boxes")
print( MainLib_pt.name + "  " + str(MainLib_pt.bbox()) )
print( Engg_pt.name + "  " + str(Engg_pt.bbox()) )

#---------- Polygon construction ---------------------

attributes = {
"area": 50.0,
"zone": "Park",
"is_active": True
}

sunken_coords_wgs84 = Polygon([
(121.064361754527,14.6549167178063),
(121.064934168163,14.6560112230016),
(121.068626550633,14.656074125599),
(121.070733787646,14.6560804158588),
(121.072727799985,14.6560804158588),
(121.073017151933,14.6557281613131),
(121.073042312972,14.6546147853386),
(121.072740380504,14.6540235009228),
(121.070758948685,14.6539605983254),
(121.068664292191,14.6539291470266),
(121.064953038943,14.6538662444292)

])

geod = Geod(ellps="WGS84")
geod_area = abs(geod.geometry_area_perimeter(sunken_coords_wgs84)[0])


attributes = {
"area": geod_area,
"zone": "Park",
"is_active": True
}

SunkenGarden = Parcel("SunkenGarden", sunken_coords_wgs84, attributes)
print("Polygon Bounding Box")
print(SunkenGarden.bbox())

# print(MainLib_pt.intersects(SunkenGarden)) # True
# print(Engg_pt.intersects(SunkenGarden)) # False


# ----------------------------
# Save info to json
# ----------------------------
# Create output folder if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Build summary dictionary
summary = {
    "file": DATA_PATH,
    "points": {
        "Engg": Engg_pt.as_dict(),
        "MainLib": MainLib_pt.as_dict() 
    },

    "SunkenGarden": SunkenGarden.as_dict() ,
    "relationships": {
        "Engg_intersects_SunkenGarden": Engg_pt.intersects(SunkenGarden),
        "MainLib_intersects_SunkenGarden": MainLib_pt.intersects(SunkenGarden)
    }
    
}

# Write summary.json
with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(f"\nSaved summary to: {SUMMARY_PATH}")


# ---------------Plotting --------------

polygon = shapely.from_wkt(  SunkenGarden.as_dict()["geometry"] )
# 1. Extract X and Y coordinate arrays natively from Shapely
x, y = polygon.exterior.xy

fig, ax = plt.subplots()

# 2. Plot using standard native matplotlib
ax.fill(x, y, facecolor= 'lightblue', edgecolor= 'red', alpha=0.5, 
        lw= 1.5, label= SunkenGarden.parcel_id)

ax.scatter(MainLib_pt.lon, MainLib_pt.lat, color='green', marker= 'o', 
           s= 50, label= MainLib_pt.name, zorder= 3)

ax.scatter(Engg_pt.lon, Engg_pt.lat, color='orange', marker= '*', 
           s= 50, label= Engg_pt.name, zorder= 4)

ax.set_title("Parcel and Points Plot")
ax.axis('equal')  # Crucial to prevent spatial distortion
ax.legend(loc='upper right')
plt.tight_layout()

plt.xlabel("Longitude")
plt.ylabel("Latitude")




plt.savefig(PLOT_PATH, dpi=150, bbox_inches="tight")
plt.close()

print(f"Saved scatter plot to: {PLOT_PATH}")