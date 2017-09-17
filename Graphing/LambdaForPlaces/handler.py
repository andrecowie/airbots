import requests
import json

def main(event, context):
    latitude = event['lat']
    longitude = event['lng']
    type = event['type']
    radius = event['radius']
    r = requests.get(
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBQcpjQOlQV6aUWeUXBdXkR9Yu2b0X03Lc&location=" + latitude + "," + longitude + "&radius=" + radius + "&type=" + type)
    data = json.loads(r.text)
    result = []
    for x in data['results']:
        obj = {}
        if 'name' in x.keys():
            obj['name'] = x['name']
        if 'opening_hours' in x.keys():
            if 'open_now' in x['opening_hours'].keys():
                obj['open'] = x['opening_hours']['open_now']
        if 'geometry' in x.keys():
            if 'location' in x['geometry'].keys():
                if 'lat' in x['geometry']['location'].keys():
                    obj['lat'] = x['geometry']['location']['lat']
                if 'lng' in x['geometry']['location'].keys():
                    obj['lng'] = x['geometry']['location']['lng']
        if 'vicinity' in x.keys():
            obj['address'] = x['vicinity']
        if 'rating' in x.keys():
            obj['rating'] = x['rating']
        result.append(obj)
    return result
