import numpy
import shutil
import os
from datetime import datetime
import pytz

def _listFiles(dir, prefix=''):
    csv_files = []
    for filename in os.listdir(dir):
        if filename != ".gitkeep":
            csv_files.append(prefix + filename)
    return csv_files

def getAllDataSource(field):
    data_source = []
    if 'LGZJ' in field:
        data_source.extend(_listFiles('data/lgzj', prefix='【LG】'))
    if 'YSZJ' in field:
        data_source.extend(_listFiles('data/yszj', prefix='【YS】'))
    if 'KML' in field:
        data_source.extend(_listFiles('data/kml', prefix='【KM】'))
    if 'GPX' in field:
        data_source.extend(_listFiles('data/gpx', prefix='【GP】'))
    if 'Shortcut' in field:
        data_source.extend(_listFiles('data/shortcut', prefix='【SC】'))
    return data_source


def floorTimestamp(t: numpy.int64):
    return t - 8 * 60 * 60 - t % (60 * 60 * 24)


def genFileName(prefix='', _format='.csv'):
    now = datetime.now()
    t = now.strftime('%Y%m%d%H%M%S')
    return f'{prefix}{t}{_format}'


def countFiles(folder_path):
    total = 0
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            total += 1
        elif os.path.isdir(item_path):
            total += countFiles(item_path)
    return total

def clearFolder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    file_count = countFiles(folder_path) - 1 # save .gitkeep
    shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, '.gitkeep'), 'w+') as _: pass
    return file_count


def utctime2Timestamp(time_str: str = ''):
    time_formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']
    for time_format in time_formats:
        try:
            time_obj = datetime.strptime(time_str, time_format)
            break
        except:
            continue
    timestamp = int(time_obj.replace(tzinfo=pytz.utc).timestamp() * 1000)
    return timestamp

def timestamp2Utctime(timestamp: int):
    timestamp /= 1000
    time_obj = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    time_str = time_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return time_str

def prettyXml(element, indent='\t', newline='\n', level=0):
    if element:
        if (element.text is None) or element.text.isspace():
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    temp = list(element)
    for sub_element in temp:
        if temp.index(sub_element) < (len(temp) - 1):
            sub_element.tail = newline + indent * (level + 1)
        else:
            sub_element.tail = newline + indent * level
        prettyXml(sub_element, indent, newline, level=level + 1)


from xml.parsers import expat

class DisableXmlNamespaces:
    def __enter__(self):
        self.old_parser_create = expat.ParserCreate
        expat.ParserCreate = lambda encoding, sep: self.old_parser_create(encoding, None)

    def __exit__(self, exc_type, exc_value, traceback):
        expat.ParserCreate = self.old_parser_create