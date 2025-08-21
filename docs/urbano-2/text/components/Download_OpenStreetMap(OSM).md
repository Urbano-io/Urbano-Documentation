# ![](../../images/icons/Download_OpenStreetMap(OSM).png) Download OpenStreetMap(OSM)

![](../../images/components/Download_OpenStreetMap(OSM).png)

Download all OSM data within given bounds (be careful with the size of the region). OSM data will be downloaded to a cache and accessible by using the URL as input to import components. Providing the file path input will copy the data to the given location and can then be used to import later

#### Inputs
* ##### Left []
Left Bound (Longitude, x-axis) of the OSM region
* ##### Right []
Right Bound (Longitude, x-axis) of the OSM region
* ##### Top []
Top Bound (Latitude, y-axis) of the OSM region
* ##### Bottom []
Bottom Bound (Latitude, y-axis) of the OSM region
* ##### Path []
File path to save downloaded OSM data to (optional - can use URL as path to import because of cached downloads)
* ##### Run []
Toggle to start downloading OSM data

#### Outputs
* ##### URL
URL used to download data (can use URL as path to import features, network, etc. because of cached downloads)
* ##### File
Path to downloaded OSM file