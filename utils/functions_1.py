# name all libraries

import numpy as np
import pandas as pd
from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon
import geopandas as gpd
import math


def open_adm3(filepath):
    """
    Function: Given a shape file, the function will output the geopandas dataframe
    Parameters:
        raster_file : string - path to shape file

    Returns
    -------
    adm3_df : geo-dataframe shape: (xxx)
        xxx
    """

    adm3_df = gpd.read_file(filepath)
    return adm3_df


def open_pop(pop_filepath, adm_df):
    """
    Function: Given the population csv and geodataframe the function will output the population dataframe
                and number of unique densities equivalent to adm-3 sectors
    Parameters:
        pop_filepath : string - path to shape file
        adm_df : geodata frame for country

    Returns
    -------
    new_df: pandas.df shape: (xxx)
        pixels with the respective population density in region
    tot_sectors: integer shape: (1,)
        total number of sectors
    density_val: numpy.array shape: (xxx)
        array of unique population density values

    """
    data = pd.read_csv(pop_filepath)
    data_arr = np.nan_to_num(data)

    ## Extract unique values
    density_val = np.unique(data_arr[:, 2])
    density_val = np.transpose(density_val)
    tot_sectors = len(density_val) + 1

    print("Number of Unique Densities:", tot_sectors)
    print("Number of Sectors:", len(adm_df))

    return data, tot_sectors, density_val, data_arr


def pop_density2gadm(pop_dataframe, gadm3_dataframe, unique_array):
    """
    Function: assigns population densities to each sector
    Parameters:
        pop_dataframe: string - path to shape file
        adm_df: geodata frame for country, admin-level 3
        unique_array: array of unique population density values

    Returns
    -------
    gadm3_dataframe: geopandas.dataframe shape: (xx)
        geodataframe of county info and its relative populaiton density

    """

    gadm3_dataframe["Population_Density"] = ""
    for idx in range(len(unique_array)):
        index = np.where(pop_dataframe.Population == unique_array[idx])
        a = index[0][0]
        p1 = Point(pop_dataframe.Lon[a], pop_dataframe.Lat[a])
        for dist in range(len(gadm3_dataframe.NAME_3)):
            if p1.within(gadm3_dataframe.geometry[dist]):
                #print(gadm3_dataframe.NAME_3[dist])
                gadm3_dataframe.loc[dist, 'Population_Density'] = unique_array[idx]

    return gadm3_dataframe


def density2cust(densityarray_1, Size_Of_Cell, Avg_Hhld_Size):
    """
    Function: Function round up the number of each grid then divides by the average household size
        to estimate the number of buildings in the 30 by 30 m area. If value >1 then
        coordinates are assigned a random coordinate inside the pixel
        by randomly perturbing the centroid coordinates (within the bounding box of the pixel).

    Parameters:
        xxx

    Returns
    -------
        xxx

    """

    ## Create a range for each coordinate : (x-Size_of_Cell/2, x+Size_Of_Cell/2) & for y
    densityarray = densityarray_1
    for i in range(0, len(densityarray_1)):
        w = math.ceil(densityarray_1[i, 2])
        k = w / Avg_Hhld_Size
        densityarray[i, 2] = round(k)

    # redistributing homes into individual coordinates
    x_new = []
    y_new = []
    hhld_num = []

    for x in range(len(densityarray)):
        if (densityarray[x, 2] > 1):
            num_of_house = int(densityarray[x, 2])
            x_coord_centroid = densityarray[x, 1]
            x_coord_min = x_coord_centroid - Size_Of_Cell / 2
            x_coord_max = x_coord_centroid + Size_Of_Cell / 2
            x_vals = np.linspace(x_coord_min, x_coord_max, num_of_house)

            y_coord_centroid = densityarray[x, 0]
            y_coord_min = y_coord_centroid - Size_Of_Cell / 2
            y_coord_max = y_coord_centroid + Size_Of_Cell / 2
            y_vals = np.linspace(y_coord_min, y_coord_max, num_of_house)

            for index in range(0, num_of_house):
                x_new.append(x_vals[index])
                y_new.append(y_vals[index])
                hhld_num.append(1.0)
        else:
            x_new.append(densityarray[x, 1])
            y_new.append(densityarray[x, 0])
            hhld_num.append(densityarray[x, 2])

    # Save output into a new rwa_hhld array
    densityarray_adj = np.zeros([int(sum(hhld_num)), 3])
    densityarray_adj[:, 0] = y_new
    densityarray_adj[:, 1] = x_new
    densityarray_adj[:, 2] = hhld_num

    return densityarray, densityarray_adj, hhld_num
