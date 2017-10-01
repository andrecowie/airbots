import requests
import bs4
import uuid
import csv
import boto3
import uuid



def insert_data():
	    #session = boto3.session.Session(profile_name="autrdproject")
    client = boto3.client('dynamodb')

    continents = {}
    continents['southamericar']= requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_South_America")
    continents['northamericar']= requests.get("https://en.wikipedia.org/wiki/North_America#Countries.2C_territories.2C_and_dependencies")
    continents['africar']= requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Africa")
    continents['europer']= requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Europe")
    continents['asiar']= requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Asia")
    continents['oceaniar']= requests.get("https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Oceania")
    countries = {}
    continentss = {}
    continentss['540d1e8a-cf32-495f-bc61-3c492fae1946'] = {"name":"Asia", "info": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Asia", "population":"4164252000","landsize":"44579000"}
    continentss['9384c76b-1ca1-4d30-b8de-291f3aeb73b8'] = {"name":"Europe", "info": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Europe", "population":"742452000","landsize":"10180000"}
    continentss['2a889c1b-c80c-4a28-af16-8cc9378391dc'] = {"name":"Antarctica", "info": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Asia", "population":"5000","landsize":"14000000"}
    continentss['b37244c0-a10b-494a-9595-cf4236e35247'] = {"name":"North America", "info": "https://en.wikipedia.org/wiki/North_America#Countries.2C_territories.2C_and_dependencies", "population":"565265000","landsize":"24709000"}
    continentss['84ab029e-6f15-43d8-bc72-dc074bb91130'] = {"name":"South America", "info": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_South_America", "population":"410013492","landsize":"17840000"}
    continentss['9ffa0aab-8981-41fb-bf4f-6387adfb7c90'] = {"name":"Oceania", "info": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Oceania", "population":"41050699","landsize":"8525989"}
    continentss['bf7e4d9e-6559-4d34-b2fd-3002a56b7c26'] = {"name":"Africa", "info": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Africa", "population":"1200000000","landsize":"30370000"}

    nacountries = []
    soup = bs4.BeautifulSoup(continents['northamericar'].text, 'html.parser')
    table = soup.findAll('table')[4]
    rows = table.findAll('tr')[1:-1]
    nacountries = []
    for x in rows:
        elements = x.findAll('td')
        countryid=str(uuid.uuid4())
        nacountries.append(countryid)
        countries[countryid] = {"continent":"b37244c0-a10b-494a-9595-cf4236e35247","name": elements[1].text.encode('utf-8').split('[')[0].split('(')[0].rstrip(),"info":elements[1].findAll('a')[0]['href'].encode('utf-8'), "population":elements[3].find(text=True, recursive=False).encode('utf-8')}
    continentss['b37244c0-a10b-494a-9595-cf4236e35247']['countries'] = nacountries

    oceaniacountries = []
    soup = bs4.BeautifulSoup(continents['oceaniar'].text, 'html.parser')
    table = soup.findAll('table')[1]
    rows = table.findAll('tr')[1:]
    for x in rows:
        elements = x.findAll('td')
        countryid=str(uuid.uuid4())
        oceaniacountries.append(countryid)
        countries[countryid] = {"continent":"9ffa0aab-8981-41fb-bf4f-6387adfb7c90","name":elements[3].findAll('a')[0].text,"info":elements[3].findAll('a')[0]['href'], "population": elements[6].text.encode('utf-8')}
    continentss['9ffa0aab-8981-41fb-bf4f-6387adfb7c90']['countries'] = oceaniacountries

    sacountries = []
    soup = bs4.BeautifulSoup(continents['southamericar'].text, 'html.parser')
    table = soup.findAll('table')[1]
    rows = table.findAll('tr')[1:]
    for x in rows:
        elements = x.findAll('td')
        countryid=str(uuid.uuid4())
        sacountries.append(countryid)
        countries[countryid] = {"continent":"84ab029e-6f15-43d8-bc72-dc074bb91130","name":elements[2].findAll('a')[0].text,"info":elements[2].findAll('a')[0]['href'], "population":elements[5].text.encode('utf-8')}
    continentss["84ab029e-6f15-43d8-bc72-dc074bb91130"]['countries'] = sacountries

    afcountries = []
    soup = bs4.BeautifulSoup(continents['africar'].text, 'html.parser')
    table = soup.findAll('table')[2]
    rows = table.findAll('tr')[1:]
    for x in rows:
        elements = x.findAll('td')
        countryid=str(uuid.uuid4())
        afcountries.append(countryid)
        countries[countryid] = {"continent":"bf7e4d9e-6559-4d34-b2fd-3002a56b7c26","name":elements[2].findAll('a')[0].text,"info":elements[2].findAll('a')[0]['href'], "population":elements[5].text.encode('utf-8')}
    continentss["bf7e4d9e-6559-4d34-b2fd-3002a56b7c26"]['countries'] = afcountries

    ecountries = []
    soup = bs4.BeautifulSoup(continents['europer'].text, 'html.parser')
    table = soup.findAll('table')[1]
    rows = table.findAll('tr')[1:]
    for x in rows:
        elements = x.findAll('td')
        countryid=str(uuid.uuid4())
        ecountries.append(countryid)
        countries[countryid] = {"continent":"9384c76b-1ca1-4d30-b8de-291f3aeb73b8","name":elements[2].findAll('a')[0].text,"info":elements[2].findAll('a')[0]['href'], "population":elements[5].text.encode('utf-8')}
    continentss["9384c76b-1ca1-4d30-b8de-291f3aeb73b8"]['countries'] = ecountries

    acountries = []
    soup = bs4.BeautifulSoup(continents['asiar'].text, 'html.parser')
    table = soup.findAll('table')[1]
    rows = table.findAll('tr')[1:]
    for x in rows:
        elements = x.findAll('td')
        countryid=str(uuid.uuid4())
        acountries.append(countryid)
        countries[countryid] = {"continent":"540d1e8a-cf32-495f-bc61-3c492fae1946","name":elements[2].findAll('a')[0].text,"info":elements[2].findAll('a')[0]['href'], "population":elements[5].text.encode('utf-8')}
    continentss["540d1e8a-cf32-495f-bc61-3c492fae1946"]['countries'] = acountries

    arrayofputs = []
    for x, y in countries.iteritems():
        arrayofputs.append({
            "PutRequest":{
                "Item":{
                    "id": {"S": x},
                    "name": {"S": y['name']},
                    "continent": {"S": y['continent']},
                    "infolink": {"S": "https://en.wikipedia.org"+y['info']},
                    "population": {"S": y['population']},
                    "type": {"S": "Country"}
                }
            }
        })
    for x, y in continentss.iteritems():
        if(y.has_key("countries")):
            arrayofputs.append({
                "PutRequest":{
                    "Item":{
                        "id": {"S": x},
                        "name": {"S": y['name']},
                        "countries": {"SS": y['countries']},
                        "infolink": {"S": y['info']},
                        "population": {"S": y['population']},
                        "type": {"S": "Continent"},
                        "landsize": {"S": y['landsize']}
                    }
                }
            })
        else:
            arrayofputs.append({
                "PutRequest":{
                    "Item":{
                        "id": {"S": x},
                        "name": {"S": y['name']},
                        "infolink": {"S": y['info']},
                        "population": {"S": y['population']},
                        "type": {"S": "Continent"},
                        "landsize": {"S": y['landsize']}
                    }
                }
            })
	def chunks(l, n):
	    """Yield successive n-sized chunks from l."""
	    for i in range(0, len(l), n):
	        yield l[i:i + n]
    arrayportions = list(chunks(arrayofputs, 25))
    for x in arrayportions:
        client.batch_write_item(
            RequestItems={
                'locations': x
            }
        )
    client.put_item(
        TableName="locationtypes",
        Item={
            "id":{'N': "0"},
            "continents": {"SS": continentss.keys()},
            "countries": {"SS": countries.keys()}
        }
    )
