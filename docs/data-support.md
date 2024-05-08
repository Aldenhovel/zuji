# 数据支持

本项目所支持的第三方应用数据情况如下，导入指从app获得的数据能够在本程序Dashboard中选择并转化为标准Shortcut数据，导出是指在本项目Export页面能够将标准Shortcut数据转化为符合app格式的数据重新加载到对应程序中。

## 一生足迹【iOS】

- 导入`csv`:white_check_mark: 
- 导出​`csv​`:white_check_mark: 
- 标准数据格式：

```csv
dataTime,locType,longitude,latitude,heading,accuracy,speed,distance,isBackForeground,stepType,altitude
1693482798,1,113.074237,22.633219,0.000000,35.000000,-1.000000,123.444022,1,0,0.000000
1691604801,1,113.073781,22.632168,0.000000,32.204060,6.618274,125.471739,1,0,0.000000
1691682066,1,113.074258,22.632974,0.000000,77.262217,0.925277,101.838244,1,0,0.000000
1691979001,1,113.073139,22.632357,0.000000,54.485453,-1.000000,133.794608,1,0,0.000000
1691979169,1,113.072162,22.631769,0.000000,35.000000,-1.000000,119.720796,1,0,0.000000
......
```

## 灵敢足迹【iOS】

- 导入`csv`:white_check_mark: 
- 导出`csv`:white_check_mark: 
- 标准数据格式：

```csv
geoTime,latitude,longitude,altitude,course,horizontalAccuracy,verticalAccuracy,speed,dayTime,groupTime,isSplit,isMerge,isAdd
1715178872670,22.2493682,113.5356293,27.0,-1.0,35.0,16.7,-1.0,1715097600,1715178872,0,0,0
......
```

## 灵敢足迹【Android】

- 导入`csv`:white_check_mark: 
- 导出`csv`:white_check_mark: 

```
geoTime,latitude,longitude,altitude,course,horizontalAccuracy,verticalAccuracy,speed,status,activity,network,appStatus,dayTime
1714195180492,22.252659,113.535536,0.0,0.0,50.0,0.0,1.57,0,0,0,0,1714147200
1714195187459,22.250341418202478,113.5356457125153,50.09,0.0,3.7900925,0.0,1.28,0,0,0,0,1714147200
1714195249499,22.24983453133266,113.53536238921829,29.04,0.0,7.649937,0.0,0.0,0,0,0,0,1714147200
1714195854484,22.24962334166963,113.53531832635532,14.71,0.0,11.80021,0.0,0.0,0,0,0,0,1714147200
......
```

## 华为运动健康【Android】

- 导入`kml`:white_check_mark: 
- 导出​ :x:
- 标准数据格式：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xsi:schemaLocation="http://earth.google.com/kml/2.1 http://earth.google.com/kml2.1.xsd" version="1.0"
    xmlns="http://earth.google.com/kml/2.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <Folder>
        <ExtendedData>
        	......
        </ExtendedData>
        <name>......</name>
        <Folder>
			......
        </Folder>
        <Folder>
            <name>Track Points</name>
            <Placemark>
                <TimeSpan>
                    <begin>2024-04-11T10:26:48.000Z</begin>
                    <end>2024-04-11T10:26:48.000Z</end>
                </TimeSpan>
                <Point>
                    <altitudeMode>clampToGround</altitudeMode>
                    <coordinates>113.528076,22.254077</coordinates>
                </Point>
            </Placemark>
            <Placemark>
                <TimeSpan>
                    <begin>2024-04-11T10:26:49.000Z</begin>
                    <end>2024-04-11T10:26:49.000Z</end>
                </TimeSpan>
                <Point>
                    <altitudeMode>clampToGround</altitudeMode>
                    <coordinates>113.528084,22.254071</coordinates>
                </Point>
            </Placemark>
            ......
```

## Google Earth【PC】

- 导入`kml`:white_check_mark: 
- 导出`kml`:white_check_mark: 
- 标准数据格式：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml 
     xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<Folder>
		<Folder>
			<name>Track Points</name>
			<Placemark>
				<TimeSpan>
					<begin>2023-08-09T18:12:37Z</begin>
					<end>2023-08-09T18:12:37Z</end>
				</TimeSpan>
				<Point>
					<coordinates>113.074038,22.633149,0</coordinates>
				</Point>
			</Placemark>
			<Placemark>
				<TimeSpan>
					<begin>2023-08-09T18:13:21Z</begin>
					<end>2023-08-09T18:13:21Z</end>
				</TimeSpan>
				<Point>
					<coordinates>113.073781,22.632168,0</coordinates>
				</Point>
			</Placemark>
			......
```

## 行者骑行数据【PC】

- 导入`gpx`:white_check_mark: （需从行者官网下载带有时间及地理坐标的gpx文件）
- 导出 :x:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd" version="1.0" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
    <name>......</name>
    <desc>......</desc>
    <time>......</time>
    <keywords>......</keywords>
    <trk>
        <name>......</name>
        <trkseg>
            <trkpt lat="22.632158" lon="113.075559">
                <ele>14.0</ele>
                <time>2023-01-30T09:15:07Z</time>
            </trkpt>
            <trkpt lat="22.63197" lon="113.075731">
                <ele>-20.0</ele>
                <time>2023-01-30T09:15:37Z</time>
            </trkpt>
			......
```

