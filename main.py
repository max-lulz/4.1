import pysrt
import os
from GPSPhoto import gpsphoto
import math
import xlsxwriter
from geopy.distance import great_circle

PI = math.pi
images = "Images\\"


# gets GPS and Time data from a .srt file and returns a list
# containing that data for each position of the drone
def get_drone_data(filepath):
    drone_coords = []
    pos_sub = pysrt.open(filepath)
    for i, data in enumerate(pos_sub):
        long, lat, alt = map(float, data.text.split(','))       # gets gps data from .srt text
        start_time = data.start.seconds + data.start.milliseconds/1000
        end_time = data.end.seconds + data.end.milliseconds/1000
        time_stamp = "{} --> {}".format(start_time, end_time)
        coords = {                                              # store individual data as a dict
            "lat": lat,
            "long": long,
            "alt": alt,
            "time": time_stamp,
        }
        drone_coords.append(coords)

    return drone_coords


# gets GPS data from the metadata of the images and returns a list
# with that data and filename of image
def get_img_data(image_path):
    image_coords = []

    for file in os.listdir(image_path):                         # iterate over files and find .JPG files
        if file.endswith(".JPG"):
            data = gpsphoto.getGPSData(images + file)
            if 'Altitude' and 'Latitude' and 'Longitude' in data:       # for images w/o gps data
                coords = {
                    "lat": data['Latitude'],
                    "long": data['Longitude'],
                    "alt": data['Altitude'],
                    "filename": file
                }
                image_coords.append(coords)

    return image_coords


# Obsolete as dist. is now calculated using polar coords
def polar_to_cart(alt, lat, long):
    x_val = alt * math.cos((lat * PI) / 180) * math.cos((long * PI) / 180)
    y_val = alt * math.cos((lat * PI) / 180) * math.sin((long * PI) / 180)
    z_val = alt * math.sin((lat * PI) / 180) * math.sin((long * PI) / 180)
    cart_coords = [x_val, y_val, z_val]

    return cart_coords


# finds distance between 2 points in a 3D space using their polar coordinates
def get_dist(drone_pos, image_pos):
    drone_gps = (drone_pos["lat"], drone_pos["long"])
    img_gps = (image_pos["lat"], image_pos["long"])

    base = great_circle(drone_gps, img_gps).m                   # here, curvature of earth is ignored
    height = abs(drone_pos["alt"] - image_pos["alt"])           # due to small distances and simplicity
    dist = math.sqrt(base ** 2 + height ** 2)                   # of calculations

    return dist


# Classifies Images based on distance from current drone
# position and stores in an Excel file
def classify(excel_name, srt_path, img_path):
    workbook = xlsxwriter.Workbook(excel_name + '.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Time(in seconds)")
    worksheet.write(0, 1, "Images")

    drone_coords = get_drone_data(srt_path)
    image_coords = get_img_data(img_path)

    for row, drone_pos in enumerate(drone_coords, 1):
        worksheet.write(row, 0, drone_pos["time"])
        for img_pos in image_coords:
            if get_dist(drone_pos, img_pos) < 35:
                worksheet.insert_image(row, 1, images + img_pos["filename"])

    workbook.close()


if __name__ == '__main__':
    srtPath = r"Video\DJI_0301.SRT"
    imgPath = r"D:\ARC Inductions 2019\4.1\Images"
    classify('project', srtPath, imgPath)
