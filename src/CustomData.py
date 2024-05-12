import pandas as pd
import os
import croodTransform
import xml.etree.ElementTree as ET
import utils
import re

class YSZJData:

    def __init__(self):
        pass

    columns = ['dataTime', 'locType', 'longitude', 'latitude', 'heading', 'accuracy',
               'speed', 'distance', 'isBackForeground', 'stepType', 'altitude']

    @staticmethod
    def read(filename, default_dir='./data/yszj'):
        return pd.read_csv(os.path.join(default_dir, filename))

    @staticmethod
    def cvtToStandardFormat(custom_df: pd.DataFrame):
        df = pd.DataFrame()
        df['stdTime'] = custom_df['dataTime']
        df['stdLongitude'] = custom_df['longitude']
        df['stdLatitude'] = custom_df['latitude']
        df['cvtFrom'] = 'YS'
        return df

    @staticmethod
    def export(df: pd.DataFrame, filename: str):
        df.to_csv(filename, index=False)


class LGZJData:

    def __init__(self):
        pass

    columns = ['geoTime', 'latitude', 'longitude', 'altitude', 'course', 'horizontalAccuracy', 'verticalAccuracy',
               'speed', 'status', 'activity', 'network', 'appStatus', 'dayTime']

    @staticmethod
    def read(filename, default_dir='./data/lgzj'):
        return pd.read_csv(os.path.join(default_dir, filename))

    @staticmethod
    def cvtToStandardFormat(custom_df: pd.DataFrame):
        df = pd.DataFrame()
        res = custom_df.apply(lambda row: croodTransform.gcj02_to_wgs84(row['longitude'], row['latitude']), axis=1)
        res = pd.DataFrame(res.tolist(), columns=['stdLongitude', 'stdLatitude'])
        df['stdTime'] = custom_df['geoTime'].apply(lambda x: x // 1000)
        df['stdLongitude'] = res['stdLongitude']
        df['stdLatitude'] = res['stdLatitude']
        df['cvtFrom'] = 'LG'
        return df

    @staticmethod
    def export(df: pd.DataFrame, filename: str):
        df.to_csv(filename, index=False)

class KMLData:

    def __init__(self):
        pass

    @staticmethod
    def read(filename, default_dir='./data/kml'):
        """返回ET.ElementTree对象，需要先对内部清洗namespace，返回无namespace的xml树，以及GE导出的<Document>标签"""
        with open(os.path.join(default_dir, filename), 'r', encoding='utf-8') as f:
            data = f.read()
        data = re.sub(r'<kml\s+[^>]*>', '<kml>', data)
        data = re.sub(r'<Document>', '', data, flags=re.DOTALL)
        data = re.sub(r'</Document>', '', data, flags=re.DOTALL)
        tree = ET.fromstring(data)
        return ET.ElementTree(tree)

    @staticmethod
    def cvtStandardFormat(tree: ET.ElementTree):
        root = tree.getroot()
        place_marks = root.findall('Folder')[0] \
            .findall('Folder')[-1] \
            .findall('Placemark')
        ts_start, lon, lat = [], [], []
        for pm in place_marks:
            utc_time_start = pm.find('TimeSpan').find('begin').text
            position = pm.find('Point').find('coordinates').text
            timestamp_start = utils.utctime2Timestamp(utc_time_start)
            longitude, latitude = position.split(',')[:2]   # 有些kml会有第三列数据
            longitude, latitude = float(longitude), float(latitude)
            ts_start.append(timestamp_start)
            lon.append(longitude)
            lat.append(latitude)
        df = pd.DataFrame({
            'stdTime': ts_start,
            'stdLongitude': lon,
            'stdLatitude': lat,
        })
        df['cvtFrom'] = 'KML'
        df['stdTime'] = df['stdTime'].apply(lambda x: x // 1000)
        return df

    @staticmethod
    def export(tree: ET.ElementTree, filename: str):
        tree.write(filename)

class GPXData:
    """
    GPX文件支持行者码表，需要在官网上导出（不是路书，需要带有时间信息）
    """

    def __init__(self):
        pass

    @staticmethod
    def read(filename, default_dir='./data/gpx'):
        """返回ET.ElementTree对象，需要先对内部清洗namespace，返回无namespace的xml树"""
        with open(os.path.join(default_dir, filename), 'r', encoding='utf-8') as f:
            data = f.read()
        data = re.sub(r'<gpx\s+[^>]*>', '<gpx>', data)
        tree = ET.fromstring(data)
        return ET.ElementTree(tree)

    @staticmethod
    def cvtStandardFormat(tree: ET.ElementTree):
        root = tree.getroot()
        points = root.find('trk').find('trkseg').findall('trkpt')
        ts, lon, lat = [], [], []
        for p in points:
            lat.append(float(p.get('lat')))
            lon.append(float(p.get('lon')))
            timestamp = utils.utctime2Timestamp(p.find('time').text)
            ts.append(timestamp)
        df = pd.DataFrame({
            'stdTime': ts,
            'stdLongitude': lon,
            'stdLatitude': lat,
        })
        df['cvtFrom'] = 'GPX'
        df['stdTime'] = df['stdTime'].apply(lambda x: x // 1000)
        return df




