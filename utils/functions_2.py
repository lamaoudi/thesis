## import libraries


def get_raster_file(raster_file):
    """
    Function: Given a raster file, the function will output the pixel size, pixel location, and the pixel value

    Parameters:
        raster_file : string - path to raster file

    Returns
    -------
    x_size : float
        Pixel size
    top_left_x_coords : numpy.ndarray  shape: (number of columns,)
        Longitude of the top-left point in each pixel
    top_left_y_coords : numpy.ndarray  shape: (number of rows,)
        Latitude of the top-left point in each pixel
    centroid_x_coords : numpy.ndarray  shape: (number of columns,)
        Longitude of the centroid in each pixel
    centroid_y_coords : numpy.ndarray  shape: (number of rows,)
        Latitude of the centroid in each pixel
    bands_data : numpy.ndarray  shape: (number of rows, number of columns, 1)
        Pixel value

    """

    raster_dataset = gdal.Open(raster_file, gdal.GA_ReadOnly)

    # get project coordination
    proj = raster_dataset.GetProjectionRef()

    bands_data = []
    # Loop through all raster bands
    for b in range(1, raster_dataset.RasterCount + 1):
        band = raster_dataset.GetRasterBand(b)
        bands_data.append(band.ReadAsArray())
        no_data_value = band.GetNoDataValue()
    bands_data = np.dstack(bands_data)
    rows, cols, n_bands = bands_data.shape

    # Get the metadata of the raster
    geo_transform = raster_dataset.GetGeoTransform()
    (upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = geo_transform

    # Get location of each pixel
    x_size = 1.0 / int(round(1 / float(x_size)))
    y_size = - x_size
    y_index = np.arange(bands_data.shape[0])
    x_index = np.arange(bands_data.shape[1])
    top_left_x_coords = upper_left_x + x_index * x_size
    top_left_y_coords = upper_left_y + y_index * y_size

    # Add half of the cell size to get the centroid of the cell
    centroid_x_coords = top_left_x_coords + (x_size / 2)
    centroid_y_coords = top_left_y_coords + (y_size / 2)

    return (x_index, y_index, x_size, top_left_x_coords, top_left_y_coords, centroid_x_coords, centroid_y_coords, bands_data, y_size)

def normal_it(array):
    """
       Function: Given a raster file, the function will output the pixel size, pixel location, adn the pixel value

       Parameters:
           raster_file : string - path to raster file

       Returns
       -------
       x_size : float
           Pixel size
       top_left_x_coords :

       """

    min_val = np.min(array)
    max_val = np.max(array)
    row = len(array)
    col = len(array[0])
    normal_array = np.zeros([row, col])
    for i in range(row):
        for j in range(col):
            normal_array[i, j] = (array[i, j] - min_val)/(max_val - min_val)
    return normal_array