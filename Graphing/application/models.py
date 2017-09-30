from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
import boto3
import sys
import os

#Commenting out on master as they are my aws config :andre
session = boto3.session.Session(profile_name='autrdproject')
# session = boto3.session.Session()
# client = boto3.client('dynamodb')

class LocationTypeTable(Model):
    class Meta:
        table_name="locationtypes"
        region_name= "ap-southeast-2"
    id = NumberAttribute(default=0,hash_key=True)
    continents = UnicodeSetAttribute(null=True)
    countries = UnicodeSetAttribute(null=True)
    cities = UnicodeSetAttribute(null=True)

class AirportTable(Model):
    class Meta:
        table_name="airports"
        region_name= "ap-southeast-2"
    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=True)
    cities = UnicodeSetAttribute(null=True)
    country = UnicodeAttribute(null=True)
    iata = UnicodeAttribute(null=True)
    icao = UnicodeAttribute(null=True)
    airnzdestination = BooleanAttribute(null=True)

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

LocationTable._connection = LocationTable._get_connection()
LocationTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
LocationTypeTable._connection = LocationTypeTable._get_connection()
LocationTypeTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
CityTable._connection = CityTable._get_connection()
CityTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
AirportTable._connection = AirportTable._get_connection()
AirportTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
if not LocationTable.exists() and not LocationTypeTable.exists():
    LocationTable.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)
    LocationTypeTable.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
    # insert_data()
else:
    print("Tables Exist Doing Nothing")
