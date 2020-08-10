import pandas as pd
import math

#Global Variables
NameCI = 'name'
DescCI = 'description'
UnitsCI = 'units'
XLFormatCI = 'xlformat'
XLWidthCI = 'xlwidth'
dfNameCI = 'df_name'
Name_iCI = 'name_import'
Name_fCI = 'name_export'
Col_orderCI = 'col_order'

#ReadColInfo - reads the col_info DataFrame to a nested dictionary
#Column 1 of the col_info.csv contains column headings used as key for the other column info items (For example
#data column 'Revenue' has Description, XLFormat and XLWidth equal to 'Annual Revenue', '$0.00' and '11',
#respectively)
def ReadColInfoFromFile(PathCIFile):
    """Read column info into ColInfo dictionary/sub-dictionaries
        Each sub-dictionary is a metadata attribute about the variables such as units, description etc.

        Sub-dictionary names:
        NameCI = 'name'
        DescCI = 'description'
        UnitsCI = 'units'
        XLFormatCI = 'xlformat'
        XLWidthCI = 'xlwidth'
        dfNameCI = 'df_name'
        Name_iCI = 'name_import'
        Name_fCI = 'name_export'
        Col_orderCI = 'col_order'

    Args:
        PathCIFile (String): directory path + filename for the column info *.csv file

    Returns:
        ColInfo (Dict): Dictionary/Sub-dictionaries with column info
    """

    #Read the file, and Create the nested dictionary empty strucure
    df_CI = pd.read_csv(PathCIFile, index_col=NameCI)
    ColInfo = {DescCI: {}, UnitsCI: {}, XLFormatCI: {}, XLWidthCI: {},
                Name_iCI: {}, Name_fCI: {}, Col_orderCI: {}}

    #Read each col_info DataFrame row and translate to dictionary values
    for var_name, row in df_CI.iterrows():
        for dictCI in ColInfo:
            ColInfo[dictCI][var_name] = row[dictCI]
    return ColInfo

#RefreshColInfoToFile - refreshes col_info.csv based on dictionary contents; adds file rows as needed
def RefreshColInfoToFile(PathCIFile, ColInfo):

    #Read the col_info file to be updated
    df_CI = pd.read_csv(PathCIFile, index_col=NameCI)

    #Iterate over dictionaries in ColInfo and over variables (keys); update/append to df_CI
    for CI_dict in ColInfo:
        for var in CI_dict:
            df_CI.loc[var,CI_dict] = ColInfo[CI_dict][var]
    df_CI.to_csv(PathCIFile)
    return

#BuildXLWriterLists - Uses number format and column width ColInfo to build needed XLWriter lists
def BuildXLWriterLists(df, ColInfo):

    #Initialize lists with placeholder for index - Works for single index
    lst_fmts = ['0']
    lst_widths = [10]

    #Populate format and width for index; xxx Need to address case of multiindex
    if df.index.names[0] is None:
        df.index.name = 'index'
    elif df.index.name in ColInfo:
        lst_fmts = [ColInfo[XLFormatCI][df.index.name]]
        lst_widths = [ColInfo[XLWidthCI][df.index.name]]

    #Iterate through df columns and add number format and column width to the lists
    for col in df.columns:
        if col in ColInfo[XLFormatCI] and col in ColInfo[XLWidthCI]:
            lst_fmts.append(ColInfo[XLFormatCI][col])
            lst_widths.append(ColInfo[XLWidthCI][col])
        else:
            lst_fmts.append('0')
            lst_widths.append(10)

    #Get rid of quotation marks that prevent formats from working with ExcelWriter
    lst_fmts = ListReplaceNaN(lst_fmts,'')
    lst_fmts = [s.replace('"', '') for s in lst_fmts]
    lst_widths = ListReplaceNaN(lst_widths,0)
    return lst_fmts, lst_widths

#Toggles val to blank string if val is nan values
def SetVal(val):
    retval = val
    if isinstance(val , float) and np.isnan(val): retval = ''
    return str(retval)

def CreateExcelStepsDF(lst_dfs, lst_XLshts, ColInfo):

    #Add needed ColInfo entries for ExcelSteps worksheet
    ColInfo[XLFormatCI]['Formula/List Name/Sort-by'] = '@'
    ColInfo[XLFormatCI]['Number Format'] = '@'

    dictC = {1:'Sheet', 2:'Column',3:'Step',4:'Comment',5:'Number Format',6:'Width'}
    df_ExcelSteps = pd.DataFrame(columns=['Sheet', 'Column', 'Step', 'Formula/List Name/Sort-by',
                                          'After or End Column', 'Keep Formulas', 'Comment',
                                          'Number Format', 'Width'])
    for dframe, sht in zip(lst_dfs, lst_XLshts):
        lst_dfCols = list(dframe.index.names) + dframe.columns.tolist()

        #Iterate through columns and append ExcelSteps recipe rows
        for i, col in enumerate(lst_dfCols):
            if not col in ColInfo[DescCI]: continue
            comment = SetVal(ColInfo[DescCI][col])
            ucomment = SetVal(ColInfo[UnitsCI][col])
            if len(ucomment) > 0: comment = comment + ' in ' + ucomment

            row = {dictC[1]:sht, dictC[2]:col, dictC[3]:'Col_Format', dictC[4]:comment,
                   dictC[5]: ColInfo[XLFormatCI][col],dictC[6]: ColInfo[XLWidthCI][col]}

            df_ExcelSteps = df_ExcelSteps.append(row, ignore_index=True)

        #Add Tbl_FreezeRow1 to end of recipe
        df_ExcelSteps = df_ExcelSteps.append({dictC[1]:np.nan}, ignore_index=True)
        freeze = {dictC[1]:sht, dictC[3]:'Tbl_FreezeRow1'}
        df_ExcelSteps = df_ExcelSteps.append(freeze, ignore_index=True)

        #add blank row to create spacing in the recipe
        df_ExcelSteps = df_ExcelSteps.append({dictC[1]:np.nan}, ignore_index=True)

        #Name the ExcelSteps df's index
        df_ExcelSteps.index.name = 'row'

    lst_dfs.append(df_ExcelSteps)
    lst_XLshts.append('ExcelSteps')
    return lst_dfs, lst_XLshts, ColInfo

def WriteExcelWorkbook(lst_dfs, lst_shts, fName_xlsx, ColInfo, IsExcelSteps):
    lst_fmts = []
    lst_colwidths = []
    retval = fName_xlsx + ' Written Successfully'
    if len(lst_dfs) != len(lst_shts): return 'ERROR: Must be same number of dfs and shts'

    #Make local copy so ColInfo doesn't get modified
    Col_Info_l = ColInfo

    if IsExcelSteps:
        lst_dfs, lst_shts, Col_Info_l = CreateExcelStepsDF(lst_dfs, lst_shts, Col_Info_l)

    i=0
    for dframe, sht in zip(lst_dfs, lst_shts):
        XLWriterPrep(lst_dfs, lst_shts, lst_fmts, lst_colwidths, dframe, sht)
        lst_fmts[i], lst_colwidths[i] = BuildXLWriterLists(dframe, ColInfo)
        i = i+1

    #Text format for ExcelSteps Formula and Number Format columns
    if IsExcelSteps:
        i = len(lst_dfs) - 1
        lst_fmts[i][4], lst_fmts[i][8] = '@', '@'
    XLWriter(fName_xlsx, lst_dfs, lst_shts, lst_fmts, lst_colwidths)
    return retval

def ListReplaceNaN(lst, val_replace):
    for i, v in enumerate(lst):
        if v is np.nan: lst[i] = val_replace
    return lst

def CI_BuildMetadataList(ColInfo, lstCols, CI_MetadataDict, IsFillColName):
    """Build a matching Column Info metadata list from a list of Column Info variables (suitable for zip
        iteration over the two lists)

    Args:
        ColInfo (Dict): Column Info dictionary of metadata property dictionaries (Units, Import Names etc.)
        lstCols (String List): list of Column Info variable names
        CI_MetadataDict (String Dict name): Column Info metadata sub-dictionary name
        IsFillColName (Boolean): TRUE toggles substituting lstCols value into lstResult in place of None.
                                 Useful if trying to populate a list of either substitute or default names

    Raises:
        iStatus = 1 if any of lstCols not found in ColInfo

    Returns:
        lstResult (String List): list of metadata values matching lst_dfCols
        iStatus (Integer): Error Status
    """
    iStatus = 0 #Normal exit
    lstResult = []
    for col in lstCols:
        if not col in ColInfo[CI_MetadataDict]:
            iStatus = 1
            continue
        if IsNullVal(ColInfo[CI_MetadataDict][col]) and IsFillColName:
            lstResult.append(col)
        else:
            lstResult.append(ColInfo[CI_MetadataDict][col])
    return lstResult, iStatus


def CI_RenameColsFromImport(ColInfo, df):
    """Rename DataFrame columns to ColInfo default variable names (typically starting from name_import Names
        used in raw data)

    Args:
        ColInfo (Dict): Column Info dictionary of metadata property dictionaries (Units, Import Names etc.)
        df (DataFrame): DataFrame of raw data for column renaming

    Returns:
        df (DataFrame) with ColInfo import column names renamed to default column names
    """
    for col in df.columns:
        altname = FindCIName(ColInfo, 'name_import', col)
        if (not IsNullVal(altname)) and (len(altname) > 0): df.rename(columns={col:altname}, inplace=True)
    return df
def CI_RenameColsForExport(ColInfo, df):
    """Renames columns from default names to ColInfo export names

    Args:
        ColInfo (Dict): Column Info dictionary of metadata property dictionaries (Units, Import Names etc.)
        df (DataFrame): DataFrame of raw data for column renaming

    Returns:
        df (DataFrame) with default column names renamed to ColInfo export names
    """

    for col in df.columns:
        altname = np.nan
        if col in ColInfo['name_export']: altname = ColInfo['name_export'][col]
        if (not IsNullVal(altname)) and (len(altname) > 0): df.rename(columns={col:altname}, inplace=True)
    return df

def FindCIName(ColInfo, CI_AltNameDict, col):
    """Find default ColInfo variable name from a variable's name_import or other name metadata property

    Args:
        ColInfo (Dict): Column Info dictionary of metadata property dictionaries (Units, Import Names etc.).
        NewNameCIDict (String: ColInfo Dict name): Metadata dictionary name in ColInfo (e.g. 'name_export')
        col (String): Default variable name in ColInfo

    Returns:
        df (DataFrame) with import names replaced by default variable (column) names
    """
    for k, v in ColInfo[CI_AltNameDict].items():
        if v == col: return k
    return np.nan

def IsNullVal(val):
    """Return TRUE if val is null"""
    if isinstance(val,float) and math.isnan(val): return True
    return False
