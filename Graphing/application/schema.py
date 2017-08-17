import graphene
from graphene import resolve_only_args
import uuid
from models import LocationTypeTable, LocationTable, CityTable, AirportTable

continentstore = {}
allContinents = False
countrystore = {}
allCountries = False
citystore = {}
allCitys = False
airportstore = {}
allAirports = False

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
	events = graphene.List(lambda: Event)
	def resolve_event(self, args, *_):
		if 'cities' in self.__dict__:
			if self.cities is not None:
				if len(self.cities) > 0:
					return [Event(title="Example Event", location="Eden Park", coordinates=LatLng(latitude=174.7448,longitude=36.8750),type="Sport", description="Come to our example event",city=list(self.cities)[0], country=self.id)]
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
	events = graphene.List(lambda: Event)
	def resolve_events(self, args, *_):
		return [Event(title="Example Event", location="Eden Park", coordinates=LatLng(latitude=174.7448,longitude=36.8750),type="Sport", description="Come to our example event",city=self.id, country=self.country)]
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

class Event(graphene.ObjectType):
	"""Our Event Type To Explore in the the coming sprint"""
	title = graphene.String()
	location = graphene.String()
	coordinates = graphene.Field(LatLng)
	type = graphene.String()
	description = graphene.String()
	city = graphene.Field(lambda: City)
	country = graphene.Field(lambda: Country)
	def resolve_city(self, args, *_):
		return get_city(self.city)
	def resolve_country(self, args, *_):
		return get_country(self.country)

def is_countryairnz_destination(airports):
	pass

def is_cityairnz_destination(airports):
	pass

def get_airport_id(iata):
	pass

def get_batch_airports(ids):
	airportreturn = []
	global airportstore
	idsStored = list(set(ids).intersection(set(airportstore.keys())))
	for x in idsStored:
		airportreturn.append(airportstore[x])
		ids.remove(x)
	airports = list(AirportTable.batch_get(ids))
	if len(airports) > 0 :
		for x in airports:
			airportreturn.append(Airport(id=x.id, name=x.name, airnzdestination=x.airnzdestination,iata=x.iata, icao=x.icao, cities=x.cities, country=x.country))
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
	idsStored = list(set(ids).intersection(set(citystore.keys())))
	for x in idsStored:
		cityreturn.append(citystore[x])
		ids.remove(x)
	cities = list(CityTable.batch_get(ids))
	if len(cities) > 0:
		for x in cities:
			cityreturn.append(City(id = x.id, name=x.name, airports=x.airports,country=x.country))
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
			citystore[z.id] = City(id=z.id, name=z.name,airports=z.airports, country=z.country)
			cities.append(citystore[z.id])
		allCitys = True
		return cities
	elif id is not None:
		if id in citystore.keys():
			return citystore[id]
		else:
			y = CityTable.get(id)
			citystore[y.id] = City(id=y.id, name=y.name, airports=y.airports,country=y.country)
			return citystore[y.id]

def get_batch_countries(ids):
	global countrystore
	countries = []
	idsStored = list(set(ids).intersection(set(countrystore.keys())))
	for x in idsStored:
		countries.append(countrystore[x])
		ids.remove(x)
	countri = list(LocationTable.batch_get(ids))
	if len(countri) > 0:
		for x in countri:
			countries.append(Country(id=x.id, name=x.name, airports=x.airports,population=x.population.replace(",", ""), continent=x.continent, cities=x.cities))
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
		clist = []
		for x in LocationTypeTable.get(0).countries:
			clist.append(x)
		y = list(LocationTable.batch_get(clist))
		allCountries=True
		for z in y:
			countrystore[z.id] = Country(id=z.id, name=z.name, airports=z.airports,population=z.population.replace(",", ""), continent=z.continent, cities=z.cities)
			countries.append(countrystore[z.id])
		return countries
	elif id is not None:
		if id in countrystore.keys():
			return countrystore[id]
		else:
			y = LocationTable.get(str(id))
			if y.type == 'Country':
				countrystore[y.id] = Country(id=y.id, name=y.name, airports=y.airports, population=y.population.replace(",", ""), continent=y.continent, cities=y.cities)
				return countrystore[y.id]
	return None


def get_continent(id=None):
	global allContinents
	global continentstore
	if id is None:
		if allContinents:
			return continentstore.values()
		continents = []
		clist = []
		for x in LocationTypeTable.get(0).continents:
			clist.append(x)
		allContinents = True
		y = list(LocationTable.batch_get(clist))
		for z in y:
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

class Query(graphene.ObjectType):
	'''A Base Query'''
	countries=graphene.List(Country, name=graphene.String())
	continents=graphene.List(Continent, name=graphene.String())
	cities=graphene.List(City, name=graphene.String())
	airports=graphene.List(Airport, iata=graphene.String())

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


schema=graphene.Schema(query=Query, mutation=Mutations)
