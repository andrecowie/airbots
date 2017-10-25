from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection
import boto3, requests, json, uuid

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


class LocationTypeTable(Model):
    class Meta:
        table_name="locationtypes"
        region_name= "ap-southeast-2"
    id = NumberAttribute(default=0,hash_key=True)
    continents = UnicodeSetAttribute(null=True)
    countries = UnicodeSetAttribute(null=True)
    cities = UnicodeSetAttribute(null=True)

LocationTypeTable._connection = LocationTypeTable._get_connection()
LocationTypeTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
LocationTable._connection = LocationTable._get_connection()
LocationTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')
CityTable._connection = CityTable._get_connection()
CityTable._connection.connection._client = session.client('dynamodb', region_name='ap-southeast-2')

def main():
    countries = LocationTable.scan(LocationTable.country3166.exists())
    newcityids = []
    for x in countries:
        if not x.cities:
            r = requests.get("https://api.meetup.com/2/cities?country="+x.country3166+"&page=10")
            r = json.loads(r.text)
            newcitiesid =[]
            newcities =[]
            for newcity in r['results']:
                if newcity['city']:
                    newid = str(uuid.uuid4())
                    newcitiesid.append(newid)
                    newcityids.append(newid)
                    print("adding new city"+newcity['city']+" to "+x.name)
                    newcities.append(CityTable(id=str(newid), country=x.id, name=str(newcity['city'].encode('utf-8'))))
            with CityTable.batch_write() as batch:
                for obj in newcities:
                    print(obj.id)
                    batch.save(obj)
            LocationTable.get(x.id).update({'cities':{'value':newcitiesid, 'action':'ADD'}})
    # x = LocationTypeTable.scan()
    # x= x.next()
    # x.update({'cities':{'value':newcitiesids, 'action':'ADD'}})

if (__name__ == '__main__'):
     main()
