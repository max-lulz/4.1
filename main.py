import pysrt
import os
from GPSPhoto import gpsphoto
import math

PI = math.pi

srt_path = "video/DJI_0301.SRT"
img_path = r"D:\ARC Inductions 2019\4.1\images"
images = "images\\"

time_stamp = []
srt_text = []
drone_coords = []
image_coords = []


def get_drone_data():
    pos_sub = pysrt.open(srt_path)

    for data in pos_sub:
        srt_text.append(data.text)
        time_stamp.append(data.start.seconds)

    for text in srt_text:
        text = text.replace(',0', '')
        lat, long = map(float, text.split(','))
        drone_coords.append(polar_to_cart(0, lat, long))


def get_img_data():
    for file in os.listdir(img_path):
        if file.endswith(".JPG"):
            data = gpsphoto.getGPSData(images + file)
            image_coords.append(polar_to_cart(data['Altitude'], data['Latitude'], data['Longitude']))


def polar_to_cart(alt, lat, long):
    x_val = alt * math.cos((lat * PI) / 180) * math.cos((long * PI) / 180)
    y_val = alt * math.cos((lat * PI) / 180) * math.sin((long * PI) / 180)
    z_val = alt * math.sin((lat * PI) / 180) * math.sin((long * PI) / 180)
    cart_coords = [x_val, y_val, z_val]

    return cart_coords


if __name__ == '__main__':
    get_drone_data()
    get_img_data()
