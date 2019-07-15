import piexif
import pysrt
import os
from GPSPhoto import gpsphoto

srt_path = "video/DJI_0301.SRT"
img_path = r"D:\ARC Inductions 2019\4.1\images"
images = "images\\"

time_stamp = []
coord_string = []
x_values = []
y_values = []


def get_sub_data():
    pos_sub = pysrt.open(srt_path)

    for data in pos_sub:
        coord_string.append(data.text)
        time_stamp.append(data.start.seconds)

    for text in coord_string:
        text = text.replace(',0', '')
        x, y = map(float, text.split(','))
        x_values.append(x)
        y_values.append(y)


def get_exif_data():
    for file in os.listdir(img_path):
        if file.endswith(".JPG"):
            data = gpsphoto.getGPSData(images + file)
            print(data)


if __name__ == '__main__':
    get_exif_data()
