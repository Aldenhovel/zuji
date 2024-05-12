import pandas as pd
import algorithm
import os
import xml.etree.ElementTree as ET

import croodTransform
import utils
from CustomData import YSZJData, LGZJData, KMLData, GPXData


class StandardData:
    def __init__(self):
        pass

    @staticmethod
    def processToWebUI(df: pd.DataFrame, k=100):
        if len(df) == 0:
            return [], False
        try:
            map_data = []
            for ix, row in df.iterrows():
                latitude, longitude = row['stdLatitude'], row['stdLongitude']
                map_data.append([latitude, longitude])
            map_data = list(set(map(tuple, map_data)))
            centers, cluster_size = algorithm.kMeans(map_data, k)
            clusters = []
            for i in range(len(centers)):
                clusters.append([float(centers[i][1]), float(centers[i][0]), float(cluster_size[i])])
            return clusters, True
        except Exception:
            return [], False

    @staticmethod
    def cvtToYSZJFormat(std_df: pd.DataFrame):
        std_df = std_df.drop_duplicates(subset=['stdTime'])
        df = pd.DataFrame()
        df['dataTime'] = std_df['stdTime']
        df['locType'] = int(1)
        df['longitude'] = std_df['stdLongitude'].map(lambda x: round(x, 6))
        df['latitude'] = std_df['stdLatitude'].map(lambda x: round(x, 6))
        df['heading'] = 0.0
        df['accuracy'] = 40.0
        df['speed'] = -1.0
        df['distance'] = 0.0
        df['isBackForeground'] = int(1)
        df['stepType'] = int(0)
        df['altitude'] = 0.0
        df = df.reset_index()
        for i in range(1, len(df)):
            df.at[i, 'distance'] = algorithm.getDistanceWgs84(df.at[i - 1, 'longitude'], df.at[i - 1, 'latitude'],
                                                                df.at[i, 'longitude'], df.at[i, 'latitude'])
        df = df[['dataTime', 'locType', 'longitude', 'latitude', 'heading', 'accuracy', 'speed', 'distance',
                 'isBackForeground', 'stepType', 'altitude']]
        df = df.sort_values(by='dataTime').drop_duplicates(subset=['dataTime'], keep='last')
        return df

    @staticmethod
    def read(filename):
        return pd.read_csv(os.path.join('data/shortcut', filename))

    @staticmethod
    def cvtToLGZJFormat(std_df: pd.DataFrame, export_os: str = 'android'):
        std_df = std_df.drop_duplicates(subset=['stdTime'])
        df = pd.DataFrame()
        res = std_df.apply(lambda row: croodTransform.wgs84_to_gcj02(row['stdLongitude'], row['stdLatitude']), axis=1)
        res = pd.DataFrame(res.tolist(), columns=['longitude', 'latitude'])
        df['longitude'] = res['longitude']
        df['latitude'] = res['latitude']
        df['dayTime'] = std_df['stdTime'].apply(utils.floorTimestamp)
        if export_os == 'android':
            df['geoTime'] = std_df['stdTime'] * 1000
            df['latitude'] = res['latitude']
            df['longitude'] = res['longitude']
            df['altitude'] = 0.0
            df['course'] = 0.0
            df['horizontalAccuracy'] = 0.0
            df['verticalAccuracy'] = 0.0
            df['speed'] = 0.0
            df['status'] = int(0)
            df['activity'] = int(0)
            df['network'] = int(0)
            df['appStatus'] = int(0)
            df['dayTime'] = std_df['stdTime'].apply(utils.floorTimestamp)
            df = df.reset_index()
            df = df[['geoTime', 'latitude', 'longitude', 'altitude', 'course', 'horizontalAccuracy', 'verticalAccuracy',
                     'speed', 'status', 'activity', 'network', 'appStatus', 'dayTime']]
        elif export_os == 'ios':
            df['geoTime'] = std_df['stdTime'] * 1000
            df['latitude'] = res['latitude']
            df['longitude'] = res['longitude']
            df['altitude'] = 0.0
            df['course'] = -1.0
            df['horizontalAccuracy'] = 0.0
            df['verticalAccuracy'] = 0.0
            df['speed'] = -1.0
            df['dayTime'] = std_df['stdTime'].apply(utils.floorTimestamp)
            df['groupTime'] = std_df['stdTime']
            df['isSplit'] = int(0)
            df['isMerge'] = int(0)
            df['isAdd'] = int(0)
            df = df.reset_index()
            df = df[['geoTime', 'latitude', 'longitude', 'altitude', 'course', 'horizontalAccuracy', 'verticalAccuracy',
                     'speed', 'dayTime', 'groupTime', 'isSplit', 'isMerge', 'isAdd']]
        else:
            raise TypeError(f'{export_os} not support')
        df = df.sort_values(by='geoTime').drop_duplicates(subset=['geoTime'], keep='last')
        return df

    @staticmethod
    def cvtToKMLFormat(std_df: pd.DataFrame):
        std_df = std_df.drop_duplicates(subset=['stdTime'])
        std_df = std_df.reset_index()
        root = ET.Element('kml')
        folder = ET.SubElement(root, 'Folder')
        folder = ET.SubElement(folder, 'Folder')
        name = ET.SubElement(folder, 'name')
        name.text = 'Track Points'
        for ix, row in std_df.iterrows():
            place_mark = ET.SubElement(folder, 'Placemark')
            time_span = ET.SubElement(place_mark, 'TimeSpan')
            begin = ET.SubElement(time_span, 'begin')
            begin.text = utils.timestamp2Utctime(row['stdTime'] * 1000)
            end = ET.SubElement(time_span, 'end')
            end.text = utils.timestamp2Utctime(row['stdTime'] * 1000)
            point = ET.SubElement(place_mark, 'Point')
            coordinates = ET.SubElement(point, 'coordinates')
            coordinates.text = f"{row['stdLongitude']},{row['stdLatitude']}"
        utils.prettyXml(root)
        tree = ET.ElementTree(root)
        return tree

    @staticmethod
    def save(df: pd.DataFrame, filename: str):
        df.to_csv(filename)

    @staticmethod
    def load(filename: str):
        df = pd.read_csv(filename)
        return df

    @staticmethod
    def mergeDataFrames(dfs: list[pd.DataFrame]):
        if dfs:
            df = pd.concat(dfs)
            df = df.drop_duplicates()
            df = df.sort_values(by='stdTime')
        else:
            df = pd.DataFrame()
        return df

    @staticmethod
    def _filterRow(row: pd.Series, save_field):
        if save_field == 'YS':
            return row[[f'YS_{col}' for col in YSZJData.columns] + ['stdTime', 'stdLongitude', 'stdLatitude']]
        if save_field == 'LG':
            return row[[f'LG_{col}' for col in LGZJData.columns] + ['stdTime', 'stdLongitude', 'stdLatitude']]

    @staticmethod
    def mergeAllDataSource(data_source):
        dfs = []
        for source in data_source:
            _type, filename = source.split('】')
            if _type == '【YS':
                ys_df = YSZJData.read(filename)
                dfs.append(YSZJData.cvtToStandardFormat(ys_df))
            elif _type == '【LG':
                lg_df = LGZJData.read(filename)
                dfs.append(LGZJData.cvtToStandardFormat(lg_df))
            elif _type == '【KM':
                kml_tree = KMLData.read(filename)
                dfs.append(KMLData.cvtStandardFormat(kml_tree))
            elif _type == '【GP':
                gpx_tree = GPXData.read(filename)
                dfs.append(GPXData.cvtStandardFormat(gpx_tree))
            elif _type == '【SC':
                sc_df = StandardData.read(filename)
                dfs.append(sc_df)
            else:
                pass
        merged_df = StandardData.mergeDataFrames(dfs)
        return merged_df
