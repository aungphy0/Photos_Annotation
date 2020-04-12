"""
pip3 install piexif
pip3 install GPSPhoto
pip3 install exifread
pip3 install reverse_geocoder
pip3 install pprint

"""
#import PIL.Image
from GPSPhoto import gpsphoto
import reverse_geocoder as rg
import pprint
import geopy
from geopy.geocoders import Nominatim
#get the metadata of the image
import pymysql





# img = PIL.Image.open('./proj_photos/IMG-1.JPG')
# exif_data = img._getexif()
#
# for k, v in exif_data.items():
#     print(k)
#     print(v)


# Get the data from image file and return a dictionary
img = './proj_photos/IMG-10.JPG'
data = gpsphoto.getGPSData(img)
s = img.split("/")
p_name = s[-1]
lat = data['Latitude']
lon = data['Longitude']
time = data['UTC-Time'] + " " + data['Date']

#print(data)

coordinates = (data['Latitude'], data['Longitude'])
# result = rg.search(coordinate)
# r = dict(result[0])
# print(r['admin2'])

locator = Nominatim(user_agent='myGeocoder')
#coordinates = “53.480837, -2.244914”
#for i in range(10):
location = locator.reverse(coordinates)
# name = location.raw['display_name']
# n = name.split(",")
# d_name = n[0] + n[1]
p_id = location.raw['place_id']
print(p_id)

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

#print(convertToBinaryData(img))

def insert(name, place_id, lat, lon, time, image):
    print("Inserting image into photos table")
    try:
        connection = pymysql.connect(host='localhost',
                                     database='Metadata',
                                     user='root',
                                     password='')

        cursor = connection.cursor()
        sql_insert = """ INSERT INTO photos
                          (name, place_id, lat, lon, time, image) VALUES (%s,%s,%s,%s,%s,%s)"""

        picture = convertToBinaryData(image)

        # Convert data into tuple format
        insert_data = (name, place_id, lat, lon, time, picture)
        result = cursor.execute(sql_insert, insert_data)
        connection.commit()
        print("Image inserted successfully into photos table", result)

    except pymysql.Error as error:
        print("error pymysql %d: %s" %(e.args[0], e.args[1]))


    finally:
        #if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

insert(p_name, p_id, lat, lon, time, img)
#print(p_name)
