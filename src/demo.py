from spatial import Point, Parcel
import json

from shapely.geometry import Polygon


# p = Point("A", 121.0, 14.6, name="Gate", tag="POI")
# print(p.id)
# print(p.lon, p.lat)
# print( p.to_tuple() )
# print( p.geometry.geom_type)

# ------------------------------


# my_big_dict = {
#     "id": 214,             # Passed as int to test str conversion
#     "lon": "121.0702",   # Passed as string to test float conversion
#     "lat": "14.6565",
#     "name": "GE Dept",
#     "tag": "building"
# }

# ge = Point.from_dict(my_big_dict)

# print(ge.id, ge.lon, ge.lat, ge.name, ge.tag)

# x = json.dumps(ge.as_dict())
# print( x )


# -----------------------------

# q = Point("A", 121.0, 14.6)
# print(q.bbox())


# -----------------------------

attributes = {
"area": 50.0,
"zone": "Residential",
"is_active": True
}

geom = Polygon([
(0, 0),
(10, 0),
(10, 5),
(0, 5)
])
parcel = Parcel(101, geom, attributes)
print(parcel.bbox())


# ---------------------------------------

x = json.dumps(parcel.as_dict())
print (x)

# ---------------------------------------

inside = Point("IN", 2, 2)
outside = Point("OUT", 12, 2)
print(inside.intersects(parcel)) # True
print(outside.intersects(parcel)) # False