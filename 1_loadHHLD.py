## Import Libraries

import numpy as np
import pandas as pd
import geopandas as gpd

# TODO: Allow user to input country code into function and extract information accordingly (dictionary)

### Administrative Data
## GADM DATA, Level 3
import utils.functions_1 as f1

pathto_gadm = "data/gadm36_"
country_code = 'RWA'
path_adm3 = pathto_gadm + country_code + '_shp/gadm36_' + country_code + '_3.shp'

adm3_df = f1.open_adm3(path_adm3)
crs_gadm = adm3_df.crs

#TODO: extract crs

# Import Facebook Population Data
# Data Info: 30-m resolution, non-zero where there is a building
# Pixel is assigned the population density in the respective province (GADM level-3 boundary).
pathto_fbdata = 'data/fb_pop/population_'
path_pop = pathto_fbdata + country_code + '/population_' + country_code + '.csv'

## VISUALIZATION: Density by Admin-lev-3
pop_df, tot_sector, density_val, pop_arr = f1.open_pop(path_pop,
                                                       adm3_df)  # pop_df = df population density values by "building"

## Convert df into geodataframe
#TODO: Include CRS
pop_gdf = gpd.GeoDataFrame(pop_df, geometry=gpd.points_from_xy(pop_df.Lon, pop_df.Lat), crs=crs_gadm)

## Plot distribution of pop_density across country by sector
density_bysector = f1.pop_density2gadm(pop_df, adm3_df, density_val)
density_bysector['Population_Density'].replace('', 0, inplace=True)
ax = density_bysector.plot(column='Population_Density', cmap='terrain', legend=True)

## Get Household Locations (LV Load)
# hhld_num provides the number of houses in a given grid cell.
# TODO: Create a dictionary of avg_hhld size by country code

Avg_Hhld_Size = 4.3
Size_Of_Cell = 0.0002777

hhlds, hhld_adj, hhld_num = f1.density2cust(pop_arr, Size_Of_Cell, Avg_Hhld_Size)

print("Sum of New HHLD List: ", sum(hhld_num))
print("Sum of Original HHLD: ", sum(hhlds[:, 2]))
sanity_check = sum(hhld_num) == sum(hhlds[:, 2])
print(sanity_check)

# Convert array of households into geopandas df
hhld_df = pd.DataFrame({'HHLD_NUM': hhld_adj[:, 2], 'Longitude': hhld_adj[:, 1], 'Latitude': hhld_adj[:, 0]})
hhld_gdf = gpd.GeoDataFrame(hhld_df, geometry=gpd.points_from_xy(hhld_df.Longitude, hhld_df.Latitude), crs=crs_gadm)

#Save geodataframe as shape file
pathto_shp = 'data/outputs/_1/' + country_code + '_hhlds.shp'
hhld_gdf.to_file(driver='ESRI Shapefile', filename=pathto_shp)
#hhld_gdf.plot(ax=ax)

np.savetxt('data/outputs/_1/' + country_code + '_hhlds.csv', hhld_adj, delimiter=",")  # export to csv file
