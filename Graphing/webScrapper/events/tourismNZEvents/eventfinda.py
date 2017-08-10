import boto3, json, requests, uuid

client = boto3.client('dynamodb')

url = 'http://api.eventfinda.co.nz/v2/events.json?row=10&fields=event:(url,name,sessions),session:(timezone,datetime_start)&q=concert&order=popularity'
url_loc = 'http://api.eventfinda.co.nz/v2/locations.json?rows=1&levels=2&fields=location:(id,url_slug,name,children)'

base64string = 'bmE1OjN4MjlqY3J2cHgyMg=='

req = requests.get(url, headers={"Authorization": "Basic "+base64string})
data = json.loads(req.text)

req_loc = requests.get(url_loc, headers={"Authorization": "Basic "+base64string})
data_loc = json.loads(req_loc.text)

for loc in data_loc["locations"]:
    print(loc)

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

i = 0

for event in data["events"]:
    id = i
    name = (event["name"])
    url_ = (event["url"])
    #print(event["sessions"]["datetime_start"]) add date
    #can add a way to search by location id?
    print("Adding event: ", id, name, url_)
    FillTable = client.put_item(
        TableName="eventfinda",
        Item={
            'id': {'N': str(id)},
            'name': {'S': name},
            'url': {'S': url_}
        }
    )
    i += 1

#client.put_item(
#    TableName = "eventfinda",
#    Item = {
        # event: name, location, date, category, url
#    }
#)



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
