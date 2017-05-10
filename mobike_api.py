import requests
import json
from bike_class.bike_class import Bike
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def convert_position(lat, lon):  # lat,lon are lists.

    print("_______________Point convert Start._______________")

    api = "http://api.gpsspg.com/convert/coord/?oid=4888&key=E9088432D4E3924F6A16CB9727E78003&from=3&to=0&latlng="
    need_request=list()

    k = 0

    conv_lats = list()
    conv_lons = list()
    for index in range(len(lat)):
        api += str(lat[index])
        api += ","
        api += str(lon[index])
        api += ";"
        if index >= k * 14 + 14:
            k += 1
            need_request.append(api)
            api = "http://api.gpsspg.com/convert/coord/?oid=4888&key=E9088432D4E3924F6A16CB9727E78003&from=3&to=0&latlng="

    # Get the rest positions
    api = "http://api.gpsspg.com/convert/coord/?oid=4888&key=E9088432D4E3924F6A16CB9727E78003&from=3&to=0&latlng="
    for index in range(k * 14 + 1, len(lat)):
        api += str(lat[index])
        api += ","
        api += str(lon[index])
        api += ";"
    need_request.append(api)

    def request_posision(url):
        import json
        response = requests.get(url).text
        j = json.loads(response)
        for p in j["result"]:
            conv_lats.append(p["lat"])
            conv_lons.append(p["lng"])

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_process = {executor.submit(request_posision, url): url for url in need_request}

    print("_______________Point convert OK._______________")
    return conv_lats, conv_lons


def get_bikes(lat, lon):

    while True:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E304 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'https://servicewechat.com/wx80f809371ae33eda/26/',
            }
            url = 'https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do'
            data = {
                'longitude': lon,  # 经度
                'latitude': lat,  # 纬度
                'citycode': '0755',
                'errMsg': 'getMapCenterLocation:ok'
            }

            response = json.loads(
                requests.post(
                    url,
                    data=data,
                    headers=headers,
                    timeout=1,
                    verify=False).text)
            all_bikes = list()

            for js in response["object"]:
                new_bike = Bike(
                    js["distY"],
                    js["distX"],
                    js["biketype"],
                    js["bikeIds"])
                all_bikes.append(new_bike)
                print(js["bikeIds"])
            return all_bikes

        except:
            print("retry.")
            continue
        break

def conv(point):
    lon,lat=point[0],point[1]
    bikes=get_bikes(lat,lon)
    return bikes


def get_bikes_square_multiprocessing(middle_lat, middle_lon, width, height):
    start_x = -width / 2 + middle_lon
    start_y = -height / 2 + middle_lat
    step = 0.001

    all_bikes = list()
    all_point = list()
    for index_x in range(int(width / step)):
        for index_y in range(int(height / step)):
            point = [index_x * step + start_x, index_y * step + start_y]
            all_point.append(point)

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_process = {executor.submit(conv, p): p for p in all_point}
        for future in as_completed(future_process):
            result=future.result()
            if isinstance(result,list):
                for bike in result:
                    all_bikes.append(bike)

    return all_bikes


def get_bikes_square(middle_lat, middle_lon, width, height):
    start_x = -width / 2 + middle_lon
    start_y = -height / 2 + middle_lat
    step = 0.001

    all_bikes = list()
    print("%s : %s" % (range(int(width / step)), range(int(height / step))))
    for index_x in range(int(width / step)):
        for index_y in range(int(height / step)):
            print(
                "x%s : y%s" %
                (index_x *
                 step +
                 start_x,
                 index_y *
                 step +
                 start_y))

            bikes = get_bikes(
                index_y * step + start_y,
                index_x * step + start_x)
            for bike in bikes:
                all_bikes.append(bike)
                # print(bike.bike_id)
            time.sleep(0.2)

            bikes = get_bikes(
                index_y * step + start_y,
                index_x * step + start_x)
            for bike in bikes:
                all_bikes.append(bike)
                # print(bike.bike_id)
            time.sleep(0.2)

            bikes = get_bikes(
                index_y * step + start_y,
                index_x * step + start_x)
            for bike in bikes:
                all_bikes.append(bike)
                # print(bike.bike_id)
            time.sleep(0.2)
    return all_bikes
