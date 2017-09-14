from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
import boto3
import json
# session = boto3.session.Session(profile_name='autrdproject')
session = boto3.session.Session()
class KeysIndex(GlobalSecondaryIndex):
     class Meta:
             index_name = 'location-index'
             read_capacity_units = 5
             write_capacity_units = 5
             projection = KeysOnlyProjection()
     name = UnicodeAttribute(hash_key=True)

class LocationTable(Model):
     class Meta:
             table_name="locations"
             region_name= "ap-southeast-2"
     id = UnicodeAttribute(hash_key=True)
     name = UnicodeAttribute()
     name_index = KeysIndex()
     infolink = UnicodeAttribute(null=True)
     population = UnicodeAttribute(null=True)
     type = UnicodeAttribute(null=True)
     continent = UnicodeAttribute(null=True)
     country = UnicodeAttribute(null=True)
     countries = UnicodeSetAttribute(null=True)
     cities = UnicodeSetAttribute(null=True)
     landsize = UnicodeAttribute(null=True)
     airports = UnicodeSetAttribute(null=True)
     events = UnicodeSetAttribute(null=True)

class CitiesNameIndex(GlobalSecondaryIndex):
     class Meta:
             index_name = 'name-index'
             read_capacity_units = 5
             write_capacity_units = 5
             projection = KeysOnlyProjection()
     name = UnicodeAttribute(hash_key=True)


class CityTable(Model):
     class Meta:
             table_name="cities"
             region_name= "ap-southeast-2"
     id = UnicodeAttribute(hash_key=True)
     country = UnicodeAttribute()
     name = UnicodeAttribute()
     name_index = CitiesNameIndex()
     population = UnicodeAttribute(null=True)
     airports = UnicodeSetAttribute(null=True)
     events = UnicodeSetAttribute(null=True)

CityTable._connection = CityTable._get_connection()
CityTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
LocationTable._connection = LocationTable._get_connection()
LocationTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
with open('../webScrapper/events/tourismNZEvents/countriesUpdate.json') as f:
    countries = json.loads(f.read())
with open('../webScrapper/events/tourismNZEvents/citiesUpdate.json') as f:
    cities = json.loads(f.read())
with open('../webScrapper/events/tourismNZEvents/citiesToCreate.json') as f:
    newCities = json.loads(f.read())
for x in countries.keys():
    LocationTable.get(x).update({'events':{'value':countries[x], 'action': 'PUT'}})
for x in cities.keys():
    CityTable.get(x).update({'events':{'value':cities[x], 'action': 'PUT'}})
cityInput = []
for x in newCities:
    cityInput.append(CityTable(name=x['name']['S'], id=x['id']['S'], country=x['country']['S']))
for x in cityInput:
    x.save()