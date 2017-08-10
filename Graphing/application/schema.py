import graphene
from graphene import resolve_only_args
import uuid
from models import LocationTypeTable, LocationTable

continents = {}
countries = {}


class Location(graphene.Interface):
	id = graphene.ID()
	name = graphene.String()
	destination = graphene.Boolean()


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
		return [get_country(None, i) for i in self.countries]

	def resolve_percentageoftotaleartharea(self, args, *_):
		return float(self.landsize) / float(510000000)

	def resolve_percentageoftotallandarea(self, args, *_):
		return float(self.landsize) / float(148428950)


class Country(graphene.ObjectType):
	class Meta:
		interfaces = (Location,)
	population = graphene.Int()
	continent = graphene.Field(lambda: Continent)

	def resolve_continent(self, args, *_):
		return get_continent(None, self.continent)


def get_country(name=None, id=None):
	if name is None and id is None:
		countries = []
		clist = []
		for x in LocationTypeTable.get(0).countries:
			# clist.append(x.encode('utf-8'))
			clist.append(x)
		y = list(LocationTable.batch_get(clist))
		for z in y:
			countries.append(Country(id=z.id, name=z.name, destination='True',
									 population=z.population.replace(",", ""), continent=z.continent))
		return countries
	elif name is not None and id is None:
		l = LocationTable.name_index.query(name)
		country = []
		for x in l:
			 y = LocationTable.get(x.id)
			 if y.type == "Country":
				 country.append(Country(id=y.id, name=y.name, destination='True',population=y.population.replace(",", ""), continent=y.continent))
		return country
	elif name is None and id is not None:
		print (str(id))
		y = LocationTable.get(str(id))
		return Country(id=y.id, name=y.name, destination='True', population=y.population.replace(",", ""), continent=y.continent)
	else:
		pass


def get_continent(name=None, id=None):
	if name is None and id is None:
		continents = []
		clist = []
		for x in LocationTypeTable.get(0).continents:
			clist.append(x)
		y = list(LocationTable.batch_get(clist))
		for z in y:
			countri = []
			if z.countries == set():
				break
			else:
				if z.countries is not None:
					for x in z.countries:
						countri.append(x)
			continents.append(Continent(id=z.id, name=z.name,
										destination='True', landsize=z.landsize, population=z.population, countries=countri))
		return continents
	elif name is not None and id is None:
		l = LocationTable.name_index.query(name)
		continent = []
		for x in l:
			 y = LocationTable.get(x.id)
			 if y.type == "Continent":
				 countri = []
				 if y.countries is not None:
					 for x in y.countries:
						 countri.append(x)
					 continent.append(Continent(id=y.id, name=y.name, destination='True', landsize=y.landsize, population=y.population, countries=countri))
		return continent
	elif name is None and id is not None:
		y=LocationTable.get(id)
		countri=[]
		if z.countries is not None:
			for x in z.countries:
				countri.append(x)
		return Continent(id=z.id, name=z.name,
						 destination='True', landsize=z.landsize, population=z.population, countries=countri)


class Query(graphene.ObjectType):
	'''A Base Query'''
	countries=graphene.List(Country, name=graphene.String())
	continents=graphene.List(Continent, name=graphene.String())

	@resolve_only_args
	def resolve_countries(self, name=None):
		return get_country(name, None)

	@resolve_only_args
	def resolve_continents(self, name=None):
		return get_continent(name)


schema=graphene.Schema(query=Query)
