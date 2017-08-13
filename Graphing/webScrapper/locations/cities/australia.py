import boto3, uuid, bs4
session = boto3.session.Session(profile_name="autrdproject")
client = session.client('dynamodb')
aus = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':"Australia"}}, ExpressionAttributeNames={"#S": "name"})
soup = ''
with open('australiacities') as f:
	soup = bs4.BeautifulSoup(f.read())

puts=[]
for y in soup.findAll('tr'):
	cols = y.findAll('td')
	item = {"name":{'S':cols[1].text.split(u'\u2013')[0]}, "id":{'S':str(uuid.uuid4())},"country":aus['Items'][0]['id'], 'population': {'S': cols[3].text}}
	puts.append({"PutRequest":{"Item":item}})

sizedputs = []
for i in xrange(0, len(puts), 25):
	sizedputs.append(puts[i:i+25])

for put in sizedputs:
	res = client.batch_write_item(RequestItems={'cities':put})

idsofauscities = []
for x in puts:
	idsofauscities.append(x['PutRequest']['Item']['id']['S'])
res = client.update_item(TableName='locations', Key={ 'id': aus['Items'][0]['id']}, UpdateExpression='SET cities = :auscity', ExpressionAttributeValues = {':auscity':{'SS':idsofauscities}})
