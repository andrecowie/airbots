import boto3, json, requests, uuid
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, NumberAttribute, BooleanAttribute
from pynamodb.indexes import GlobalSecondaryIndex, KeysOnlyProjection

client = boto3.client('dynamodb')
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

# url = 'http://api.eventfinda.co.nz/v2/events.json?&fields=event:(url,name,location, datetime_summary,sessions,category),session:(timezone,datetime_start) ' #&date_format=%A%20%e%20%B&date_start_end_separator=%20until%20'

# url_loc = 'http://api.eventfinda.co.nz/v2/locations.json?rows=1&levels=2&fields=location:(id,url_slug,name,children)'
cityNameToID = {}
countriesUpdate = {}
citiesUpdate = {}
eventsToAdd = []
citiesToCreate=[]
def populate(increment, nz, nzcities):
    for x in nzcities:
        cityNameToID[x['name']['S']] = x['id']['S']
    base64string = 'bmE1OjN4MjlqY3J2cHgyMg=='
    url = 'http://api.eventfinda.co.nz/v2/events.json?rows=20&offset='+str(increment)+'&fields=event:(url,name,location,category,sessions,description),session:(timezone,datetime_start)&order=popularity'
    req = requests.get(url, headers={"Authorization": "Basic "+base64string})
    data = json.loads(req.text)
    for events in data["events"]:
        dt = datetime.strptime(events["sessions"]["sessions"][0]["datetime_start"], "%Y-%m-%d %H:%M:%S")
        cityid = None
        for each in cityNameToID.keys():
            if each in events["location"]["summary"].split(', '):
                cityid = cityNameToID[each]
                break
        eventid = str(uuid.uuid4())
        if not cityid:
            for each in cityNameToID.keys():
                if each in events["location"]["summary"].replace(",","").split(' '):
                    cityid = cityNameToID[each]
                    break
            if not cityid:
                cityid = str(uuid.uuid4())
                cityNameToID[events["location"]["summary"].split(', ')[-1]] = cityid
                citiesToCreate.append({'id':cityid, "name": events["location"]["summary"].split(', ')[-1], "country":nz})
        else:
            if cityid in citiesUpdate.keys():
                citiesUpdate[cityid].append(eventid)
            else:
                citiesUpdate[cityid] = [eventid]
        if nz not in countriesUpdate.keys():
            countriesUpdate[nz] = [eventid]
        else:
            countriesUpdate[nz].append(eventid)
        eventitem = {'description':events['description'].replace('\r', "").replace('\n', ""),'venuename':events['location']['name'],"longitude": str(events["location"]['point']['lng']),"latitude":str(events["location"]['point']['lat']),"category":events["category"]["name"],'city':cityid,"country":nz,"date":str(dt.date()), "time":str(dt.time()),"id": eventid, "name": events['name'], "url":events['url']}
        eventsToAdd.append(eventitem)

def main(event, context):
    populate(event["increment"], event['nz'],event["nzcities"])
    for x in citiesToCreate:
        CityTable(id=x['id'], name=x['name'], country=x['country']).save()
    for x in eventsToAdd:
        EventTable(id=x['id'], name=x['name'], url=x['url'], time=x['time'], date=x['date'], country=x['country'], city=x['city'], latitude=x['latitude'], longitude=x['longitude'],venuename=x['venuename'], category=x['category'], description=x['description']).save()
    for x in countriesUpdate.keys():
        LocationTable.get(x).update({'events':{'action':"ADD", "value": countriesUpdate[x]}})
    for x in citiesUpdate.keys():
        CityTable.get(x).update({'events':{'action':"ADD", "value": citiesUpdate[x]}})
