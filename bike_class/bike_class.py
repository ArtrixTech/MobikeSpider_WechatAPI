class Bike:

    _bike_type = ""
    _bike_id = ""
    _lat = ""
    _lon = ""

    # Lat=Y, Lon=X

    def __init__(self, lat, lon, bike_type, bike_id):
        self.lat = lat
        self.lon = lon
        self.bike_type = bike_type
        self.bike_id = bike_id

    def __str__(self):
        properties = dict()
        properties["bike_type"] = self.bike_type
        properties["bike_id"] = self.bike_id
        properties["lat"] = self.lat
        properties["lon"] = self.lon
        import json
        return json.dumps(properties)

    @property
    def bike_type(self):
        return self._bike_type

    @bike_type.setter
    def bike_type(self, value):
        self._bike_type = value

    @property
    def bike_id(self):
        return self._bike_id

    @bike_id.setter
    def bike_id(self, value):
        self._bike_id = value

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def lon(self):
        return self._lon

    @lon.setter
    def lon(self, value):
        self._lon = value
