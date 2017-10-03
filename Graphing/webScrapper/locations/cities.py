import requests
import bs4
import uuid
import boto3
from boto3.dynamodb.conditions import Key

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

r = requests.get("https://en.wikipedia.org/wiki/Lists_of_cities_by_country")

soup = bs4.BeautifulSoup(r.text, 'html.parser')

x = soup.findAll('ul')

for y in x:
    for child in y.parentGenerator():
        a = child.findAll('a')
        for b in a:
            if b.has_attr('title'):
                if 'List of cities' in b['title']:
                    href = b['href']
                    country = b['title'].split('in')[1]

countries = open('GeoDataCities/GEODATASOURCE-COUNTRY.TXT')
countri = {}
for f in countries:
    country = f.split('\t')
    countri[country[0]] = {'name': country[3].split(
        '\r')[0], "ISO": country[1], "TLD": country[2], "places": []}

cities = open('GeoDataCities/GEODATASOURCE-CITIES-FREE.TXT')
for x in cities:
    city = x.split('\t')
    if city[0] in countri:
        countri[city[0]]['places'].append(
            {'name': city[1].split('\r')[0], "id": str(uuid.uuid4())})

countrieskeys = countri.keys()

session = boto3.session.Session(profile_name="autrdproject")
client = session.client('dynamodb')
table = session.resource('dynamodb')
table = table.Table('locations')
allPlaces = []
for x in countrieskeys:
    rangekey = countri[x]['name']
    res = table.query(
        IndexName='location-index',
        KeyConditionExpression=Key('name').eq(rangekey)
    )
    if res['Count'] > 0:
        print("Uploading Places for "+rangekey)
        hashid = res['Items'][0]['id']
        placesIds = []
        putPlaces = []
        for y in countri[x]['places']:
            placesIds.append(y['id'])
            allPlaces.append(y['id'])
            putPlaces.append({
                "PutRequest": {
                    "Item": {
                        'id': {'S': y['id']},
                        'name': {'S': y['name']},
                        'type': {'S': "Place"},
                        'country': {'S': str(hashid)}
                    }
                }
            })
        putPlacesChunks = list(chunks(putPlaces, 25))
        for twentyFivePlaces in putPlacesChunks:
            client.batch_write_item(
                RequestItems={
                    'locations': twentyFivePlaces
                }
            )
        response = client.update_item(
            TableName='locations',
            Key={
                'id': {'S': str(hashid)}
            },
            UpdateExpression='SET place = :p',
            ExpressionAttributeValues={":p": {'SS': placesIds}}
        )
client.update_item(
    TableName='locationtypes',
    Key={
        'id': {'N': 0}
    },
    UpdateExpression='SET places = :p',
    ExpressionAttributeValues={":p": {'SS': allPlaces}}
)
