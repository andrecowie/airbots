import boto3, json, requests, uuid

client = boto3.client('dynamodb')

url = 'http://api.eventfinda.co.nz/v2/events.json?&fields=event:(url,name,location, sessions),session:(timezone,datetime_start)'
url_loc = 'http://api.eventfinda.co.nz/v2/locations.json?rows=1&levels=2&fields=location:(id,url_slug,name,children)'

base64string = 'bmE1OjN4MjlqY3J2cHgyMg=='

req = requests.get(url, headers={"Authorization": "Basic "+base64string})
data = json.loads(req.text)

req_loc = requests.get(url_loc, headers={"Authorization": "Basic "+base64string})
data_loc = json.loads(req_loc.text)

for events in data["events"]:
    print("ID: "+uuid.uuid4().__str__())
    print("EVENT: "+(events["name"]))
    print("URL: "+(events["url"]))
    print("LOCATION: "+(events["location"]["name"]))
    print("CITY: "+(events["location"]["summary"].split(', ')[-1])+"\n")


# response = client.delete_table(
#     TableName="eventfinda"
# )

# creating the DynamoDB table
# table = client.create_table(
#     TableName = 'eventfinda',
#     KeySchema=[
#         {
#             'AttributeName': 'city',
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
#             'url': {'S': url_},
#             'location' : {'S': location},
#             'city' : {'S': city}
#         }
#     )


