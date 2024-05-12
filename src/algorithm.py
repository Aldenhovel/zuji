import numpy as np
from sklearn.cluster import KMeans
import math
from math import radians, cos, sin, asin, sqrt
import random
import matplotlib.pyplot as plt
import PIL
import os
PIL.Image.MAX_IMAGE_PIXELS = 233280000

def kMeans(x_y, k):
    if not x_y:
        return [], []
    k = min(len(x_y), k)
    k_means = KMeans(n_clusters=k, n_init='auto')
    k_means.fit(x_y)
    return k_means.cluster_centers_, np.bincount(k_means.labels_)

def getDistanceHaversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r * 1000

def getDistanceWgs84(lon1, lat1, lon2, lat2):
    earthR = 6378137.0
    pi180 = math.pi / 180
    arcLatA, arcLatB = lat1 * pi180, lat2 * pi180
    x = (math.cos(arcLatA) * math.cos(arcLatB) * math.cos((lon1 - lon2) * pi180))
    y = math.sin(arcLatA) * math.sin(arcLatB)
    s = x + y
    if s > 1:
        s = 1
    if s < -1:
        s = -1
    alpha = math.acos(s)
    distance = alpha * earthR
    return distance

def crood2Pix(w_center: int, h_center: int, lon: float, lat: float):
    x, y = w_center, h_center
    move_x, move_y = x * (lon / 180), y * (lat / 90)
    x += move_x
    y -= move_y
    return int(x), int(y)


def reDrawPoints(data, save_dir):
    img = plt.imread('static/media/worldmaps.cf46a66b4311f8f4db7a.jpg')
    nimg = img.copy()
    for ix, row in data.iterrows():
        x, y = crood2Pix(5400 // 2, 2700 // 2, row['stdLongitude'], row['stdLatitude'])
        nimg[y][x] = np.asarray([0, 255, 0])
    tmp_filename = os.path.join(save_dir, f'{str(random.randint(0, 1000000))}.jpg')
    plt.imsave(tmp_filename, nimg)
    return tmp_filename