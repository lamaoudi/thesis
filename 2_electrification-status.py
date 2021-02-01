## Import Libraries
import fiona
import rasterio.mask
import geopandas as gpd
import numpy as np

# OBJECTIVE: Classify households as in/out of an electrified region to the grid.
# NOTE: High-density regions, confirmed as cities, should me classified as electrified regions
# NOTE: Regions with high nighttime light intensity should be considered electrified as well

#VISUALIZATION: Nighttime Light and population density linear graph (is there a correlation)
    # HOW? By extrapolating average nighttime light intensities to sectors.
    # Map the data with tier 0 and 1 and without

#OUTPUT: 2 csv files: (1) households electrified (2) households unelectrified

#Graph tier, tier of where each is
# DATASET: Falchetta

# Map the data with tier 0 and 1 and without
# https://github.com/giacfalk/Electrification_SSA_data

## GADM DATA, Level 1
pathto_gadm = "data/gadm36_"
country_code = 'RWA'
path_adm1 = pathto_gadm + country_code + '_shp/gadm36_' + country_code + '_0.shp'

## Read shp file as feature
with fiona.open(path_adm1, "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

print(shapes)

## NTL Data, Level
pathto_tier = "data/falchetta_tier/tierofaccess_SSA_2018.tiff"

## convert netcdf file into tiff file via command prompt:
## gdal_translate -of GTiff tiersofaccess_SSA_2018.nc tierofaccess_SSA_2018.tiff

## Clip SSA tiff to just country's tiff
with rasterio.open(pathto_tier) as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

## write image file to data
out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

## output path
pathto_clip = 'data/outputs/_2/tierofaccess_' + country_code + '_2018.tif'
with rasterio.open(pathto_clip, "w", **out_meta) as dest:
    dest.write(out_image)

## read in image array of falchetta_tiff file
with rasterio.open(pathto_clip) as src:
    tier_array = src.read()

print(tier_array.shape)
non_val = np.unique(tier_array)[0]

## read in geodataframe of households
pathto_hhld = 'data/outputs/_1/' + country_code + '_hhlds.shp'
hhld_gdf = gpd.read_file(pathto_hhld)
total_households = len(hhld_gdf)

# Read points from shapefile
hhld_gdf.index = range(len(hhld_gdf))
coords = [(x,y) for x, y in zip(hhld_gdf['geometry'].x, hhld_gdf['geometry'].y)]

# open raster file
src = rasterio.open(pathto_clip)

#Sample the raster at every point location and store values in DataFrame
hhld_gdf['Raster Value'] = [x[0] for x in src.sample(coords)]

# Remove points that are sorted an area outside of Rwanda
raster_vals_dist = np.array(hhld_gdf['Raster Value'])
idx_todrop = np.where(raster_vals_dist == non_val)
hhld_gdf = hhld_gdf.drop(idx_todrop[0])

# For grid connected customers, we'll assume that they have at least above a tier 0
# Drop tier 0

noelec_hhld = np.where(raster_vals_dist == 0.0)
hhld_gdf = hhld_gdf.drop(noelec_hhld[0])

## get distribution per pixel value
distribution = {}
for response in hhld_gdf['Raster Value']:
    distribution[response] = distribution.setdefault(response, 0) + 1

##SANITY CHECK
## Check Electrification Rate
electrified_hhlds = len(hhld_gdf)
electrification_rate = electrified_hhlds / total_households
print("Electrification Rate Estimated: ", electrification_rate, "/n", "Reported Electrification Rate: 30%")

## Export shape file
pathto_shp = 'data/outputs/_2/' + country_code + '_elec-hhlds.shp'
hhld_gdf.to_file(driver='ESRI Shapefile', filename=pathto_shp)

