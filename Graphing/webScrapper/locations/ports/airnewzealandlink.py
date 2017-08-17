import boto3, bs4, uuid

session = boto3.session.Session(profile_name='autrdproject')
client = session.client('dynamodb')

response = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S': 'New Zealand'}}, ExpressionAttributeNames={"#S": "name"})
nzid = response['Items'][0]['id']['S']

cities = client.scan(TableName='cities', FilterExpression="country = :nz", ExpressionAttributeValues={":nz":{"S":nzid}})

airports = client.scan(TableName='airports', FilterExpression="country = :nz", ExpressionAttributeValues={":nz":{"S":nzid}})

citynames = ['Napier']
iatacodes = []

for x in airports['Items']:
    iatacodes.append(x['iata']['S'])
for x in cities['Items']:
    citynames.append(x['name']['S'])

with open('airnewzealandlink') as f:
    soup = bs4.BeautifulSoup(f.read(), 'html.parser')

rows  = soup.findAll('tr')
oldcities = {}
newcities = {}
cityids = []
airportids = []
newairports = {}
for x in rows:
    cols = x.findAll('td')
    if cols[0].text not in citynames:
        newcities[cols[0].text] = {"name":{'S':cols[0].text}, "id":{'S':str(uuid.uuid4())},"country":{'S':nzid}}
        cityids.append(newcities[cols[0].text]['id']['S'])
    if cols[1].text not in iatacodes:
        airid = str(uuid.uuid4())
        if cols[0].text in newcities.keys():
            newcities[cols[0].text]['airports'] = {'SS': [airid]}
            cityid = newcities[cols[0].text]['id']['S']
        else:
            for x in airports['Items']:
                if x['name']['S'] == cols[0].text:
                    cityid = x['id']['S']
                    oldcities[cityid] = airid
        item={"name":{'S':cols[3].text}, "id":{'S':airid},"country":{'S':nzid}, 'iata': {'S': cols[1].text}, 'icao':{'S':cols[2].text}, 'cities':{'SS': [cityid]}}
        if len(cols[4].findAll('img'))>0 or len(cols[5].findAll('img'))>0:
            item['airnzdestination'] = {'BOOL': True }
            if len(cols[4].findAll('img'))>0:
                item['mtcookdestination'] = {'BOOL': True }
            if len(cols[5].findAll('img'))>0:
                item['airnelsondestination'] = {'BOOL': True }
        newairports[cols[1].text] = item
        airportids.append(item['id']['S'])
put = []
for x in newcities.keys():
    put.append({'PutRequest':{'Item':newcities[x]}})
# res = client.batch_write_item(RequestItems={'cities':put})
print put
put = []
for x in newairports.keys():
    put.append({'PutRequest':{'Item':newairports[x]}})
print put
# res = client.batch_write_item(RequestItems={'airports':put})
# for x in oldcities.keys():
#     res = client.update_item(TableName='cities', Key={ 'id': x }, UpdateExpression='ADD airports :auscity', ExpressionAttributeValues = {':auscity':{'SS':[oldcities[x]]}})
# res = client.update_item(TableName='locations', Key={ 'id': nzid }, UpdateExpression='ADD cities :auscity', ExpressionAttributeValues = {':auscity':{'SS':cityids}})
# res = client.update_item(TableName='locations', Key={ 'id': nzid }, UpdateExpression='ADD airports :auscity', ExpressionAttributeValues = {':auscity':{'SS':airportids}})
