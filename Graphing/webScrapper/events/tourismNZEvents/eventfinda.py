import boto3, json, requests

#session = boto3.session.Session(profile_name="autrdproject")
#client = session.client('dynamodb')

url = 'http://api.eventfinda.co.nz/v2/events.json?row=10&fields=event:(url,name,sessions),session:(timezone,datetime_start)&q=concert&order=popularity'

base64string = 'bmE1OjN4MjlqY3J2cHgyMg=='

req = requests.get(url, headers={"Authorization": "Basic "+base64string})
data = json.loads(req.text)

for event in data["events"]:
    print(event["name"])
    print(event["url"])
   #print(event["sessions"]["datetime_start"]) add date
    # can add a way to search by location id?


#client.put_item(
#    TableName="eventfinda",
 #   Item={
  #      "id":{'N': "0"},
   #     "continents": {"SS": continentss.keys()},
    #    "countries": {"SS": countries.keys()}
#    }
#)
#table = session.resource('dynamodb')
#table = table.Table('locations')
