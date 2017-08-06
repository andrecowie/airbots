import requests, bs4

r = requests.get("https://en.wikipedia.org/wiki/Lists_of_cities_by_country")

soup = bs4.BeautifulSoup(r.text, 'html.parser')

x = soup.findAll('ul')

for y in x:
    for child in y.parentGenerator():
        a = child.findAll('a')
        for b in a:
            if b.has_attr('title'):
                if 'List of cities' in b['title']:
                    href = b['href']
                    country = b['title'].split('in')[1]

countries = open('GEODATASOURCE-COUNTRY.TXT')
countri = {}
for f in countries:
    country = f.split('\t')
    countri[country[0]] = {'name': country[3].split('\r')[0], "ISO":country[1], "TLD":country[2], "cities": []}

cities = open('GEODATASOURCE-CITIES-FREE.TXT')
for x  in cities:
    city = x.split('\t')
    if city[0] in countri:
        countri[city[0]]['cities'].append(city[1].split('\r')[0])

