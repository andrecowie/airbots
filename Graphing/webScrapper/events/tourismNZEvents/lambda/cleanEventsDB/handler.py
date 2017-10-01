import boto3, json
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

session = boto3.session.Session()

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

LocationTable._connection = LocationTable._get_connection()
LocationTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
CityTable._connection = CityTable._get_connection()
CityTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
EventTable._connection = EventTable._get_connection()
EventTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')

def main(event, context):
    EventTable.delete_table()
    allCities = json.loads(CityTable.dumps())
    allCountries = json.loads(LocationTable.dumps())
    citiesWithEvents = []
    countriesWithEvents = []
    for x in allCities:
        if 'events' in x[1]['attributes'].keys():
            citiesWithEvents.append(x[0])
    for x in citiesWithEvents:
        CityTable.get(x).update({'events':{'action':"DELETE"}})
    for x in allCountries:
        if 'events' in x[1]['attributes'].keys():
            countriesWithEvents.append(x[0])
    for x in countriesWithEvents:
        LocationTable.get(x).update({'events':{'action':"DELETE"}})
