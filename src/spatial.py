import math
import os
import csv

from shapely.geometry import Point as ShapelyPoint

class Point:
    def __init__(self, id, lon, lat, name=None, tag=None):
        if not ( -180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        if not ( -90 <= lat <= 90):
                    raise ValueError("Latitude must be between -90 and 90")
              
        self.id = id
        self.geometry = ShapelyPoint(lon, lat)
        self.name = name
        self.tag = tag

    @property
    def lon(self):
        return self.geometry.x

    @property
    def lat(self):
        return self.geometry.y
        
     
    # --------------------------
    # Instance methods (behavior belongs to the object)
    # -----------------------------
    def to_tuple(self) -> tuple[float, float]:
        """
        Return the coordinate as a (lon, lat) tuple
        """
        return (self.lon, self.lat)


    def distance_to(self, other):
          return Point.haversine_m(self.lon, self.lat, other.lon, other.lat)


    # ------------------------------------------------------------------
    # Static method (pure spatial math)
    # ------------------------------------------------------------------
    @staticmethod
    def haversine_m( lon1: float, lat1: float, lon2: float, lat2: float
    ) -> float:
        """
        Compute the Haversine distance between two lon/lat pairs in meters.
        Static method because it does not depend on object state.
        """
        R = 6_371_000.0 # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = ( math.sin(dphi / 2) ** 2 
             + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2 )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c


    # ------------------------------------------------------------------
    # Class method (constructing objects from data)
    # ------------------------------------------------------------------
    @classmethod
    def from_row(cls, row):
        return cls(
            id=str(row["id"]),
            lon=float(row["lon"]),
            lat=float(row["lat"]),
            name=row.get("name"),
            tag=row.get("tag"),
        )


    def is_poi(self):
        return (self.tag or "").lower() == "poi"


###---------------------------



class PointSet:
    def __init__(self, pointlist=None):
        self.pointlist = pointlist if pointlist is not None else []

        
    @classmethod
    def from_csv(cls, path):
        pointlist = []
        with open(path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    point = Point.from_row(row)
                    pointlist.append(point)
                except(ValueError) as e:
                    print(f"Skipping this row: {row} due to error in lon/lat value")

        return cls(pointlist)


    def count(self) -> int:
         return len(self.pointlist)


    def bbox(self):
        """Returns the bounding box as a tuple: (min_lon, min_lat, max_lon, max_lat)"""
        if not self.pointlist:
            raise ValueError("Cannot compute a bounding box for an empty PointSet.")

        min_lon = min(p.lon for p in self.pointlist)
        min_lat = min(p.lat for p in self.pointlist)
        max_lon = max(p.lon for p in self.pointlist)
        max_lat = max(p.lat for p in self.pointlist)

        return (min_lon, min_lat, max_lon, max_lat)


    def filter_by_tag(self, tag):
        tag_pointlist = [p for p in self.pointlist if p.tag == tag]

        return PointSet(tag_pointlist)

    