# 4.1
Problem statement 4.1 of ARC inductions


## Description:
The script retrieves GPS coordinates and time stamps of the drone from the .srt file and the GeoData from the metadata of the images in the
"Images" folder. It then finds the distance between the drone and all the images at different intervals of time, and stores the images that lie within a certain distance of the drone in an Excel file along with the time stamp. 

## Distance Calculation
The distance calculated is the hypotenuse of a triangle with the base as the [Great-Circle distance](https://en.wikipedia.org/wiki/Great-circle_distance) between two points and the absolute difference of their altitudes taken as the height. This ignores the curvature of the earth due to relatively short distances between the points.


