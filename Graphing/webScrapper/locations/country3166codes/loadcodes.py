from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
import boto3
from bs4 import BeautifulSoup

session = boto3.session.Session(profile_name='autrdproject')
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
     country3166 = UnicodeAttribute(null=True)
     countries = UnicodeSetAttribute(null=True)
     cities = UnicodeSetAttribute(null=True)
     landsize = UnicodeAttribute(null=True)
     airports = UnicodeSetAttribute(null=True)
     events = UnicodeSetAttribute(null=True)

LocationTable._connection = LocationTable._get_connection()
LocationTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
countriesCodes = []

def main():
     counter = 0
     with open('wikitable') as f:
          countries = BeautifulSoup(f.read())
     for row in countries.findAll('tr'):
          cols = row.findAll('td')
          countriesCodes.append({'name':cols[0].text, 'code':cols[1].text})
     for x in countriesCodes:
          l = LocationTable.name_index.query(x['name'])
          l = list(l)
          if len(l) > 0:
               LocationTable.get(l[0].id).update({'country3166':{'value':x['code'], 'action':'PUT'}})
               print("Updated "+x['name']+" with "+x['code'])

if (__name__ == '__main__'):
     main()
