from spatial import Point

p = Point("A", 121.0, 14.6, name="Gate", tag="POI")
print(p.id)
print(p.lon, p.lat)
print( p.to_tuple() )
print( p.geometry.geom_type)