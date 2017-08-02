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
    countries = graphene.List(lambda: Country)
    def resolve_countries(self, args, *_):
        return [get_country(None,i) for i in self.countries]
    def resolve_percentageoftotaleartharea(self, args, *_):
        return float(self.landsize)/float(510000000)
    def resolve_percentageoftotallandarea(self, args, *_):
        return float(self.landsize)/float(148428950)

class Country(graphene.ObjectType):
    class Meta:
        interfaces=(Location,)
    population = graphene.Int()
    continent = graphene.Field(lambda: Continent)
    def resolve_continent(self, args, *_):
        return get_continent(None,self.continent)


newzealand = Country(
    id='1baa1c39-6dfa-4e32-a8cb-b2c0773a5742',
    name="New Zealand",
    destination="True",
    population="4802520",
    continent="9ffa0aab-8981-41fb-bf4f-6387adfb7c90"
)

def get_country(name=None, id=None):
    if name is None and id is None:
        countries = []
        clist = []
        for x in LocationTypeTable.get(0).countries:
            clist.append(x.encode('utf-8'))
        y = list(LocationTable.batch_get(clist))
        for z in y:
            countries.append(Country(id=z.id,name=z.name.encode('UTF-8'),destination='True',population=z.population.replace(",",""),continent=z.continent.encode('UTF-8')))
        return countries
    elif name is not None and id is None:
        pass
    elif name is None and id is not None:
        return countries[id]
    else:
        pass

def get_continent(name=None, id=None):
    if name is None and id is None:
        return continents.values()
    elif name is not None and id is None:
        return
    elif name is None and id is not None:
        return continents[id]
    else:
        pass

class Query(graphene.ObjectType):
    '''A Base Query'''
    countries = graphene.List(Country, name=graphene.String())
    continents = graphene.List(Continent, name=graphene.String())
    @resolve_only_args
    def resolve_countries(self, name=None):
        return get_country(name, None)
    @resolve_only_args
    def resolve_continents(self, name=None):
        return get_continent(name)

schema = graphene.Schema(query=Query)
