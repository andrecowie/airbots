import graphene
from graphene import resolve_only_args
import uuid, json, boto3
from models import LocationTypeTable, LocationTable, CityTable, AirportTable, EventTable

# session = boto3.session.Session(profile_name='autrdproject')
lambdaClient = boto3.client('lambda')
# lambdaClient = session.client('lambda')

continentstore = {}
allContinents = False
countrystore = {}
allCountries = False
citystore = {}
allCitys = False
airportstore = {}
allAirports = False
eventstore = {}
allEvents = False
# client = session.client('dynamodb')

class Location(graphene.Interface):
	id = graphene.ID()
	name = graphene.String()


class Continent(graphene.ObjectType):
	'''Continents on earth, landsize is in kilometers squared.'''

	class Meta:
		interfaces = (Location,)
	population = graphene.Field(graphene.Float)
	landsize = graphene.Int()
	percentageoftotallandarea = graphene.Field(lambda: graphene.Float)
	percentageoftotaleartharea = graphene.Field(lambda: graphene.Float)
	countries = graphene.List(lambda: Country, name=graphene.String())
	def resolve_countries(self, args, *_):
		if 'name' in args:
			if 'countries' in self.__dict__:
				countryid = get_countryorcontinent_id(args['name'])
				if countryid is not None:
					if countryid in self.countries:
						return [get_country(countryid)]
				return []
		if 'countries' in self.__dict__:
			if self.countries is not None:
				if len(self.countries) > 1:
					return get_batch_countries(self.countries)
				elif len(self.countries) == 1:
					return [get_countries(self.countries.pop())]
		return []

	def resolve_percentageoftotaleartharea(self, args, *_):
		return float(self.landsize) / float(510000000)

	def resolve_percentageoftotallandarea(self, args, *_):
		return float(self.landsize) / float(148428950)



class Country(graphene.ObjectType):
	class Meta:
		interfaces = (Location,)
	population = graphene.Int()
	airnzdestination = graphene.Field(lambda: graphene.Boolean)
	continent = graphene.Field(lambda: Continent)
	cities =  graphene.List(lambda: City, name=graphene.String())
	airports = graphene.List(lambda: Airport)
	events = graphene.List(lambda: Event, category=graphene.String(), date=graphene.String())
	def resolve_events(self, args, *_):
		if 'events' in self.__dict__:
			if self.events is not None:
				if len(self.events) > 0:
					if 'category' in args and 'date' in args:
						return get_event(self.events, args['category'], args['date'])
					elif 'category' not in args and 'date' in args:
						return get_event(self.events,None, args['date'])
					elif 'category' in args and 'date' not in args:
						return get_event(self.events,args['category'], None)
					else:
						print("Getting Country Events")
						return get_event(self.events, None, None)
				elif len(self.events) == 1:
					return [get_event(self.events.pop())]
		return []
	def resolve_airnzdestination(self, args, *_):
		if 'airports' in self.__dict__:
			return is_countryairnz_destination(self.airports)
		return 'False'
	def resolve_continent(self, args, *_):
		return get_continent(self.continent)
	def resolve_cities(self, args, * _):
		if 'name' in args:
			if 'cities' in self.__dict__:
				cityid = get_city_id(args['name'])
				if self.cities is not None:
					if cityid in list(self.cities):
						return [get_city(cityid)]
				return []
		if 'cities' in self.__dict__:
			if self.cities is not None:
				if len(self.cities) > 1:
					return get_batch_cities(self.cities)
				elif len(self.cities) == 1:
					return [get_city(self.cities.pop())]
		return []
	def resolve_airports(self, args, *_):
		if 'airports' in self.__dict__:
			if self.airports is not None:
				if len(self.airports) > 1:
					return get_batch_airports(self.airports)
				elif len(self.airports) == 1:
					return [get_airport(list(self.airports)[0])]
		return []

class City(graphene.ObjectType):
	'''Cities on earth, some have populations others don't. Are adding more to the database.'''

	class Meta:
		interfaces = (Location,)
	airnzdestination = graphene.Field(lambda: graphene.Boolean)
	airports = graphene.List(lambda: Airport)
	country = graphene.Field(lambda: Country)
	events = graphene.List(lambda: Event, category=graphene.String(), date=graphene.String())
	eventful = graphene.List(lambda: Event, search=graphene.String())
	def resolve_eventful(self, args, *_):
		x = lambdaClient.invoke(FunctionName="eventfulApiCall",InvocationType="RequestResponse", LogType="None", Payload=json.dumps({"location":str(self.name), "search":args['search']}))
		x = x['Payload'].read()
		x = json.loads(x)
		eventfulList = []
		for z in x:
			eventfulList.append(Event(id=z['id'], title=z['title'],description=z['description'],date=z['date'], time=z['time'], location=z['venuename'], category=args['search'], coordinates=LatLng(latitude=z['coordinates']['latitude'],longitude=z['coordinates']['longitude'])))
		return eventfulList
	def resolve_events(self, args, *_):
		if 'events' in self.__dict__:
			if self.events is not None:
				if len(self.events) > 1:
					if 'category' in args and 'date' in args:
						return get_event(self.events, args['category'], args['date'])
					elif 'category' not in args and 'date' in args:
						return get_event(self.events,None, args['date'])
					elif 'category' in args and 'date' not in args:
						return get_event(self.events,args['category'], None)
					else:
						return get_event(self.events, None, None)
				elif len(self.events) == 1:
					return [get_event(list(self.events)[0])]
		return []
	def resolve_airnzdestination(self, args, *_):
		if 'airports' in self.__dict__:
			return is_cityairnz_destination(self.airports)
		return 'False'
	def resolve_airports(self, args, *_):
		if 'airports' in self.__dict__:
			if self.airports is not None:
				if len(self.airports) > 1:
					return get_batch_airports(self.airports)
				elif len(self.airports) == 1:
					return [get_airport(list(self.airports)[0])]
		return []
	def resolve_country(self, args, *_):
		return get_country(self.country)

class Airport(graphene.ObjectType):
	"""Airports adding more. Will look to add airlines"""
	class Meta:
		interfaces = (Location,)
	airnzdestination = graphene.Field(lambda: graphene.Boolean)
	iata = graphene.String()
	icao = graphene.String()
	cities = graphene.List(lambda: City)
	country = graphene.Field(lambda: Country)
	def resolve_airnzdestination(self, args, *_):
		if 'airnzdestination' in self.__dict__:
			if self.airnzdestination is not None:
				return self.airnzdestination
		return False
	def resolve_cities(self, args, *_):
		if 'cities' in self.__dict__:
			if self.cities is not None:
				if len(list(self.cities)) > 1:
					return get_batch_cities(list(self.cities))
				elif len(list(self.cities)) == 1:
					return [get_city(list(self.cities)[0])]
		return []
	def resolve_country(self, args, *_):
		return get_country(self.country)

class LatLng(graphene.ObjectType):
	latitude = graphene.Float()
	longitude = graphene.Float()


class Place(graphene.ObjectType):
	name = graphene.String()
	isopen = graphene.Boolean()
	coordinates = graphene.Field(LatLng)
	address = graphene.String()
	rating = graphene.Field(graphene.Float)

class CityCountryPlace(graphene.ObjectType):
	city = graphene.Field(lambda: City)
	country = graphene.Field(lambda: Country)
	places = graphene.List(lambda: Place, radius=graphene.Int(), category=graphene.String())
	def resolve_city(self, args, *_):
		return get_city(self.city)
	def resolve_country(self, args, *_):
		return get_country(self.country)
	def resolve_places(self, args, *_):
		x = lambdaClient.invoke(FunctionName="placesApiCall",InvocationType="RequestResponse", LogType="None", Payload=json.dumps({"lat":str(self.places[0]), "lng":str(self.places[1]),"type":args['category'], "radius": str(args['radius'])}))
		x = x['Payload'].read()
		print(x)
		x = json.loads(x)
		placesArr = []
		for z in x:
			# print(type(1.2))
			# print(type(z['rating']))
			placesArr.append(Place(name=z['name'], isopen=z['open'] if 'open' in z else None, address=z['address'], rating=z['rating'] if 'rating' in z else None, coordinates=LatLng(latitude=float(z['lat']), longitude=float(z['lng']))))
		return placesArr


class Event(graphene.ObjectType):
	"""Our Event Type To Explore in the the coming sprint"""
	id = graphene.ID()
	title = graphene.String()
	location = graphene.String()
	date = graphene.String()
	time = graphene.String()
	coordinates = graphene.Field(LatLng)
	category = graphene.String()
	description = graphene.String()
	city = graphene.Field(lambda: City)
	country = graphene.Field(lambda: Country)
	def resolve_city(self, args, *_):
		return get_city(self.city)
	def resolve_country(self, args, *_):
		return get_country(self.country)

def get_batch_events(ids):
	methodsIds = list(ids)
	eventreturn = []
	global eventstore
	idsStored = list(set(ids).intersection(set(eventstore.keys())))
	for x in idsStored:
		eventreturn.append(eventstore[x])
		methodsIds.remove(x)
	events = list(EventTable.batch_get(methodsIds))
	if len(events) > 0:
		for x in events:
			eventstore[x.id] = Event(id=x.id, title=x.name,description=x.description,date=x.date, time=x.time, location=x.venuename, category=x.category, country=x.country, city=x.city, coordinates=LatLng(latitude=x.latitude, longitude=x.longitude))
			eventreturn.append(eventstore[x.id])
	return eventreturn

def get_event_id_by_category(category):
	catids=[]
	x = EventTable.categoryindex.query(category)
	for z in x:
		catids.append(z.id)
	return catids

def get_event_id_by_date(date):
	datids = []
	x = EventTable.dateindex.query(date)
	for z in x:
		datids.append(z.id)
	return datids

def get_event(id=None, category=None, date=None):
	global allEvents
	global eventstore
	if id is None:
		if category is not None and date is not None:
			catids = get_event_id_by_category(category)
			datids = get_event_id_by_date(date)
			idstoget = list(set(datids).intersection(set(catids)))
			return get_batch_events(idstoget)
		elif category is not None and date is None:
			return get_batch_events(get_event_id_by_category(category))
		elif category is None and date is not None:
			return get_batch_events(get_event_id_by_date(date))
		else:
			if allEvents:
				return eventstore.values()
			events = []
			y = EventTable.scan()
			for x in y:
				eventstore[x.id] =  Event(id=x.id, title=x.name,description=x.description,date=x.date, time=x.time, location=x.venuename, category=x.category, country=x.country, city=x.city, coordinates=LatLng(latitude=x.latitude, longitude=x.longitude))
				events.append(eventstore[x.id])
			allEvents = True
			return events
	else:
		if isinstance(id, set):
			print("ID is Set")
			if category is not None and date is not None:
				catids = get_event_id_by_category(category)
				datids = get_event_id_by_date(date)
				idstoget = list(set(datids).intersection(set(catids)).intersection(set(id)))
				return get_batch_events(idstoget)
			elif category is not None and date is None:
				idstoget = list(set(get_event_id_by_category(category)).intersection(set(id)))
				return get_batch_events(idstoget)
			elif category is None and date is not None:
				idstoget = list(set(get_event_id_by_date(date)).intersection(set(id)))
				return get_batch_events(get_event_id_by_date(date))
			else:
				return get_batch_events(id)
		elif id in eventstore.keys():
			return eventstore[id]
		else:
			y = EventTable.get(id)
			eventstore[y.id] = Event(id=y.id, title=y.name,description=y.description, date=y.date, time=y.time, location=y.venuename, category=y.category, country=y.country, city=y.city, coordinates=LatLng(latitude=y.latitude, longitude=y.longitude))
			return eventstore[y.id]


def is_countryairnz_destination(airports):
	pass

def is_cityairnz_destination(airports):
	pass

def get_airport_id(iata):
	pass

def get_batch_airports(ids):
	airportreturn = []
	global airportstore
	methodsIds = list(ids)
	idsStored = list(set(ids).intersection(set(airportstore.keys())))
	for x in idsStored:
		airportreturn.append(airportstore[x])
		methodsIds.remove(x)
	airports = list(AirportTable.batch_get(methodsIds))
	if len(airports) > 0 :
		for x in airports:
			airportstore[x.id] = Airport(id=x.id, name=x.name, airnzdestination=x.airnzdestination,iata=x.iata, icao=x.icao, cities=x.cities, country=x.country)
			airportreturn.append(airportstore[x.id])
	return airportreturn

def get_airport(id=None):
	global allAirports
	global airportstore
	if id is None:
		if allAirports:
			return airportstore.values()
		airports = []
		y = AirportTable.scan()
		for x in y:
			airportstore[x.id] =  Airport(id=x.id, name=x.name, airnzdestination=x.airnzdestination,iata=x.iata, icao=x.icao, cities=x.cities, country=x.country)
			airports.append(airportstore[x.id])
		allAirports = True
		return airports
	else:
		if id in airportstore.keys():
			return airportstore[id]
		else:
			y = AirportTable.get(id)
			airportstore[y.id] = Airport(id=y.id, name=y.name, airnzdestination=y.airnzdestination,iata=y.iata, icao=y.icao, cities=y.cities, country=y.country)
			return airportstore[y.id]


def get_batch_cities(ids):
	global citystore
	cityreturn = []
	methodsIds = list(ids)
	idsStored = list(set(ids).intersection(set(citystore.keys())))
	for x in idsStored:
		cityreturn.append(citystore[x])
		methodsIds.remove(x)
	cities = list(CityTable.batch_get(methodsIds))
	if len(cities) > 0:
		for x in cities:
			cityreturn.append(City(id = x.id, name=x.name, airports=x.airports,country=x.country, events=x.events))
	return cityreturn


def get_city_id(name):
	l = CityTable.name_index.query(name)
	l = list(l)
	if len(l) > 0:
		return l[0].id
	return None

def get_city(id=None):
	global allCitys
	global citystore
	if id is None:
		if allCitys:
			return citystore.values()
		cities = []
		y = CityTable.scan()
		for z in y:
			citystore[z.id] = City(id=z.id, name=z.name,airports=z.airports, country=z.country, events=z.events)
			cities.append(citystore[z.id])
		allCitys = True
		return cities
	elif id is not None:
		if id in citystore.keys():
			return citystore[id]
		else:
			y = CityTable.get(id)
			citystore[y.id] = City(id=y.id, name=y.name, airports=y.airports,country=y.country,events=y.events)
			return citystore[y.id]

def get_batch_countries(ids):
	global countrystore
	countries = []
	methodsIds = list(ids)
	idsStored = list(set(ids).intersection(set(countrystore.keys())))
	for x in idsStored:
		countries.append(countrystore[x])
		methodsIds.remove(x)
	countri = list(LocationTable.batch_get(methodsIds))
	if len(countri) > 0:
		for x in countri:
			countries.append(Country(id=x.id, name=x.name, airports=x.airports,population=x.population.replace(",", ""), continent=x.continent, cities=x.cities, events=x.events))
	return countries

def get_countryorcontinent_id(name):
	l = LocationTable.name_index.query(name)
	l = list(l)
	if len(l) > 0:
		print("Returning country id: "+l[0].id)
		return l[0].id
	return None

def get_country(id=None):
	global allCountries
	global countrystore
	if id is None:
		if allCountries:
			return countrystore.values()
		countries = []
		# clist = []
		# for x in LocationTypeTable.get(0).countries:
		# 	clist.append(x)
		y = LocationTable.scan()
		allCountries=True
		for z in y:
			if z.type == 'Country':
				countrystore[z.id] = Country(id=z.id, name=z.name, airports=z.airports,population=z.population.replace(",", ""), continent=z.continent, cities=z.cities, events=z.events)
				countries.append(countrystore[z.id])
		return countries
	elif id is not None:
		if id in countrystore.keys():
			return countrystore[id]
		else:
			y = LocationTable.get(str(id))
			if y.type == 'Country':
				countrystore[y.id] = Country(id=y.id, name=y.name, airports=y.airports, population=y.population.replace(",", ""), continent=y.continent, cities=y.cities, events=y.events)
				return countrystore[y.id]
	return None


def get_continent(id=None):
	global allContinents
	global continentstore
	if id is None:
		if allContinents:
			return continentstore.values()
		continents = []
		# clist = []
		# for x in LocationTypeTable.get(0).continents:
		# 	clist.append(x)
		allContinents = True
		y = LocationTable.scan()
		for z in y:
			if z.type == 'Continent':
				countri = []
				if z.countries == set():
					break
				else:
					if z.countries is not None:
						for x in z.countries:
							countri.append(x)
				continentstore[z.id] = Continent(id=z.id, name=z.name, landsize=z.landsize, population=z.population, countries=countri)
				continents.append(continentstore[z.id])
		return continents
	elif id is not None:
		if id in continentstore.keys():
			return continentstore[id]
		else:
			y=LocationTable.get(id)
			if y.type == 'Continent':
				continentstore[y.id] = Continent(id=y.id, name=y.name, landsize=y.landsize, population=y.population, countries=y.countries)
				return continentstore[y.id]
	return None

class CityInput(graphene.InputObjectType):
	country = graphene.String()
	name = graphene.String()
	population = graphene.Int()
	airports = graphene.List(graphene.ID)

class CreateCity(graphene.Mutation):
	class Input:
		city_data = graphene.Argument(CityInput)
	city = graphene.Field(lambda: City)

	def mutate(root, args, context, info):
		c_data = args.get('city_data')
		countryid = get_countryorcontinent_id(c_data.get('country'))
		if countryid:
			id = str(uuid.uuid4())
			if not c_data.get('airports'):
				print ("No Airports")
				pop = str(c_data.get('population'))
				CityTable(id=id, name=c_data.get('name'), country=countryid,population=pop).save()
				print "City Saved"
				LocationTable.get(countryid).update({'cities':{'action':'add','value':[id]}}).save()
				print "Country Updated"
			else:
				validports = []
				for x in c_data.get('airports'):
					if get_airport(x):
						validports.append(x)
				CityTable(id=id, name=c_data.get('name'), country=countryid,population=c_data.get('population'),airports=validports).save()
				LocationTable.get(countryid).update({'cities':{'action':'add','value':[id]}})
			return CreateCity(get_city(id))
		return CreateCity(City())

class CreateCities(graphene.Mutation):
	class Input:
		city_data = graphene.Argument(graphene.List(CityInput))
	cities = graphene.List(lambda: City)

	@staticmethod
	def mutate(root, args, context, info):
		c_data = args.get('city_data')
		countryid = get_countryorcontinent_id(c_data.get('countryName'))
		if countryid:
			id = str(uuid.uuid4())
			return CreateCity([City(name=a_data.get('name'),airports=a_data.get('airports'),country=countryid,population=a_data.get('population'),id=id)])

class AirportInput(graphene.InputObjectType):
	country = graphene.String()
	cities = graphene.List(graphene.ID)
	# airlines = graphene.ID()
	name = graphene.String()
	iata = graphene.String()
	icao = graphene.String()

class CreateAirport(graphene.Mutation):
	class Input:
		airport_data = graphene.Argument(AirportInput)
	airports = graphene.Field(lambda: Airport)

	@staticmethod
	def mutate(root, args, context, info):
		id = str(uuid.uuid4())
		a_data = args.get('airport_data')
		countryid = get_countryorcontinent_id(a_data.get('country'))
		if countryid:
			cities = []
			cityids =[]
			for x in a_data.get('cities'):
				y = get_city(x)
				if y:
					cityids.append(x)
					cities.append(y)
			for x in cities:
				x.update({'airports':{'action':'add','value':id}}).save()
			get_country(countryid).update({'airports':{'action':'add','value':id}}).save()
			AirportTable(name=a_data.get('name'), iata=a_data.get('iata'), icao=a_data.get('icao'), country=countryid,cities=cityids,id=id).save()
			return CreateAirport(get_airport)
		return CreateAirport(Airport(name=a_data.get('name'), iata=a_data.get('iata'), icao=a_data.get('icao'), airnzdestination='True',country=a_data.get('country'),cities=a_data.get('cities'),id=a_data.get('id')))

class CreateAirports(graphene.Mutation):
	class Input:
		airport_data = graphene.Argument(graphene.List(AirportInput))
	airport = graphene.List(lambda: Airport)

	@staticmethod
	def mutate(root, args, context, info):
		a_data = args.get('airport_data')
		return CreateAirports([Airport(name=a_data.get('name'), iata=a_data.get('iata'), icao=a_data.get('icao'), airnzdestination='True',country=a_data.get('country'),cities=a_data.get('cities'),id=a_data.get('id'))])

class Mutations(graphene.ObjectType):
	createAirport = CreateAirport.Field()
	createCities = CreateCities.Field()
	createCity = CreateCity.Field()

class LatLngInput(graphene.InputObjectType):
	latitude = graphene.Float()
	longitude = graphene.Float()

class Eventful(graphene.InputObjectType):
	search = graphene.String()
	location = graphene.String()

class Query(graphene.ObjectType):
	'''A Base Query'''
	countries=graphene.List(Country, name=graphene.String())
	continents=graphene.List(Continent, name=graphene.String())
	cities=graphene.List(City, name=graphene.String())
	airports=graphene.List(Airport, iata=graphene.String())
	events=graphene.List(Event, city=graphene.String(),category=graphene.String(), date=graphene.String(), eventful=Eventful())
	where =graphene.Field(CityCountryPlace, latlng=LatLngInput())

	@resolve_only_args
	def resolve_countries(self, name=None):
		if name is not None:
			return [get_country(get_countryorcontinent_id(name))]
		else:
			return get_country(None)

	@resolve_only_args
	def resolve_continents(self, name=None):
		if name is not None:
			return [get_continent(get_countryorcontinent_id(name))]
		else:
			return get_continent(None)

	@resolve_only_args
	def resolve_cities(self, name=None, required=False):
		if name is None:
			return get_city(name)
		else:
			return [get_city(get_city_id(name))]

	@resolve_only_args
	def resolve_airports(self, iata=None, required=False):
		if iata is None:
			return get_airport(iata)
		else:
			return get_airport(get_airport_id(iata))

	@resolve_only_args
	def resolve_events(self, category=None, date=None, eventful=None,required=False):
		eventfulList=[]
		if eventful:
			x = lambdaClient.invoke(FunctionName="eventfulApiCall",InvocationType="RequestResponse", LogType="None", Payload=json.dumps({"location":str(eventful['location']), "search":str(eventful['search'])}))
			x = x['Payload'].read()
			x = json.loads(x)
			for z in x:
				eventfulList.append(Event(id=z['id'], title=z['title'],description=z['description'],date=z['date'], time=z['time'], location=z['venuename'], category=eventful['search'], coordinates=LatLng(latitude=z['coordinates']['latitude'],longitude=z['coordinates']['longitude'])))
		if category is None and date is None:
			return get_event(None,None, None)+eventfulList
		elif category is None and date is not None:
				return get_event(None, None, date)+eventfulList
		elif category is not None  and date is None:
				return get_event(None, category, None)+eventfulList
		else:
				return get_event(None,category, date)+eventfulList

	@resolve_only_args
	def resolve_where(self, latlng=None, required=True):
		x = lambdaClient.invoke(FunctionName="reverseGeocode",InvocationType="RequestResponse", LogType="None", Payload=json.dumps({"latitude":str(latlng['latitude']), "longitude":str(latlng['longitude'])}))
		x = json.loads(x['Payload'].read())
		return CityCountryPlace(city=x[1], country=x[0], places=[latlng['latitude'],latlng['longitude']])

schema=graphene.Schema(query=Query, mutation=Mutations)
