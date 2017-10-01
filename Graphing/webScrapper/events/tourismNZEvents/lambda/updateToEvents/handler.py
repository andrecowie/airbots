import requests, boto3, json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
session = boto3.session.Session()

class CategoryEventIndex(GlobalSecondaryIndex):
	 class Meta:
			 index_name = 'category-index'
			 read_capacity_units = 1
			 write_capacity_units = 1
			 projection = KeysOnlyProjection()
	 category = UnicodeAttribute(hash_key=True)

class DateEventIndex(GlobalSecondaryIndex):
     class Meta:
             index_name = 'date-index'
             read_capacity_units = 1
             write_capacity_units = 1
             projection = KeysOnlyProjection()
     date = UnicodeAttribute(hash_key=True)

class EventTable(Model):
    class Meta:
        table_name="events"
        region_name="ap-southeast-2"
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=True)
    url = UnicodeAttribute(null=True)
    time = UnicodeAttribute(null=True)
    date = UnicodeAttribute(null=True)
    dateindex = DateEventIndex()
    country = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    latitude = UnicodeAttribute(null=True)
    longitude = UnicodeAttribute(null=True)
    venuename = UnicodeAttribute(null=True)
    category = UnicodeAttribute(null=True)
    categoryindex = CategoryEventIndex()
    description = UnicodeAttribute(null=True)

EventTable._connection = EventTable._get_connection()
EventTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')

def main(event, context):
	if not EventTable.exists():
		print("Creating table")
		EventTable.create_table(read_capacity_units=1, write_capacity_units=5, wait=True)
	lambdaClient = boto3.client('lambda')
	dynamodbClient = boto3.client('dynamodb')
	url = 'http://api.eventfinda.co.nz/v2/events.json?rows=20&fields=event:(url,name,location,category,sessions),session:(timezone,datetime_start)&q=concert&order=popularity'
	base64string = 'bmE1OjN4MjlqY3J2cHgyMg=='
	req = requests.get(url, headers={"Authorization": "Basic "+base64string})
	data = json.loads(req.text)
	count = data['@attributes']['count']
	increment = 0
	nz = dynamodbClient.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':"New Zealand"}}, ExpressionAttributeNames={"#S": "name"})['Items'][0]['id']['S']
	nzcities = dynamodbClient.get_item(TableName='locations', Key={'id':{'S':nz}}, AttributesToGet=['cities'])['Item']['cities']['SS']
	nzcitiesbatchlook = []
	for x in nzcities:
		nzcitiesbatchlook.append({'id': {'S':x}})
	res = dynamodbClient.batch_get_item(RequestItems={
		'cities':{
			'Keys':nzcitiesbatchlook
			}
		})
	while True:
		if increment >= count:
			break
		lambdaClient.invoke(
			FunctionName="GetEventFindaEvents",
			InvocationType="Event",
			LogType="None",
			ClientContext="None",
			Payload=json.dumps({"increment":increment, "nzcities": res['Responses']['cities'], "nz": nz}).encode()
		)
		increment += 20
