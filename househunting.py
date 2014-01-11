import apartmentscom

import googlemaps


def san_mateo(gmaps):
	apartments = [
		'203 laurie meadows drive 94403',
		'55 west 5th avenue 94402',
		'3110 casa de campo 94403',
		'888 n. san mateo dr. 94401',
	]
	caltrain_stop = 'san mateo caltrain station'

	for apartment in apartments:
		directions = gmaps.directions(apartment, caltrain_stop)
		print "===", apartment, "==="
		print directions['Directions']['Distance']
		print directions['Directions']['Duration']['html']


def googlemaps_example():
	# documentation: http://py-googlemaps.sourceforge.net/
	start = '3 ames street 02142'
	end = '465 bolivar st 02021'

	directions = gmaps.directions(start, end)
	print directions['Directions']['Duration']


def main():
	#googlemaps_example()
	gmaps = googlemaps.GoogleMaps('AIzaSyBHMOZfCCSElPKRh7ub4FAiXWnuGarO5Mo')
	print apartmentscom.search_city('san mateo')

if __name__ == '__main__':
	main()
