import piexif
import pysrt
import ast

pos_sub = pysrt.open("video/DJI_0301.SRT")

time_stamp = []
coord_string = []
x_value = []
y_value = []


def get_sub_data(subtitle):
    for data in subtitle:
        coord_string.append(data.text)
        time_stamp.append(data.start.seconds)

    for text in coord_string:
        text = text.replace(',0','')
        lat, lng = map(float, text.split(','))
        x_value.append(lat)
        y_value.append(lng)

def get_exif_data():


if __name__ == '__main__':









