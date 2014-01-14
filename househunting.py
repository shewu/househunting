import apartmentscom
import apartmentsguide

import googlemaps

apple = '1 infinite loop 95014'


def meters_to_miles(meters):
	return int(meters) / 1600


def get_directions(start, end, gmaps):
	directions = gmaps.directions(start, end)
	print "=== %s > %s ===" % (start, end,)
	print meters_to_miles(directions['Directions']['Distance']['meters'])
	print directions['Directions']['Duration']['html']


def to_caltrain_station(address, city, gmaps):
	start = address
	end = city + ' caltrain station'
	get_directions(start, end, gmaps)


def to_apple(address, gmaps):
	get_directions(address, '1 infinite loop 95014', gmaps)


def to_derpbox(address, gmaps):
	get_directions(address, '185 berry st san francisco', gmaps)


def redwood_city(gmaps):
	apartments = set(
		apartmentscom.search_city('redwood city')
		+ apartmentsguide.search_city('redwood city')
	)
	caltrain_stop = 'redwood city caltrain station'

	for apartment in apartments:
		to_caltrain_station(apartment, 'redwood city', gmaps)
		to_apple(apartment, gmaps)


def san_mateo(gmaps):
	apartments = set(
		apartmentscom.search_city('san mateo')
		+ apartmentsguide.search_city('san mateo')
	)
	caltrain_stop = 'san mateo caltrain station'

	for apartment in apartments:
		to_caltrain_station(apartment, 'san mateo', gmaps)
		to_apple(apartment, gmaps)


def googlemaps_example():
	# documentation: http://py-googlemaps.sourceforge.net/
	start = '3 ames street 02142'
	end = '465 bolivar st 02021'

	directions = gmaps.directions(start, end)
	print directions['Directions']['Duration']


def main():
	#googlemaps_example()
	gmaps = googlemaps.GoogleMaps('AIzaSyBHMOZfCCSElPKRh7ub4FAiXWnuGarO5Mo')
	san_mateo(gmaps)
	#redwood_city(gmaps)

if __name__ == '__main__':
	main()
