import requests, json

def main(event, context):
	country = event['country'] if 'country' in event.keys() else None
	city= event['city'] if 'city' in event.keys() else None
	if city is None and country is None:
		return
	elif city is not None and country is None:
		r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?components=locality:'+city+'&key=AIzaSyANQtbsvQe87AclrQpm1aHQNWS6AaltNE4')
	elif city is  None and country is not None:
		r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?components=country:'+country+'&key=AIzaSyANQtbsvQe87AclrQpm1aHQNWS6AaltNE4')
	else:
		r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?components=locality:'+city+'|country:+'country'+&key=AIzaSyANQtbsvQe87AclrQpm1aHQNWS6AaltNE4')
