import boto3, uuid, bs4
session = boto3.session.Session(profile_name="autrdproject")
client = session.client('dynamodb')
jpn = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :jpn", ExpressionAttributeValues={":jpn" : {'S':"Japan"}}, ExpressionAttributeNames={"#S": "name"})
soup = ''
with open('japancities') as f:
	soup = bs4.BeautifulSoup(f.read())

puts=[]
for y in soup.findAll('tr'):
    cols = y.findAll('td')
    if cols[4].text == 'City':
        item = {"name":{'S':cols[1].text}, "id":{'S':str(uuid.uuid4())},"country":jpn['Items'][0]['id'], 'population': {'S': cols[3].text}}
        puts.append({"PutRequest":{"Item":item}})

sizedputs = []
for i in xrange(0, len(puts), 25):
	sizedputs.append(puts[i:i+25])

idsofjpncities = []
for x in puts:
	idsofjpncities.append(x['PutRequest']['Item']['id']['S'])

for put in sizedputs:
	res = client.batch_write_item(RequestItems={'cities':put})

res = client.update_item(TableName='locations', Key={ 'id': jpn['Items'][0]['id']}, UpdateExpression='SET cities = :auscity', ExpressionAttributeValues = {':auscity':{'SS':idsofjpncities}})
