import re, boto3, uuid bs4

with open('airnz') as f:
	airnzairports = bs4.BeautifulSoup(f.read())

rows = airnzairports.findAll('tr')
airnzdestinations = []
for x in rows:
	cols = x.findAll('td')
	if cols[6].text == 'Present':
		airnzdestinations.append(cols[2].text)

with open('allairports') as f:
	airports = bs4.BeautifulSoup(f.read())

airports = airports.findAll('tr', attrs={'class': None})

client = boto3.session.Session(profile_name='autrdproject')
client = client.client('dynamodb')

updatesToCountries = {}
puts = []
for x in airports:
	cols = x.findAll('td')
	if '(' in cols[2].text or '[' in cols[2].text:
		airname = re.sub('[\(\[].*?[\)\]]', '', cols[2].text)
	else:
		airname = cols[2].text
	airname = airname.replace("Airport", "")
	iata = cols[0].text
	icao = cols[1].text
	country = cols[3].split(', ')[-1]
	potentialcities = cols[3].split(', ')[:-1]
	for index, city in enumerate(potentialcities):
		res = client.query(TableName='cities', IndexName="name-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':city}}, ExpressionAttributeNames={"#S": "name"})
		if res['Count'] == 1:
			potentialcities[index] = res['Items'][0][id]['S']

	airid = str(uuid.uuid4())
	res = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':country}}, ExpressionAttributeNames={"#S": "name"})
     if res['Count'] == 1:
             country = res['Items'][0][id]['S']
			 if country in updatesToCountries:
				 updatesToCountries[country].append(airid)
			else:
				updatesToCountries[country] = [airid]
	item = {"name":{'S':airname}, "id":{'S':airid},"country":{'S':country}, 'iata': {'S': iata}, 'icao':{'S':icao}}
	if iata in airnzdestinations:
		item['Air New Zealand'] = {'BOOL': True}
