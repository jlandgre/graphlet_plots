#Version 8/7/20
import pandas as pd
import numpy as np

#Import JDL utility modules
import sys
sys.path.append(sys.path[0])
import pd_util
import util

#graphlet_plot.py
class Graphlet():
    """
    Set attributes common to Categorical and Continuous plots. Parent of
    GraphletCategorical and GraphletContinuous

    Attributes:
    t_range [tuple - datetime format] - the datetime range of plot data
    ylims [tuple - either numeric or None] - (ymin, ymax) for the Graphlet
           in y-axis units.  Specify either ymin or ymax to anchor Graphlet
           location on y-axis of plot
    spacing [tuple - numeric] - (spacing between categories, buffer between
                                graphlets)
    data [tuple - Pandas Series] (x-data, unscaled/unmapped y-data)
    IsHLine [boolean] toggles horizontal line below the graphlet on the plot
    heading - [string] - optional heading to label graphlet at its top left
    dot_format [tuple - mixed types] - (string Matplotlib color, integer dot
                size, integer dot transparency)

    Version: 8/6/20 JDL Data Delve LLC
    """
    def __init__(self, t_range, spacing, ylims, data, IsHLine, heading=None, dot_format=None):
        self.xdata = data[0]
        self.ydata_unscaled = data[1]
        self.heading = ''
        if not heading is None: self.heading = heading
        if not dot_format[0] is None: self.dotcolor = dot_format[0]
        if not dot_format[1] is None: self.dotsize = dot_format[1]
        if not dot_format[2] is None: self.dot_transparency = dot_format[2]

        self.heading_coords = (t_range[0], (self.ymax + 1 * spacing[1])) #Label's x-y position
        self.hline = None
        self.ypos_hline = None
        if IsHLine: self.ypos_hline = self.ymin - spacing[1]

class GraphletCategorical():
    """
    Set attributes for categorical time-series plots. Map y-values to
    specified categories

    Child of Graphlet, which initializes common attributes between
    GraphletCategorical and GraphletContinuous

    Attributes:
    See Parent Class docstring for its attributes

    ticklabels - dictionary of categorical keys (in terms of unmapped y-data)
                  and values that are labels to use on the plot for data series
    Methods:
    CreateCombinedFlagColSeries
    CalculateYLimitsCategorical
    SeriesFromDFCols

    Version: 8/7/20 JDL Data Delve LLC
    """
    def __init__(self, t_range, spacing, ylims, data, IsHLine, ticklabels=None, heading=None, dot_format=None):

        #Generate y-limits, ticklist and labels for categorical plot
        lst_cats = list(set(data[1]))
        ncats = len(lst_cats)
        self.ymin, self.ymax = GraphletCategorical.CalculateYLimitsCategorical(ylims, ncats, spacing)

        Graphlet.__init__(self, t_range, spacing, ylims, data, IsHLine, heading, dot_format)

        self.ticklist, self.labels = [], []
        for i, cat in zip(range(0,ncats), lst_cats):
            self.ticklist.append(self.ymin+ (i * spacing[0]))
            if ticklabels is not None:
                self.labels.append(ticklabels[cat])
            else:
                self.labels.append(cat)

        #Generate y-data that maps categories to ticklist values
        self.ydata = pd_util.MapSerToAltVals(self.ydata_unscaled, lst_cats, self.ticklist)

    def CreateCombinedFlagColSeries(lst_flags):
        """
        Create Concatenated Series with mapped flag values and create dictionary of original
        flag column names or labels by value.

        Designed to work on columns that use 1/blank to flag time series discrete
        events. This function maps multiple such columns to alternate integers and
        concatenates the result into a single series.  The returned dictionary decodes
        how integers and original column names (or integers and user-specified labels)
        match up.

        Args:
        lst_flags (list of 3-item or, optionally, 4-item tuples) describing one or more
                    series to be concatenated:
                    df name - name of Pandas DataFrame containing valuecol and indexcol
                    valuecol - column in df to serve as returned series values
                    indexcol - column in df to serve as returned series index
                    label string [optional] - Description for plot labeling

        Returns:
        Concatenated Series with original values mapped to integers
        Dictionary of integer (keys) to original column names (values)
        """

        lst_flag_series, ticklabels = [], {}
        for flag, i in zip(lst_flags, range(0,len(lst_flags))):

            #Default to None label then check whether it's specified
            label = None
            if len(flag) == 3: (df, valuecol, indexcol) = flag
            if len(flag) == 4: (df, valuecol, indexcol, label) = flag

            #Create a series from flag and append it to list of such series
            ser = pd_util.SeriesFromDFCols(df, valuecol, indexcol, 'int64')
            ser = pd_util.MapSerToAltVals(ser, [1], [i+1])
            lst_flag_series.append(ser)

            #Add a label to dict --either column name or user-specified string
            ticklabels[i+1] = ser.name
            if not label is None: ticklabels[i+1] = label
        return pd.concat(lst_flag_series), ticklabels

    def CalculateYLimitsCategorical(ylims, ncats, spacing):
        """
        Populate y-limits for Categorical plots from either upper or lower limit

        Args:
        ylims [tuple; number] - (lower, upper) y-limits; one may be None
        ncats [integer] - number of categories
        spacing [tuple; number] - (spacing between categories, spacing between graphlets) in y-axis limits

        Returns:
        individual ymin and ymax (calculation overrides specified values if ylims input has both specified)
        """
        if ylims[0] is not None:
            ymin = ylims[0]
            ymax = ymin + (ncats - 1) * spacing[0]
        elif ylims[1] is not None:
            ymax = ylims[1]
            ymin = ymax - (ncats - 1) * spacing[0]
        else:
            return None, None
        return ymin, ymax

    def SeriesFromDFCols(df, valcol, indexcol, dtype=None):
        """
        Convert two DataFrame columns into a Series as index and values

        args:
        df (Pandas DataFrame) - DataFrame containing valcol and indexcol
        valcol (String) - name of DataFrame column to return as Series values (and name of Series)
        indexcol (String) - name of DataFrame column to return as Series index
        dtype (Python dtype - typically int) - optional returned dtype of Series
        """
        ser = pd.Series(df[valcol].values, index=df[indexcol]).dropna()
        ser.name = valcol
        if not dtype is None: ser = ser.astype(dtype)
        return ser

class GraphletContinuous():
    """
    Set attributes for continuous variable graphlet
    Optionally, rescale y-values for graphing

    Child of Graphlet, which initializes common attributes between
    GraphletCategorical and GraphletContinuous

    Attributes:
    See Parent Class docstring for its attributes

    ticklabels - Optional dictionary of values (unscaled y units) as keys
                      string labels as values
    scale_orig - [tuple - numeric]: Upper and lower values in unscaled y-units
                 for linear rescaling to plot y-axis units)
    scale_scaled [tuple - numeric]: Upper and lower values in scaled y-units;
                 used with scale_orig for linear rescaling of y-data

    Methods: None

    Version: 8/6/20 JDL Data Delve LLC
    """
    def __init__(self, t_range, spacing, ylims, data, IsHLine, ticklabels=None, heading=None, scale_orig=None, scale_scaled=None, dot_format=None):

        self.ymin = ylims[0]
        self.ymax = ylims[1]
        Graphlet.__init__(self, t_range, spacing, ylims, data, IsHLine, heading, dot_format)

        IsScaled = False
        if (scale_orig is not None) and (scale_scaled is not None): IsScaled=True

        #If specified, scale the y-values and the ticklist values
        self.ydata = self.ydata_unscaled
        if IsScaled:
            self.ydata = pd_util.RescaleSerValues(self.ydata_unscaled, scale_orig, scale_scaled)

        #Build ticklist and tick label list
        if not ticklabels is None:
            self.ticklist, self.labels = [], []
            for k, v in ticklabels.items():

                #Scale the tick value if needed
                k_scaled = k
                if IsScaled: k_scaled = pd_util.RescaleValue(k, scale_orig, scale_scaled)

                #Add tick and label to lists; If no specified label, tick value is the label
                self.ticklist.append(k_scaled)
                if v is not None:
                    self.labels.append(v)
                else:
                    self.labels.append(k_scaled)
