# Graphing

Inside this folder is a collection of scripts which we wrote to load databases and to build graphql applications.

Some code may have been executed in python idle resulting in it only needing to be ran once. Thus some minor functions to collect data may be missing,

application/
contains the graphql python application directory

databaseScript/
contains scripts to create countries tables in aws

docs/
contains a readme from just after the requirements change

Lambda for City To LatLng/
Inside this directory is an incomplete and un needed lambda function to turn  a name of a city to a lat lng position
(was going to be used along with a facebook api lambda function.)

LambdaForEventFul/
Inside this directory is a lambda function to call the eventful api to return a list of events

LambdaForPlaces/
Inside this directory is a lambda function to call the google places api to get a list of places

LamdaForReverseGeocoding/
Inside this directory is a lambda functon to call the google api to turn a lat lng coordinate into a reference to our own country and city id

nodeExample/
contains our example node js graphql application

pythonExample/
contains our example python graphql application

webScrapper/
contains an assortment of code to call eventfinda apis and to webscrape content from wikipedia
