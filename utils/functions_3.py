import numpy as np
from pyproj import Proj
import pandas as pd

from progressbar import ProgressBar
from progressbar import *

widgets = ['Test: ', Percentage(), ' ', Bar(marker='0', left='[', right=']'),
           ' ', ETA(), ' ', FileTransferSpeed()]  # see docs for other options

pbar = ProgressBar(widgets=widgets)


def sample_power(hhld_gdf, tier_breakdown, c_factor):
    for idx, row in hhld_gdf.iterrows():
        i = hhld_gdf['Raster Val'][idx]
        index = np.where(tier_breakdown.Tier == i)
        index = index[0][0]
        mean = tier_breakdown['Mean Power'][index]
        strd_dev = tier_breakdown['stdrd_error'][index]
        p_ = np.random.normal(mean, strd_dev)
        p = p_/1000

        if p < 0:
            p = p * -1
            hhld_gdf.loc[idx, 'power'] = p
            #print(hhld_gdf.power[idx])
        if p == 0:
            p = 0.35
            hhld_gdf.loc[idx, 'power'] = p
            #print(hhld_gdf.power[idx])
        else:
            hhld_gdf.loc[idx, 'power'] = p
            #print(hhld_gdf.power[idx])

        print(idx, " of ", len(hhld_gdf))

    hhld_gdf['power coincident'] = hhl2_gdf['power'] * c_factor

    return hhld_gdf


def reproject_rnm(hhld_gdf, projcrs, idxval):
    p = Proj(projcrs)

    pbar = ProgressBar(widgets=widgets)

    x_coord = []
    y_coord = []
    for pval in pbar(idxval):
        px, py = hhld_gdf.geometry[pval].x, hhld_gdf.geometry[pval].y
        x, y = p(px, py)
        x_coord.append(x / 1000)
        y_coord.append(y / 1000)

    len_df = len(hhld_gdf)
    return len_df, x_coord, y_coord


def convert_to_rnm(hhld_gdf, len_df, x_coord, y_coord):
    z_coord = np.zeros([len_df, 1])  # z-coordinate, 0.0

    z_coord = []
    for i in range(len_df):
        z_coord.append(0.0)

    Dn = []  # In settlement
    for i in range(len_df):
        Dn.append('S')

    zF = []
    for i in range(len_df):
        zF.append('A')

    Mun = []
    for i in range(len_df):
        Mun.append(1000)

    ID = hhld_gdf.HHLD_NUM

    Prop = []
    for i in range(len_df):
        Prop.append('c')

    Con = []
    for i in range(len_df):
        Con.append('A')

    LV = []
    for i in range(len_df):
        LV.append(0.4)

    Cens_max = []
    for i in range(len_df):
        Cens_max.append(1.0)

    Cens_mid = []
    for i in range(len_df):
        Cens_mid.append(1.0)

    Cens_min = []
    for i in range(len_df):
        Cens_min.append(1.0)

    Nuc = []
    for i in range(len_df):
        Nuc.append(0.0)

    P = hhld_gdf['power coincident']
    p_factor = 0.98
    multiplier = 0.02 / 0.98
    Q = P * multiplier

    lvc = pd.DataFrame(
        {'x-coordinate': x_coord, 'y-coordinate': y_coord, 'z-coordinate': z_coord, 'Dn': Dn, 'zF': zF, 'Mun': Mun,
         'ID': ID, 'Prop': Prop, 'Con': Con,
         'V': LV,
         'max': Cens_max,
         'mid': Cens_mid,
         'min': Cens_min,
         'P': P,
         'Q': Q,
         'Nuc': Nuc})

    return lvc