import os                     
import sys                     
from datetime import datetime    
import csv                     
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from prettytable import PrettyTable

def ExtractGPSDictionary(fileName):
    try:
        pilImage = Image.open(fileName)
        exifData = pilImage._getexif()

    except Exception: 
        return None, None

    imageTimeStamp = "NA"
    cameraModel = "NA"
    cameraMake = "NA"
    gpsData = False
    gpsDictionary = {}

    if exifData:
        for tag, theValue in exifData.items():
            tagValue = TAGS.get(tag, tag)

            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = exifData.get(tag).strip()

            if tagValue == "Make":
                cameraMake = exifData.get(tag).strip()

            if tagValue == 'Model':
                cameraModel = exifData.get(tag).strip()

            if tagValue == "GPSInfo":
                gpsData = True
                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag, curTag)
                    gpsDictionary[gpsTag] = theValue[curTag]

        basicExifData = [imageTimeStamp, cameraMake, cameraModel]    

        return gpsDictionary, basicExifData
    else:
        return None, None


def ExtractLatLon(gps):
    try:
        latitude     = gps["GPSLatitude"]
        latitudeRef  = gps["GPSLatitudeRef"]
        longitude    = gps["GPSLongitude"]
        longitudeRef = gps["GPSLongitudeRef"]

        lat, lon = ConvertToDegreesV1(latitude, latitudeRef, longitude, longitudeRef)

        gpsCoor = {"Lat": lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        return gpsCoor

    except Exception as err:
        return None


def ConvertToDegreesV1(lat, latRef, lon, lonRef):
    degrees = lat[0]
    minutes = lat[1]
    seconds = lat[2]
    try:
        seconds = float(seconds)
    except:
        seconds = 0.0

    latDecimal = float(degrees + (minutes / 60) + (seconds / (60 * 60)))
    if latRef == 'S':
        latDecimal = latDecimal * -1.0
        
    degrees = lon[0]
    minutes = lon[1]
    seconds = lon[2]
    try:
        seconds = float(seconds)
    except:
        seconds = 0.0

    lonDecimal = float(degrees + (minutes / 60) + (seconds / (60 * 60)))
    if lonRef == 'W':
        lonDecimal = lonDecimal * -1.0

    return latDecimal, lonDecimal


def process_directory(directory_path):
    latLonList = []
    resultTable = PrettyTable(['File-Name', 'Lat', 'Lon', 'TimeStamp', 'Make', 'Model'])

    resultTable.align["File-Name"] = "l"
    resultTable.align["Lat"] = "l"
    resultTable.align["Lon"] = "l"
    resultTable.align["TimeStamp"] = "l"
    resultTable.align["Make"] = "l"
    resultTable.align["Model"] = "l"
    
    for file in os.listdir(directory_path):
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            file_path = os.path.join(directory_path, file)
            gpsDictionary, exifList = ExtractGPSDictionary(file_path)

            if exifList:
                TS = exifList[0]
                MAKE = exifList[1]
                MODEL = exifList[2]
            else:
                TS = 'NA'
                MAKE = 'NA'
                MODEL = 'NA'

            if gpsDictionary:
                dCoor = ExtractLatLon(gpsDictionary)
                if dCoor:
                    lat = dCoor.get("Lat")
                    lon = dCoor.get("Lon")
                    if lat and lon:
                        latLonList.append([file, lat, lon])
                        resultTable.add_row([file, '{:4.4f}'.format(lat), '{:4.4f}'.format(lon), TS, MAKE, MODEL])
                    else:
                        resultTable.add_row([file, 'No GPS', 'No GPS', TS, MAKE, MODEL])
                else:
                    resultTable.add_row([file, 'No GPS', 'No GPS', TS, MAKE, MODEL])
            else:
                resultTable.add_row([file, 'No GPS', 'No GPS', TS, MAKE, MODEL])

    print(resultTable)
    return latLonList


def save_to_csv(latLonList, output_file='gps_coordinates.csv'):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File-Name", "Latitude", "Longitude"])
        for item in latLonList:
            writer.writerow(item)

if __name__ == "__main__":
    ''' Main Program Entry '''
    print("\nExtract EXIF Data from JPEG Files")
    print("Script Started", str(datetime.now()))
    print()

    directory_path = input("Enter the path to the directory containing JPEG files: ").strip()

    if not os.path.isdir(directory_path):
        print("Invalid directory path. Please try again.")
        sys.exit()

    latLonList = process_directory(directory_path)

    if latLonList:
        save_to_csv(latLonList)
        print("\nGPS Coordinates extracted and saved to gps_coordinates.csv")
        print("You can upload this CSV to MapMaker for mapping the coordinates.")
    else:
        print("No GPS data found in the images.")
print("\nEnd Script")