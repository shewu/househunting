import apartment

from bs4 import BeautifulSoup
import urllib


URL_BASE = 'http://www.apartments.com'


def search_city(city):
    f = urllib.urlopen('%(base)s/search/?query=%(city)s' % {
        'base': URL_BASE,
        'city': city.replace(' ', '%%20')
    })
    bs = BeautifulSoup(f.read())
    search_results = bs.find_all(itemprop='url', href=True)

    apartments = []

    for search_result in search_results:
        follow_link = search_result['href']
        f2 = urllib.urlopen(URL_BASE + follow_link)
        bs2 = BeautifulSoup(f2.read())

        address = apartment.Address(
            street=bs2.find(itemprop='streetAddress').string,
            city=bs2.find(itemprop='addressLocality').string,
            state=bs2.find(itemprop='addressRegion').string,
            zipcode=bs2.find(itemprop='postalCode').string
        )

        name = '(No Name)'
        name_string = bs2.find(itemprop='name').string
        name = name_string if name_string is not None else name
        name_content = bs2.find(itemprop='name').get('content')
        name = name_content if name_content is not None else name
        apartments.append(apartment.Apartment(
            name,
            URL_BASE + follow_link,
            address
        ))

    return apartments
