import requests

def main(event, context):
	latitude = event['lat']
	longitude = event['lng']
	type = event['type']
	radius = event['radius']
	r = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=AIzaSyBQcpjQOlQV6aUWeUXBdXkR9Yu2b0X03Lc&location="+latitude+","+longitude+"&radius="+radius+"&type="+type)
	print(r.text)
