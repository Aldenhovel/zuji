import pandas as pd

from CustomData import YSZJData, LGZJData
from StandardData import StandardData

def filterRow(row: pd.Series, save_field):
    if save_field == 'YS':
        return row[[f'YS_{col}' for col in YSZJData.columns] + ['stdTime', 'stdLongitude', 'stdLatitude']]
    if save_field == 'LG':
        return row[[f'LG_{col}' for col in LGZJData.columns] + ['stdTime', 'stdLongitude', 'stdLatitude']]


def mergeAllDataSource(data_source):
    dfs = []
    for source in data_source:
        _type, filename = source.split('-')
        if _type == 'YS':
            ys_df = YSZJData.read(filename)
            dfs.append(YSZJData.cvtToStandardFormat(ys_df))
        elif _type == 'LG':
            lg_df = LGZJData.read(filename)
            dfs.append(LGZJData.cvtToStandardFormat(lg_df))
        elif _type == 'SC':
            sc_df = StandardData.read(filename)
            dfs.append(sc_df)
        else:
            pass
    merged_df = StandardData.mergeDataFrames(dfs)
    return merged_df