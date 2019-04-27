library(rgdal)
library(raster)

capri <- readOGR('/home/jamey/Documents/datakind/natgeo/data/Vegetation types_ Caprivi/veg_type_capri.geojson')
capri$VEG_STRUC <- as.character(capri$VEG_STRUC)

targets <- c('Tall Open Grassland', 'Tall Closed Grassland', 
             'High Closed Grassland', 'High Closed Shrubland',
             'Wetland')

base <- '/home/jamey/Documents/datakind/natgeo/data/Vegetation types_ Caprivi/lc_polys'


for (i in 1:length(targets)) {
  d <- capri[capri$VEG_STRUC==targets[i], ]
  n <- gsub(" ", "_", targets[i])
  writeOGR(d, dsn=paste0(base, '/', n, '.kml'), layer=n, driver='KML')
}


