import folium
from datetime import datetime

photo_data = []
with open("photo_data.txt", "r") as data_file:
    for line in data_file:
        parts = line.strip().split(",")
        photo_name = parts[0]
        date_time_str = parts[1]
        lat = float(parts[2])
        lon = float(parts[3])

        # Convert date-time string to a datetime object
        date_time = datetime.strptime(date_time_str, "%Y:%m:%d %H:%M:%S")
        
        photo_data.append((photo_name, date_time, lat, lon))

# Create a map using the "OpenStreetMap" tileset by default
m = folium.Map(location=[photo_data[0][2], photo_data[0][3]], zoom_start=15)

# Add different tile providers
folium.TileLayer('OpenStreetMap').add_to(m)
folium.TileLayer('CartoDB Positron').add_to(m)
folium.TileLayer('Stamen Terrain').add_to(m)

# Add a layer control with buttons to switch between tile providers
folium.LayerControl().add_to(m)

for photo in photo_data:
    marker = folium.Marker(location=[photo[2], photo[3]], popup=photo[0])
    
    # Add a click event to the marker to display a photo preview
    popup_html = f'<img src="{photo[0]}" width="200" height="auto">'
    popup = folium.Popup(popup_html, max_width=250)
    marker.add_child(popup)
    
    marker.add_to(m)

for i in range(len(photo_data) - 1):
    folium.PolyLine(
        locations=[(photo_data[i][2], photo_data[i][3]), (photo_data[i + 1][2], photo_data[i + 1][3])],
        color="blue"
    ).add_to(m)

m.save("photo_map.html")
