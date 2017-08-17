import boto3, json, requests, uuid
from datetime import datetime

client = boto3.client('dynamodb')

# url = 'http://api.eventfinda.co.nz/v2/events.json?&fields=event:(url,name,location, datetime_summary,sessions,category),session:(timezone,datetime_start) ' #&date_format=%A%20%e%20%B&date_start_end_separator=%20until%20'

# url_loc = 'http://api.eventfinda.co.nz/v2/locations.json?rows=1&levels=2&fields=location:(id,url_slug,name,children)'

nz = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':"New Zealand"}}, ExpressionAttributeNames={"#S": "name"})
nzcities = client.get_item(TableName='locations', Key={'id':{'S':nz['Items'][0]['id']['S']}}, AttributesToGet=['cities'])['Item']['cities']['SS']
nzcitiesbatchlook = []
cityNameToID = {}
countriesUpdate = {nz['Items'][0]['id']['S']: []}
citiesUpdate = {}
eventsToAdd = []
citiesToCreate=[]
for x in nzcities:
    nzcitiesbatchlook.append({'id': {'S':x}})
res = client.batch_get_item(RequestItems={
    'cities':{
        'Keys':nzcitiesbatchlook
        }
    })

for x in res['Responses']['cities']:
    cityNameToID[x['name']['S']] = x['id']['S']

base64string = 'bmE1OjN4MjlqY3J2cHgyMg=='
increment = 0
count = 50
while True:
    if increment >= count:
        break
    url = 'http://api.eventfinda.co.nz/v2/events.json?rows=20&offset='+str(increment)+'&fields=event:(url,name,location,category,sessions),session:(timezone,datetime_start)&q=concert&order=popularity'
    req = requests.get(url, headers={"Authorization": "Basic "+base64string})
    data = json.loads(req.text)
    increment = increment+20
    count = data['@attributes']['count']
    print(increment)
    # req_loc = requests.get(url_loc, headers={"Authorization": "Basic "+base64string})
    # data_loc = json.loads(req_loc.text)

    for events in data["events"]:
        # print(events["sessions"]["sessions"][0]["datetime_start"])
        dt = datetime.strptime(events["sessions"]["sessions"][0]["datetime_start"], "%Y-%m-%d %H:%M:%S")
        cityid = None
        for each in cityNameToID.keys():
            if each in events["location"]["summary"].split(', '):
                cityid = cityNameToID[each]
                break

        eventid = str(uuid.uuid4())
        if not cityid:
            for each in cityNameToID.keys():
                if each in events["location"]["summary"].replace(",","").split(' '):
                    cityid = cityNameToID[each]
                    break
            if not cityid:
                cityid = str(uuid.uuid4())
                cityNameToID[events["location"]["summary"].split(', ')[-1]] = cityid
                citiesToCreate.append({'id': {"S": cityid}, "name": {"S":events["location"]["summary"].split(', ')[-1]}, "country":nz['Items'][0]['id']})
        else:
            if cityid in citiesUpdate.keys():
                citiesUpdate[cityid].append(eventid)
            else:
                citiesUpdate[cityid] = [eventid]
        countriesUpdate[nz['Items'][0]['id']['S']].append(eventid)
        eventitem = {'venuename':{'S':events['location']['name']},"longitude":{'S': str(events["location"]['point']['lng'])},"latitude":{'S': str(events["location"]['point']['lat'])},"category": {'S': events["category"]["name"]},'city':{'S':cityid},"country":nz['Items'][0]['id'],"date":{'S':str(dt.date())}, "time":{'S':str(dt.time())},"id": {'S': eventid}, "name":{'S': events['name']}, "url":{'S':events['url']}}
        eventsToAdd.append({"PutRequest":{"Item":eventitem}})
with open("events.json", 'w') as f:
    json.dump(eventsToAdd, f, indent=4)
with open("citiesToCreate.json", 'w') as f:
    json.dump(citiesToCreate, f, indent=4)
with open("countriesUpdate.json", 'w') as f:
    json.dump(countriesUpdate, f, indent=4)
with open("citiesUpdate.json", 'w') as f:
    json.dump(citiesUpdate, f, indent=4)
print (citiesUpdate)

print (countriesUpdate)

print(eventsToAdd)

print (citiesToCreate)

print (cityNameToID)

sizedputs = []
for i in range(0, len(eventsToAdd), 25):
	sizedputs.append(eventsToAdd[i:i+25])

# res = client.update_item(TableName='locations', Key={ 'id': {'S': countriesUpdate.keys()[0]}}, UpdateExpression='SET events = :ev', ExpressionAttributeValues = {':ev':{'SS':countriesUpdate[countriesUpdate.keys()[0]]}})
# res = client.update_item(TableName='cities', Key={ 'id': {'S': countriesUpdate.keys()[0]}}, UpdateExpression='SET events = :ev', ExpressionAttributeValues = {':ev':{'SS':countriesUpdate[countriesUpdate.keys()[0]]}})
for put in sizedputs:
    res = client.batch_write_item(RequestItems={'events': put})
    print ("Another 25")


    #["datetime_start"]) #["timezone"])
  #  print("ID: "+.__str__())
   # print("EVENT: "+(events["name"]))
   # print(events["category"]["name"])
   # print("URL: "+(events["url"]))
    #print("DATE: "+events["summary"]["startdate_time"])
   # print("LOCATION: "+(events["location"]["name"]))
   # print("CITY: "+(events["location"]["summary"].split(', ')[-1])+"\n")


# response = client.delete_table(
#     TableName="eventfinda"
# )

# creating the DynamoDB table
# table = client.create_table(
#     TableName = 'eventfinda',
#     KeySchema=[
#         {
#             'AttributeName': 'id',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'name',
#             'KeyType': 'RANGE'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'id',
#             'AttributeType': 'N'
#         },
#         {
#             'AttributeName': 'name',
#             'AttributeType': 'S'
#         }
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 10,
#         'WriteCapacityUnits': 10
#     }
# )
#
#
# for event in data["events"]:
#     id = uuid.uuid4()
#     name = (event["name"])
#     category = (event["category"]["name"])
#     url_ = (event["url"])
#     location = (event["location"]["name"])
#     city = (event["location"]["summary"].split(', ')[-1]
#
#     #print(event["sessions"]["datetime_start"]) add date
#     print("Adding event: ", id, name, url_)
#     FillTable = client.put_item(
#         TableName="eventfinda",
#         Item={
#             'id' : {'S' : id},
#             'name': {'S': name},
#             'category': {'S' : category},
#             'url': {'S': url_},
#             'location' : {'S': location},
#             'city' : {'S': city}
#         }
#     )


