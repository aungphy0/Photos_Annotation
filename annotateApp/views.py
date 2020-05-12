from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from PIL import Image, ExifTags
from GPSPhoto import gpsphoto
import geopy
from geopy.geocoders import Nominatim
import pymysql
import os

#for auto orientation of the photos
def rotate_image(filepath):
  try:
    image = Image.open(filepath)
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    image.save(filepath)
    image.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass

#for index.html
def index(request):
    images = os.listdir('media/photos')
    return render(request, 'annotateApp/index.html', {'images' : images})

#for saveimage.html
def saveimage(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
            s = name
            s1 = 'media/photos/' + str(s)

            form.save()
            ls = getImage(s1)
            insert(ls[0], ls[1], ls[2], ls[3], ls[4])
            rotate_image(s1)
            return redirect('index')
    else:
        form = ImageForm()

    return render(request, 'annotateApp/saveimage.html', {'form' : form})

#return the medatada value of the photos
def getImage(filepath):
    img = filepath
    data = gpsphoto.getGPSData(img)
    s = img.split("/")
    img_path = s[1] + "/" + s[2]
    try:
        lat = data['Latitude']
        lon = data['Longitude']
        time = data['Date']
        coordinates = (data['Latitude'], data['Longitude'])
        locator = Nominatim(user_agent='myGeocoder')
        location = locator.reverse(coordinates)
        p_id = location.raw['place_id']
        return [p_id, lat, lon, time, img_path]
    except (AttributeError, KeyError, IndexError):
        return [None, None, None, None, img_path]

#insert the metadata into db
def insert(place_id, lat, lon, time, image):
    print("Inserting image into photos table")
    try:
        connection = pymysql.connect(host='localhost',
                                     database='Metadata',
                                     user='root',
                                     password='')

        cursor = connection.cursor()
        sql_insert = """ INSERT INTO annotateApp_data
                           (place_id, lat, lon, time, image) VALUES (%s,%s,%s,%s,%s)"""


        picture = image
        # Convert data into tuple format
        insert_data = (place_id, lat, lon, time, picture)
        result = cursor.execute(sql_insert, insert_data)
        connection.commit()
        print("Image inserted successfully into photos table", result)

    except pymysql.Error as error:
        print("error pymysql %d: %s" %(e.args[0], e.args[1]))


    finally:
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

#for location.html page
def location(request):
    pid = Data.objects.raw('select * from annotateApp_data')
    ls_dict = {}
    lst = []
    for p in pid:
        if p.place_id in ls_dict or p.place_id is None:
            continue
        else:
            locator = Nominatim(user_agent='myGeocoder')
            location = locator.reverse((p.lat,p.lon))
            lst = location[0].split(",")
            ls_dict[p.place_id] = lst[0] + " " + lst[1]

    return render(request, 'annotateApp/location.html', {'ls' : ls_dict, 'pid' : pid})

#for time.html page
def time(request):
    pdate = Data.objects.raw('select * from annotateApp_data')
    ls_date = []
    for d in pdate:
        if d.time in ls_date:
            continue
        else:
            ls_date.append(d.time)
    return render(request, 'annotateApp/time.html', {'ls_date' : ls_date, 'pdate' : pdate})

#for annotete.html page 
def annotate(request):
    pname = Data.objects.raw('select * from annotateApp_image')
    ls_image = []
    for i in pname:
        if i.name in ls_image:
            continue
        else:
            ls_image.append(i.name)
    return render(request, 'annotateApp/annotate.html', {'ls_image' : ls_image, 'pname' : pname})
