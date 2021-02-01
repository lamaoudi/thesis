import geopandas as gpd
import pandas as pd
import numpy as np

from utils import functions_3 as f3

#TODO: Aytomate Multi-Franework creation

# Upload Multi_Tier Framework
country_code = 'RWA'
pathto_framework = 'data/worldbank_multi-tier/' + country_code + '.csv'
tier_breakdown = pd.read_csv(pathto_framework)
print(tier_breakdown)

## Assume Normal Distribution between max/min
## parameters = (mean, stdv)
## parameters estiamte using 95% interval (min = mean - 1.96 * s_n)
mean_power = np.array(tier_breakdown['Mean Power'])
min_power_capacity = np.array(tier_breakdown['Min Power Capacity'])
stdrd_error = (mean_power - min_power_capacity) * 1/1.96
tier_breakdown['stdrd_error'] = stdrd_error

## Read in Electrified Household Shapefile
pathto_hhlds = 'data/outputs/_2/' + country_code + '_tier-hhlds.shp'
hhld_elec = gpd.read_file(pathto_hhlds)
hhld_elec['power'] = ''
hhld_elec.head()

COINCIDENT_FACTOR = 0.4
hhld_elec = f3.sample_power(hhld_elec, tier_breakdown, COINCIDENT_FACTOR)

projcrs = 'PROJCS["wgs84",GEOGCS["GCS_WGS_1984",DATUM["WGS_1984",SPHEROID["WGS_84",6378137.0,298.257223563]],' \
         'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],PROJECTION[' \
         '"Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",5000000.0],' \
         'PARAMETER["Central_Meridian",30.0],PARAMETER["Scale_Factor",0.9999],PARAMETER["Latitude_Of_Origin",0.0],' \
         'UNIT["Meter",1.0]] '

idx_val = list(hhld_elec.index)

len_df, x_coord, y_coord = f3.reproject_rnm(hhld_elec, projcrs, idx_val)

lvc_out = f3.convert_to_rnm(hhld_elec, len_df, x_coord, y_coord)

pathto_lvc = 'data/outputs/_3/' + country_code + '_lvc.csv'
lvc_out.to_csv(pathto_lvc, header = False, index = None, sep = '\t')


