import requests, json, boto3
from boto3.dynamodb.conditions import Key, Attr

countryTable =boto3.resource("dynamodb").Table("locations")
cityTable =boto3.resource("dynamodb").Table("cities")

def main(event, context):
	latitude = event['latitude']
	longitude = event['longitude']
	r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&key=AIzaSyANQtbsvQe87AclrQpm1aHQNWS6AaltNE4')
	r = json.loads(r.text)
	for index, value in enumerate(r["results"][0]['address_components']):
		print(value['long_name'] + " Index: " + str(index))
		if 'country' in value['types']:
			countryindex = index
			country = value["long_name"]
	if country:
		response = countryTable.scan(FilterExpression=Attr('name').contains(country))
		if response['Items']:
			countryid = response['Items'][0]['id']
	potentialcity = r["results"][0]['address_components'][countryindex-1]["long_name"]
	response = cityTable.scan(FilterExpression=Attr('name').contains(potentialcity))
	if response['Items']:
		for x in response['Items']:
			if x["country"] == countryid:
				cityid = x['id']
	if cityid and countryid:
		return countryid, cityid
