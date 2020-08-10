#Version 8/7/20
# 8/7/20 Added PrintClass function

import math
import os
import glob
import shutil
import pandas as pd
import numpy as np

def IsNullVal(val):

    """Return TRUE if val is null (nan)"""

    if isinstance(val,float) and math.isnan(val): return True
    return False

#Set the environment for code - can convert to return a class
def OSDefaults():

    """Set OS-specific values"""

    IsWindows, IsMacOS = False, False
    if os.name == 'nt':
        IsWindows = True
        sep = '\\'
    elif os.name == 'posix':
        IsMacOS = True
        sep = '/'
    return sep

#Returns the filename portion of a directory path
def FileNameFromPath(pathplusfile, sep):

    """Return the filename string from a directory path"""

    return pathplusfile.split(sep)[-1]

def ResetInitialAndFinalFolders(sPath_i, sPath_f, IsRemove, sFileType):

    """Reset files in an initial/final sub-folder structure by either moving files back to initial
       from final or, optionally, deleting all files from both subfolders

    Args:
        path_i (String): directory path of 'initial' sub-folder including final path separator
        path_f (String): directory path of 'final' sub-folder  including final path separator
        IsRemove (Boolean): toggle to either (TRUE) delete all files or (FALSE) move files in final
                            sub-folder to initial without any deletions
        sFileType (String): file specifier such as '*.csv' or '*.*' recognizable to glob.glob()

    Returns:
        i, j, k (Integers): numbers of files relocated, removed from initial and removed from
                            final subfolders, respectively
    """

    i, j, k = 0, 0, 0
    for f in glob.glob(sPath_f + sFileType):
        if not IsRemove:
            shutil.move(f, sPath_i)
            i += 1
        else:
            os.remove(f)
            j += 1
    if IsRemove:
        for f in glob.glob(sPath_i + sFileType):
            os.remove(f)
            k += 1
    return i, j, k


def FractionalDays(tdelta):
    sec_day = 86400
    return round(tdelta.total_seconds()/sec_day,1)

def DatetimeDurationMin(dt_end, dt_begin):
    return round((dt_end - dt_begin).total_seconds()/60,1)

def DatetimeDurationHrs(dt_end, dt_begin):
    return round((dt_end - dt_begin).total_seconds()/3600,1)

def PrintClass(cls):
    """Print all attribute values for a class instance"""
    for var in vars(cls).items():
        if isinstance(var[1], pd.DataFrame) | isinstance(var[1], pd.Series):
            print('\n',var[0], '\n', var[1], '\n\n')
        else:
            print(var[0], ': ', var[1])
