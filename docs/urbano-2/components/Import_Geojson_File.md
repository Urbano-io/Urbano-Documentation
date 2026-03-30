# ![Import Geojson File icon](../images/icons/Import_Geojson_File.png) Import Geojson File

![Import Geojson File component](../images/components/Import_Geojson_File-crop.png)

Import Geojson File

#### Input
* ##### Geojson File Path [Text]
  Geojson file path (.geojson)
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