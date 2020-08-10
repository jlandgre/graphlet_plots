#Version 8/7/20

import pandas as pd
import os

#Import JDL utility modules
import sys
sys.path.append(sys.path[0])
import colinfo

def SubsetToFilter(df, fil):
    return df[fil]

#Add a row order column to fingerprint rows (move this to tbltools library)
def AddRowOrderCol(df, col_name):
    df.reset_index(inplace=True,drop=True)
    df.index.name = col_name
    df.reset_index(drop=False, inplace=True)
    return df

def ImportDataFrame(tbl_cls, file):
    """
    Import a DataFrame from csv. Rename columns to ColInfo Names. Filter to keepcols
    JDL 7/21/20
    """
    df = pd.read_csv(file)
    ColInfo = colinfo.ReadColInfoFromFile('libs/colinfo.csv')
    colinfo.CI_RenameColsFromImport(ColInfo, df)
    if len(tbl_cls.keepcols) > 0: df = df[tbl_cls.keepcols]
    return df

def TopItemCtAndDesc(df, lst_by):
    """
    Group a Dataframe by a list of "by" columns and return top item's lst_by value(s) and count

    Returns:
    desc:   lst_by value(s) for top-ranked row.  data type will be value or tuple depending
            on whether lst_by is single item or multi-item list
    ct:     count of top-ranked row in groupby

    JDL 7/27/20
    """
    ser = df.groupby(lst_by).size()
    ser.sort_values(ascending=False, inplace=True)
    if ser.index.size > 0:
        return ser.index.values[0], ser[0]
    else:
        return 'None', 0

def MapSerToAltVals(ser_data, lst_data_keys, lst_data_vals):
    """Map a list of values to an alternate list for plotting

    Useful for "rescaling" or mapping text categories to numerical values for plotting

    Args:
    ser_data (Pandas Series) - data series with values for remapping
    lst_data_keys (list) - list of keys (current series values) for mapping
    lst_data_vals (list) - list of values to map to

    Raises:
    No error trapping currently

    Returns:
    Pandas series with keys remapped to values

    """

    ser_mapped = ser_data.copy()
    di = dict(zip(lst_data_keys, lst_data_vals))
    return ser_mapped.replace(di)

def RescaleSerValues(ser_data, tup_lims_data, tup_lims_rescaled):
    """
    Rescale numeric data

    Useful for "rescaling" data for plotting.  Example:
    tup_lims_data = (0, 100)
    tup_lims_rescaled = (-10, 0)
    Series will be rescaled such that 0 --> -10 and 100 --> 0

    Args:
    ser_data (Pandas Series) - data series with numeric values for remapping
    tup_lims_data (tuple; numeric values)
    tup_lims_data (tuple; numeric values)

    Raises:
    No error trapping currently

    Returns:
    Pandas series with rescaled values
    """
    ser_plot = ser_data.copy()

    x1_new = tup_lims_rescaled[1]
    x0_new = tup_lims_rescaled[0]
    x1_prev = tup_lims_data[1]
    x0_prev = tup_lims_data[0]
    return (ser_data - x0_prev)*((x1_new - x0_new)/(x1_prev - x0_prev)) + x0_new

def RescaleValue(val, tup_lims_data, tup_lims_rescaled):
    """
    Rescale numeric data value

    Useful for "rescaling" data for plotting.  Example:
    tup_lims_data = (0, 100)
    tup_lims_rescaled = (-10, 0)
    value will be rescaled such that 0 --> -10 and 100 --> 0

    Args:
    val (Float) - value to be rescaled
    tup_lims_data (tuple; numeric values)
    tup_lims_data (tuple; numeric values)

    Raises:
    No error trapping currently

    Returns:
    rescaled value
    """

    x1_new = tup_lims_rescaled[1]
    x0_new = tup_lims_rescaled[0]
    x1_prev = tup_lims_data[1]
    x0_prev = tup_lims_data[0]
    return (val - x0_prev)*((x1_new - x0_new)/(x1_prev - x0_prev)) + x0_new

def SeriesFromDFCols(df, valcol, indexcol, dtype=None):
    """
    Convert two DataFrame columns into a Series as index and values; drop nulls from valcol

    args:
    df (Pandas DataFrame) - DataFrame containing valcol and indexcol
    valcol (String) - name of DataFrame column to return as Series values (and name of Series)
    indexcol (String) - name of DataFrame column to return as Series index
    dtype (Python dtype - typically int) - optional returned dtype of Series

    JDL 8/6/20
    """
    ser = pd.Series(df[valcol].values, index=df[indexcol]).dropna()
    ser.name = valcol
    if not dtype is None: ser = ser.astype(dtype)
    return ser
