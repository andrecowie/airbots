import requests

key = "pQFFvbjGbbJBd9nL"

def main(event, context):
	eventarray = []
	if 'search' in event.keys():
		if len(event['search']) > 1:
	
	if 'location' in event.keys():
		location = "location="+str(event['location'])
	elif 'latlng' in event.keys():
		latitude = event['latlng']['latitude']
		longitude = event['latlng]['latitude']
		location = "where="+latitude+","+longitude
		if 'within' in event.keys():
			
		
			
