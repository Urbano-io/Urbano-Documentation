## ![](../images/icons/Import_SHP_File.png) Import SHP File

![](../images/components/Import_SHP_File-crop.png)

Import data from GIS shapefiles

#### Input
* ##### Shp File Path [Text]
  Shp file path (.shp)
* ##### Coordinate Reference [CR]
  Coordinate reference information for properly locating the geometries in the Rhino canvas
* ##### Cropping Geometry [Curve]
  Cropping Geometry
* ##### Cropping Boundary [Text]
  A string representing geographical boundary. (Use 'Geo Boundary' component to get the string)
* ##### Terrain [Boolean]
  If turned on, the component will try to download corresponding terrain data files into the parent folderof the user-specified file path.
* ##### Run [Boolean]
  Run

#### Output
* ##### Polylines [Geometry list]
  Polylines
* ##### Polygons [Geometry list]
  Polygons
* ##### Points [Geometry list]
  Points
* ##### Coordinate Reference [CR]
  Coordinate reference information for properly locating the geometries in the Rhino canvas
* ##### Boundary [Text]
  A string representing geographical boundary