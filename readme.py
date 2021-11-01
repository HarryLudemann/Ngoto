import urllib3
import json
import certifi

class metlink():
    __version__ = '0.0.4'
    base_url = 'https://api.opendata.metlink.org.nz/v1/'

    def __init__(self, API_KEY = None):
        self.API_KEY = API_KEY
        if self.API_KEY is None:
            raise ValueError('API_KEY not provided')


    def get_metlink_data(self, API_Path):
        """ Method passed API Path eg 'vehiclepositions' and returns response"""
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        r = http.request(
        'GET',
        API_Path,
        headers={
                'accept': 'application/json',
                'x-api-key': self.API_KEY
            }
        )
        if r.status == 200:
            return json.loads(r.data.decode('utf-8'))
        else:
            raise ValueError('API Error:', json.loads(r.data.decode('utf-8')))


    # GTFS APIS Static public transport data for Wellington in GTFS (General Transit Feed Specification).


    def get_stops(self, trip_id = None, route_id = None):
        """ Returns list of dictionarys of stops infomation, optionally given route_id and or trip_id as filter """
        if trip_id and route_id:
            response = self.get_metlink_data(f'https://api.opendata.metlink.org.nz/v1/gtfs/stops?route_id={route_id}&trip_id={trip_id}') 
        elif trip_id:
            response = self.get_metlink_data(f'https://api.opendata.metlink.org.nz/v1/gtfs/stops?trip_id={trip_id}') 
        elif route_id:
            response = self.get_metlink_data(f'https://api.opendata.metlink.org.nz/v1/gtfs/stops?route_id={route_id}') 
        else:
            response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/gtfs/stops') 
        routes = []
        for entity in response:
            route = {
                'id': entity['id'],
                'stop_id': entity['stop_id'],
                'stop_code': entity['stop_code'],
                'stop_name': entity['stop_name'],
                'stop_desc': entity['stop_desc'],
                'zone_id': entity['zone_id'],
                'stop_lat': entity['stop_lat'],
                'stop_lon': entity['stop_lon'],
                'location_type': entity['location_type'],
                'parent_station': entity['parent_station'],
                'stop_url': entity['stop_url'],
                'stop_timezone': entity['stop_timezone'],
            }
            routes.append(route)
        return routes


    def get_routes(self, stop_id = None):
        """ Returns list of dictionarys of route infomation, optionally given stop_id as filter """
        if stop_id:
            response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/gtfs/routes?stop_id=' + str(stop_id)) 
        else:
            response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/gtfs/routes') 
        routes = []
        for entity in response:
            route = {
                'id': entity['id'],
                'route_id': entity['route_id'],
                'agency_id': entity['agency_id'],
                'route_short_name': entity['route_short_name'],
                'route_long_name': entity['route_long_name'],
                'route_desc': entity['route_desc'],
                'route_type': entity['route_type'],
                'route_color': entity['route_color'],
                'route_text_color': entity['route_text_color'],
                'route_url': entity['route_url'],
            }
            routes.append(route)
        return routes



    # GTFS-RT APIS - Real time data from the public transport network.


    def get_vehicle_positions(self):
        """ Vehicle Positions -  API to get Information about vehicles including location.
            Given nothing, returns list of dictionaries.
            if no busses are active returns empty list
        """
        response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/gtfs-rt/vehiclepositions') 
        vehicle_positions = []
        for entity in response['entity']:
            vehicle_position = {
                'vehicle_id': entity['vehicle']['vehicle']['id'],
                'bearing': entity['vehicle']['position']['bearing'],
                'latitude': entity['vehicle']['position']['latitude'],
                'longitude': entity['vehicle']['position']['longitude']
            }
            vehicle_positions.append(vehicle_position)
        return vehicle_positions


    def get_trip_updates(self):
        """ Trip Updates - Delays, cancellations, changed routes.
            Given nothing, returns list of dictionaries.
            if empty no trip delays or changes
        """
        response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/gtfs-rt/tripupdates')
        trip_updates = []
        for entity in response['entity']:
            trip_update = {
                'stop_id': entity['trip_update']['stop_time_update']['stop_id'],
                'arrival_delay': entity['trip_update']['stop_time_update']['arrival']['delay'],
                'arrival_time': entity['trip_update']['stop_time_update']['arrival']['time'],
                'trip_start_time': entity['trip_update']['trip']['start_time'],
                'vehicle_id': entity['trip_update']['vehicle']['id'],
            }
            trip_updates.append(trip_update)
        return trip_updates


    def get_service_alerts(self):
        """ Trip Updates - Information about unforeseen events affecting routes, stops, or the network.
            Given nothing, returns list of dictionaries.
        """
        response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/gtfs-rt/servicealerts') 
        service_alerts = []
        for entity in response['entity']:
            service_alert = {
                'active_period': entity['alert']['active_period'],
                'effect': entity['alert']['effect'],
                'cause': entity['alert']['cause'],
                'description_text': entity['alert']['description_text']['translation'][0]['text'],
                'header_text': entity['alert']['header_text']['translation'][0]['text'],
                'severity_level': entity['alert']['severity_level'],
                'informed_entity': entity['alert']['informed_entity'],
                #'id': entity['alert']['id'],
                #'timestamp': entity['alert']['timestamp']
            }
            service_alerts.append(service_alert)
        return service_alerts


    # stop predicion API

    def get_stop_predictions(self, stop_id = None):
        """ Passed stop_id, returns list of dictionary's """
        if stop_id:
            response = self.get_metlink_data('https://api.opendata.metlink.org.nz/v1/stop-predictions?stop_id=' + str(stop_id))
            stop_predictions = []
            for stop in response['departures']:
                prediction = {
                    'service_id': stop['service_id'],
                    'name': stop['name'],
                    'vehicle_id': stop['vehicle_id'],
                    'direction': stop['direction'],
                    'status': stop['status'],
                    'trip_id': stop['trip_id'],
                    'delay': stop['delay'],
                    'monitored': stop['monitored'],
                    'operator': stop['operator'],
                    'origin': stop['origin'],
                    'wheelchair_accessible': stop['wheelchair_accessible'],
                    'departure': stop['departure'],
                    'arrival': stop['arrival']
                }
                stop_predictions.append(prediction)
            return stop_predictions
        
        raise ValueError('stop_id must be given for get_stop_predictions') 