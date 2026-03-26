# ![](../images/icons/Osm_Feature_Query.png) Osm Feature Query

![](../images/components/Osm_Feature_Query-crop.png)

Generate OSM feature queries suitable for input to the Import Osm File

#### Input
* ##### Osm Feature Query [Text list]
               Define one or more OpenStreetMap tag queries to filter features.              Query syntax:             • x=y → Exact key–value match             Example: amenity=parking             • x=* → Any value for a given key             Example: building=*             • *=y → Any key with a given value             Example: *=school             • (x) → Vague text search (key or value)             Example: (parking)              Input format:             Provide a list of query strings. Each query is evaluated independently and combined as a union.             

#### Output
* ##### Osm Features [Text list]
               Define one or more OpenStreetMap tag queries to filter features.              Query syntax:             • x=y → Exact key–value match             Example: amenity=parking             • x=* → Any value for a given key             Example: building=*             • *=y → Any key with a given value             Example: *=school             • (x) → Vague text search (key or value)             Example: (parking)              Input format:             Provide a list of query strings. Each query is evaluated independently and combined as a union.             