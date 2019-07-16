import pysrt
import os                                                          # NEED TO FIND DIST, AND CLASSIFY
from GPSPhoto import gpsphoto                                      # OPTIM IN DIST
import math
import xlsxwriter

PI = math.pi

srt_path = r"video\DJI_0301.SRT"
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
            if 'Altitude' and 'Latitude' and 'Longitude' in data:
                polar_cords = polar_to_cart(data['Altitude'], data['Latitude'], data['Longitude'])
                polar_cords.append(file)
                image_coords.append(polar_cords)


def polar_to_cart(alt, lat, long):
    x_val = alt * math.cos((lat * PI) / 180) * math.cos((long * PI) / 180)
    y_val = alt * math.cos((lat * PI) / 180) * math.sin((long * PI) / 180)
    z_val = alt * math.sin((lat * PI) / 180) * math.sin((long * PI) / 180)
    cart_coords = [x_val, y_val, z_val]

    return cart_coords


def get_dist(pt1, pt2):
    dist = math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2 + (pt1[2] - pt2[2])**2)
    return dist


def create_excel(sheet_name):
    workbook = xlsxwriter.Workbook(sheet_name + '.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    for drone_pos in drone_coords:
        worksheet.write(row, 0, time_stamp[row])
        for img_pos in image_coords:
            if get_dist(drone_pos, img_pos) < 35:
                worksheet.insert_image(row, 1, images + img_pos[3])

        row += 1

    workbook.close()


if __name__ == '__main__':
    get_drone_data()
    get_img_data()
    create_excel('project')
