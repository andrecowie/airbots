import requests
from bs4 import BeautifulSoup
url='http://www.tourismnewzealand.com/events/'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')
events = []
for x in soup.findAll("div", {"class":"listing__content"}):
    events.append(x)
eve =[]
for x in events:
    eve.append({'date':x.findAll("span")[0].get_text(),'location': x.findAll("span",{"itemprop":"location"})[0].findAll("span",{"itemprop":"name"})[0].get_text(),'title':x.findAll("a")[0].get_text(),'content':x.findAll("p")[0].get_text()})
for x in eve:
	print (x['date'] + " " +x['location'] +" "+ x['title'])


