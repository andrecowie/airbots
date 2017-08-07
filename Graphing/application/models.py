from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
import boto3
import sys
import os

#Commenting out on master as they are my aws config :andre
#session = boto3.session.Session(profile_name="autrdproject")
#client = boto3.client('dynamodb')

class KeysIndex(GlobalSecondaryIndex):
     class Meta:
             index_name = 'location-index'
             read_capacity_units = 5
             write_capacity_units = 5
             projection = KeysOnlyProjection()
     name = UnicodeAttribute(hash_key=True)

class LocationTypeTable(Model):
    class Meta:
        table_name="locationtypes"
        region_name= "ap-southeast-2"
    id = NumberAttribute(default=0,hash_key=True)
    continents = UnicodeSetAttribute(null=True)
    countries = UnicodeSetAttribute(null=True)
    cities = UnicodeSetAttribute(null=True)


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
     countries = UnicodeSetAttribute(null=True)
     landsize = UnicodeAttribute(null=True)

#LocationTable._connection = LocationTable._get_connection()
#LocationTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
#LocationTypeTable._connection = LocationTypeTable._get_connection()
#LocationTypeTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')

if not LocationTable.exists() and not LocationTypeTable.exists():
    LocationTable.create_table(read_capacity_units=50, write_capacity_units=50, wait=True)
    LocationTypeTable.create_table(read_capacity_units=10, write_capacity_units=10, wait=True)
    # insert_data()
else:
    print("Tables Exist Doing Nothing")
