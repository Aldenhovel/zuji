import PIL.Image
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
PIL.Image.MAX_IMAGE_PIXELS = 233280000
import random

img = plt.imread('../static/media/worldmapl.2fd87ef4e544fcce43ea.jpg')
data = pd.read_csv('../data/shortcut/20240507200524.csv')


def crood2Pix(pic_w: int, pic_h: int, lon: float, lat: float):
    assert pic_w > 0 and pic_h > 0
    assert -180 < lon <= 180 and -90 < lat <= 90
    x, y = pic_w // 2, pic_h // 2
    move_x, move_y = x * (lon / 180), y * (lat / 90)
    x += move_x
    y -= move_y
    return int(x), int(y)


def reDrawPoints(img, data, save_dir='static/media/'):
    nimg = img.copy()
    for ix, row in data.iterrows():
        x, y = crood2Pix(21600, 10800, row['stdLongitude'], row['stdLatitude'])
        nimg[y][x] = np.asarray([0, 255, 0])
    tmp_filename = str(random.randint(0, 1000000))
    plt.imsave(f'../static/media/{tmp_filename}.jpg', nimg)
    return tmp_filename
