# Refactoring Point: Geometry becomes a Shapely Object

Objective

refactor the Point Class from previous exercise to use external library Shapely to define its geometry, while preserving its public interface

Dependencies
Shapely, pandas, matplotlib

Scripts

src\spatial.py contains classes like Point, SpatialObject, and Parcel
src\demo.py for incremental testing 
src\run_lab3.py for generating final output


MILESTONES
1. Configured project environment
2. Refactored Point class using Shapely geometry, tested with demo.py to see if it still retains public access like before
3. Added structured data boundaries with from_dict and as_dict, and tested in demo
4. Created SpatialObject class
5. Refactored Point to inherit from SpatialObject, tested methods in demo
6. Created Parcel class that inherits from ParcelObject, tested methods in demo
7. Completed runner script, with JSON reporting and plotting


REFLECTIONS
1. The main thing that changed in the Point class is its geometric representation, which we left inherited from SpatialObject, whose geometry is mostly handled by a Shapely geometry. The public interface never changed, which is nice since no extra coding is done, and other runner scripts that previously called it is not affected at all, so other people that use the class can still use it with minimal to no change in their codebase.

2. Shapely now handles the geometry representation, which is great since that library has been stable for years anyways, and has more geoemtry methods that surpass what we (the class maker) would ever need for our purposes. 
SpatialObject becomes the main abstract class that will be inherited from by other classes that has geometric properties. Very clean organization.
Point and Parcel classes now handle every method that are beyond the basic geometry, like other attributes.

3. Putting that validation in the constructor reduces redundant checking of objects, which as you go deeper in the inheritance becomes cumbersome.
Also, by putting it in the constructor, then we prevent creating objects that contain illogical/illegal values. We can print and read the error from the start, and prevent tedious debugging later on because of illogical values going thu methods

4. Doing it like this protects the primary geometry of your data, making it less exposed to other coders and classes. In most systems this is more secure, although it comes with the cost of parsing WKT / JSON / text files.

5. Because it is logical to do so. Intersect means the same thing anyways for points, polygons, for any implementation of spatial topology. writing it differently for each class is redunadant, and might lead to different implementation down the line, which makes code review later harder. Better for it to be in just one place.

6. That is a CRS issue. For it to translate to real world distance, we need to specify the reference system. I experimented with doing this for the area of the parcel in the runner script, using the pyproj library :)

7. Having shapely handle the geometry helps in maintainability because this is maintained by other programmers, and is optimized in terms of processing times so this scales even at larger scales.

To be honest, I don't think there will be performance problems if we stick to Point and Parcel objects, even if they grow to millions. What I anticipate having a problem is when we aggregate the points and put them in the PointSet class.

Imagine later on that we need to extend the functionality of intersects to the points inside the point class and output points only within the parcel. That does not scale at all if there are no indexing involved. I've seen this in just hundreds of thousands in ArcGIS and QGIS, and I imagine that is going to happen in a python code too. Recall that the PointSet only has one bounding box. It would be better if each of the bounding box/geometry of each point is quickly compared with the bbox of the parcel first, so only points near are already evaluated, before doing the more compute-heavy work of intersection.
