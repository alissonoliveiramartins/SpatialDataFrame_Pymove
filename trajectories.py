from __future__ import division

import folium
import numpy as np
import pandas as pd

from pymove.utils.constants import DATETIME, LATITUDE, LONGITUDE, TRAJ_ID


def read_csv(
    filename,
    sep=",",
    encoding="utf-8",
    header="infer",
    names=None,
    latitude=LATITUDE,
    longitude=LONGITUDE,
    datetime=DATETIME,
    traj_id=TRAJ_ID,
    type_="pandas",
    n_partitions=1,
):
    """
    Reads a .csv file and structures the data into the desired structure
    supported by PyMove.

    Parameters

    ----------
    filename : String.
        Represents coordinates lat, lon which will be the center of the map.

    sep : String, optional, default ','.
        Delimiter to use.

    encoding : String, optional, default 'utf-8'.
        Encoding to use for UTF when reading/writing

    header: int, list of int, default ‘infer’
        Row number(s) to use as the column names, and the start of the data.
        Default behavior is to infer the column names: if no names are passed the
        behavior is identical to header=0 and column names are inferred from the
        first line of the file, if column names are passed explicitly then the behavior
        is identical to header=None

    names: array-like, optional
        List of column names to use. If the file contains a header row,
        then you should explicitly pass header=0 to override the column names.
        Duplicates in this list are not allowed.

    latitude : String, optional, default 'lat'.
        Represents the column name of feature latitude.

    longitude : String, optional, default 'lon'.
        Represents the column name of feature longitude.

    datetime : String, optional, default 'datetime'.
        Represents the column name of feature datetime.

    traj_id : String, optional, default 'id'.
        Represents the column name of feature id trajectory.

    type_ : String, optional, default 'pandas'.
        Represents the type_ of                    \

    n_partitions : int, optional, default 1.
        Represents .

    Returns
    -------
    pymove.core.MoveDataFrameAbstract subclass.
        Trajectory data.
    """
    df = pd.read_csv(
        filename,
        sep=sep,
        encoding=encoding,
        header=header,
        names=names,
        parse_dates=[datetime],
    )

    from pymove import PandasMoveDataFrame as pm
    from pymove import DaskMoveDataFrame as dm

    if type_ == "pandas":
        return pm(df, latitude, longitude, datetime, traj_id)
    if type_ == "dask":
        return dm(df, latitude, longitude, datetime, traj_id, n_partitions)


def format_labels(current_id, current_lat, current_lon, current_datetime):
    """
    Format the labels for the PyMove lib pattern labels output = lat, lon and datatime.

    Parameters
    ----------
    current_id : String.
        Represents the column name of feature id.

    current_lat : String.
        Represents the column name of feature latitude.

    current_lon : String.
        Represents the column name of feature longitude.

    current_datetime : String.
         Represents the column name of feature datetime.

    Returns
    -------
    dic_labels : dict.
        Represents a dict with mapping current columns of data to format of PyMove column.

    """
    dic_labels = {}
    dic_labels[current_id] = TRAJ_ID
    dic_labels[current_lon] = LONGITUDE
    dic_labels[current_lat] = LATITUDE
    dic_labels[current_datetime] = DATETIME
    return dic_labels

def format_labelsSpatial(current_lat, current_lon):
    """
    Format the labels for the PyMove lib pattern labels output = lat, lon and datatime.

    Parameters
    ----------
    current_id : String.
        Represents the column name of feature id.

    current_lat : String.
        Represents the column name of feature latitude.

    current_lon : String.
        Represents the column name of feature longitude.

    current_datetime : String.
         Represents the column name of feature datetime.

    Returns
    -------
    dic_labels : dict.
        Represents a dict with mapping current columns of data to format of PyMove column.

    """
    dic_labels = {}
    dic_labels[current_lon] = LONGITUDE
    dic_labels[current_lat] = LATITUDE
    return dic_labels


def shift(arr, num, fill_value=np.nan):
    """
    Shifts the elements of the given array by the number of periods specified.

    Parameters
    ----------
    arr : array.
        The array to be shifed.

    num : int.
        Number of periods to shift. Can be positive or negative. If posite, the elements will be pulled down, and pulled
        up otherwise.

    fill_value : int, optional, default np.nan.
        The scalar value used for newly introduced missing values.

    Returns
    -------
    result : array.
        A new array with the same shape and type_ as the initial given array, but with the indexes shifted.

    Notes
    -----
        Similar to pandas shift, but faster.

    References
    --------
        https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
    """

    result = np.empty_like(arr)

    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result = arr
    return result


def fill_list_with_new_values(original_list, new_list_values):
    """
    Copies elements from one list to another. The elements will be positioned in
    the same position in the new list as they were in their original list.

    Parameters
    ----------
    original_list : list.
        The list to which the elements will be copied.

    new_list_values : list.
        The list from which elements will be copied.

    Returns
    -------
    """
    n = len(new_list_values)
    original_list[:n] = new_list_values


def save_bbox(bbox_tuple, file, tiles="OpenStreetMap", color="red"):
    """
    Save bbox as file .html using Folium.

    Parameters
    ----------
    bbox_tuple : tuple.
        Represents a bound box, that is a tuple of 4 values with the min_ and max limits of latitude e longitude.

    file : String.
        Represents filename.

    tiles : String, optional, default 'OpenStreetMap'.
        Represents tyles's type_.
        Example: 'openstreetmap', 'cartodbpositron', 'stamentoner', 'stamenterrain', 'mapquestopen',
        'MapQuest Open Aerial', 'Mapbox Control Room' and 'Mapbox Bright'.

    color : String, optional, default 'red'.
        Represents color of lines on map.

    Returns
    -------


    Examples
    --------
    >>> from pymove.trajectories import save_bbox
    >>> bbox = (22.147577, 113.54884299999999, 41.132062, 121.156224)
    >>> save_bbox(bbox, 'bbox.html')
    """
    m = folium.Map(tiles=tiles)
    m.fit_bounds(
        [[bbox_tuple[0], bbox_tuple[1]], [bbox_tuple[2], bbox_tuple[3]]]
    )
    points_ = [
        (bbox_tuple[0], bbox_tuple[1]),
        (bbox_tuple[0], bbox_tuple[3]),
        (bbox_tuple[2], bbox_tuple[3]),
        (bbox_tuple[2], bbox_tuple[1]),
        (bbox_tuple[0], bbox_tuple[1]),
    ]
    folium.PolyLine(points_, weight=3, color=color).add_to(m)
    m.save(file)
