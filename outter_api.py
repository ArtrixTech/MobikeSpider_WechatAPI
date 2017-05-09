from flask import Flask
from bike_class.bike_class import Bike
from mobike_api import get_bikes


app = Flask(__name__)


@app.route('/mobike_api/<lat>,<lon>')
def api_post(lat, lon):
    all_bike = get_bikes(lat, lon)
    text = ""
    for bike in all_bike:
        text += str(bike)
        text += "\n"
    return text

if __name__ == '__main__':
    app.run()
