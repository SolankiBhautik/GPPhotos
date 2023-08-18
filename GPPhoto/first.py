import os
import exifread
from fractions import Fraction

def convert_to_decimal(degrees, minutes, seconds):
    return degrees + (minutes / 60.0) + (seconds / 3600.0)

photo_directory = "./photos"
photo_data = []

for filename in os.listdir(photo_directory):
    if filename.endswith(".jpg"):
        with open(os.path.join(photo_directory, filename), "rb") as f:
            tags = exifread.process_file(f)
            if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags and "EXIF DateTimeOriginal" in tags:
                lat_parts = tags["GPS GPSLatitude"].values
                lon_parts = tags["GPS GPSLongitude"].values
                
                lat = convert_to_decimal(lat_parts[0], lat_parts[1], lat_parts[2])
                lon = convert_to_decimal(lon_parts[0], lon_parts[1], lon_parts[2])
                
                date_time = str(tags["EXIF DateTimeOriginal"])
                photo_data.append((os.path.join(photo_directory, filename), lat, lon, date_time))

photo_data.sort(key=lambda x: x[3])

with open("photo_data.txt", "w") as data_file:
    for entry in photo_data:
        photo_path = entry[0].replace("\\", "/")  # Replace backslashes with forward slashes
        data_file.write(f"{photo_path},{entry[3]},{entry[1]},{entry[2]}\n")
