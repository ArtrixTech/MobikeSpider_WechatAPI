import folium
from bike_class.bike_class import Bike
from mobike_api import get_bikes_square, convert_position, get_bikes_square_multiprocessing
from kml_operations import create

tileset = r'http://{s}.tile.osm.org/{z}/{x}/{y}.png'

# test location
start_lat = 22.6131442749
start_lon = 113.8617736101
all_bike = get_bikes_square_multiprocessing(start_lat, start_lon, 0.008, 0.008)

lats = list()
lons = list()
ids = list()

for bike in all_bike:
    lats.append(bike.lat)
    lons.append(bike.lon)
    ids.append(bike.bike_id)

lats, lons = convert_position(lats, lons)


map_osm = folium.Map(
    location=[
        start_lat,
        start_lon],
    tiles=tileset,
    attr='My Data Attribution',
    zoom_start=18)
print(len(lats))
print(len(lons))
print(len(ids))

for index in range(len(lats)):
    folium.Marker([start_lat, start_lon], popup="id=%s" %
                  ids[index]).add_to(map_osm)

map_osm.save('osm.html')
