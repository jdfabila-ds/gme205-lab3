# Refactoring Point: Geometry becomes a Shapely Object

Objective

refactor the Point Class from previous exercise to use external library Shapely to define its geometry, while preserving its public interface

Dependencies
Shapely, pandas, matplotlib

Scripts

src\spatial.py contains classes like Point, SpatialObject, and Parcel
src\demo.py for incremental testing 
src\run_lab3.py for generating final output


Milestones
1. Configured project environment
2. Refactored Point class using Shapely geometry, tested with demo.py to see if it still retains public access like before
3. Added structured data boundaries with from_dict and as_dict, and tested in demo
4. Created SpatialObject class
5. Refactored Point to inherit from SpatialObject, tested methods in demo
6. Created Parcel class that inherits from ParcelObject, tested methods in demo