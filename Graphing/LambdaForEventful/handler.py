import requests, json,boto3
from boto3.dynamodb.conditions import Key, Attr

countryTable =boto3.resource("dynamodb").Table("locations")
cityTable =boto3.resource("dynamodb").Table("cities")

key = "pQFFvbjGbbJBd9nL"

def main(event, context):
	eventarray = []
	if 'search' in event.keys():
		search = "search?q="+event['search']
	if 'location' in event.keys():
		location = "l="+str(event['location'])
	elif 'latlng' in event.keys():
		latitude = event['latlng']['latitude']
		longitude = event['latlng']['latitude']
		location = "where="+latitude+","+longitude
		if 'within' in event.keys():
			location +="&within="+event['within']
	r = requests.get("http://api.eventful.com/json/events/"+search+'&'+location+"&app_key="+key)
	r = json.loads(r.text)
	print(r)
	for x in r['events']['event']:
		obj = {}
		if 'title' in x.keys():
			obj['title']=x['title']
		if 'venue_name' in x.keys():
			obj['venuename'] = x['venue_name']
		if 'latitude' in x.keys() and 'longitude' in x.keys():
			obj['coordinates'] = {'latitude': x['latitude'], 'longitude': x['longitude']}
		if 'description' in x.keys():
			obj['description'] = x['description']
		if 'start_time' in x.keys():
			obj['date'], obj['time'] = x['start_time'].split(' ')
		obj['id'] = x['id']
		response = countryTable.scan(FilterExpression=Attr('name').contains(x['country_name']))
		if response['Items']:
			obj['country'] = response['Items'][0]['id']
		response = cityTable.scan(FilterExpression=Attr('name').contains(x['city_name']))
		if response['Items']:
			for z in response['Items']:
				if z["country"] == obj['country']:
					obj['city'] = z['id']
		eventarray.append(obj)
	return eventarray
