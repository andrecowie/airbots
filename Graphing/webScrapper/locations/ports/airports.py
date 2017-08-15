import re, boto3, uuid, bs4

def getCountrys():
	countries = ['United States of America', 'New Zealand','Japan','Australia']
	resp = {}
	for i in countries:
		response = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S': i}}, ExpressionAttributeNames={"#S": "name"})
		resp[i] = response['Items'][0]['id']['S']
	return resp

with open('airnz') as f:
	airnzairports = bs4.BeautifulSoup(f.read(), 'html.parser')

rows = airnzairports.findAll('tr')
airnzdestinations = []
for x in rows:
	cols = x.findAll('td')
	if cols[6].text == 'Present':
		airnzdestinations.append(cols[2].text)

with open('allairports') as f:
	airports = bs4.BeautifulSoup(f.read(), 'html.parser')

airports = airports.findAll('tr', attrs={'class': None})

session = boto3.session.Session(profile_name='autrdproject')
client = session.client('dynamodb')

dynamodb = session.resource('dynamodb')
airportTable = dynamodb.Table('airports')

citiestocheck = {}
x = client.scan(TableName='cities', IndexName='name-index',AttributesToGet=['id','name'])
for y in x['Items']:
	citiestocheck[y['name']['S']]=y['id']['S']
updatesToCountries = {'United States of America': [], 'New Zealand': [], 'Japan': [], 'Australia': []}
countriesIds = getCountrys()
updatesToCities = {}
puts = []
listofkeys =[]
for x in airports:
	cols = x.findAll('td')
	if '(' in cols[2].text or '[' in cols[2].text:
		airname = re.sub('[\(\[].*?[\)\]]', '', cols[2].text)
	else:
		airname = cols[2].text
	airname = airname
	iata = cols[0].text
	icao = cols[1].text
	country = cols[3].text.split(', ')[-1]
	potentialcities = cols[3].text.split(', ')[:-1]

	airid = str(uuid.uuid4())
	if country == 'United States':
		country = 'United States of America'
	if country in updatesToCountries.keys():
		updatesToCountries[country].append(airid)
		item={"name":{'S':airname}, "id":{'S':airid},"country":{'S':str(countriesIds[country])}, 'iata': {'S': iata}, 'icao':{'S':icao}, 'cities':{'SS': []}}
		if iata in airnzdestinations:
			item['airnzdestination'] ={'BOOL':True}
		# item={"name":airname, "id":airid,"country":countriesIds[country], 'iata': iata, 'icao':icao, 'cities':[]}
		for city in potentialcities:
			if city in citiestocheck:
				if citiestocheck[city] in updatesToCities:
					updatesToCities[citiestocheck[city]].append(item['id']['S'])
				else:
					updatesToCities[citiestocheck[city]] = [item['id']['S']]
				item['cities']['SS'].append(citiestocheck[city])
				if item['id']['S'] not in listofkeys:
					if item['name']['S'] and item['id']['S'] and item['country']['S'] and item['iata']['S'] and item['icao']['S'] and item['cities']['SS']:
						puts.append({'PutRequest':{ 'Item':item}})
						listofkeys.append(item['id']['S'])
				break
sizedputs = []
for i in xrange(0, len(puts), 25):
	sizedputs.append(puts[i:i+25])

# Insert airports into airports table
# with airportTable.batch_writer() as batch:
# 	for i in puts:
# 		batch.put_item(
# 			Item=i
# 		)
for put in sizedputs:
	res = client.batch_write_item(RequestItems={'airports':put})

# Update countries with airports
for each in updatesToCountries.keys():
	res = client.update_item(TableName='locations', Key={ 'id': {'S':countriesIds[each]}}, UpdateExpression='SET airports = :auscity', ExpressionAttributeValues = {':auscity':{'SS':updatesToCountries[each]}})

# Update cities with airports
for each in updatesToCities.keys():
	res = client.update_item(TableName='cities', Key={ 'id': {'S':each} }, UpdateExpression='SET airports = :auscity', ExpressionAttributeValues = {':auscity':{'SS':updatesToCities[each]}})

print "Added "+str(len(listofkeys)) + " airports."
print "Added airports to "+str(len(updatesToCountries.keys()))+" countries."
print "Added airports to "+str(len(updatesToCities.keys()))+" cities."

















		# res = client.query(TableName='locations', IndexName="location-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':country}}, ExpressionAttributeNames={"#S": "name"})
		# if res['Count'] == 1:
			# country = res['Items'][0]['id']['S']
			# if country in updatesToCountries:
			# 	updatesToCountries[country].append(airid)
			# else:
			# 	updatesToCountries[country] = [airid]
			# item = {"name":{'S':airname}, "id":{'S':airid},"country":{'S':country}, 'iata': {'S': iata}, 'icao':{'S':icao}}
			# if iata in airnzdestinations:
			# 	item['Air News Zealand'] = {'BOOL': True}
			# if 'cities' in client.get_item(TableName="locations", Key={'id':{'S': country}})['Item']:
			# 	for city in potentialcities:
			# 		cityres = client.query(TableName='cities', IndexName="name-index", KeyConditionExpression="#S = :aus", ExpressionAttributeValues={":aus" : {'S':city}}, ExpressionAttributeNames={"#S": "name"})
			# 		if cityres['Count'] == 1:
			# 			if 'cities' in item:
			# 				item['cities']['SS'].append(cityres['Items'][0]['id']['S'])
			# 			else:
			# 				item['cities'] = {'SS':[cityres['Items'][0]['id']['S']]}
			# 			puts.append(item)
