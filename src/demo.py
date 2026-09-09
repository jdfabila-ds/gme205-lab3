from spatial import Point
import json

p = Point("A", 121.0, 14.6, name="Gate", tag="POI")
print(p.id)
print(p.lon, p.lat)
print( p.to_tuple() )
print( p.geometry.geom_type)


my_big_dict = {
    "id": 214,             # Passed as int to test str conversion
    "lon": "121.0702",   # Passed as string to test float conversion
    "lat": "14.6565",
    "name": "GE Dept",
    "tag": "building"
}

ge = Point.from_dict(my_big_dict)

print(ge.id, ge.lon, ge.lat, ge.name, ge.tag)

x = json.dumps(ge.as_dict())
print( x )