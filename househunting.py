import apartmentscom
import apartmentsguide

import googlemaps

class Result(object):
	def __init__(self, dist, duration):
		self._dist = dist
		self._duration = duration
	
	@property
	def dist(self):
		return self._dist

	@property
	def duration(self):
		return self._duration

	def __str__(self):
		return "%f miles, %f min" % (self.dist, self.duration)


class MetricsResults(object):
	def __init__(self, apartment, result_caltrain, result_apple):
		self._apartment = apartment
		self._result_caltrain = result_caltrain
		self._result_apple = result_apple

	@property
	def apartment(self):
		return self._apartment

	@property
	def result_caltrain(self):
		return self._result_caltrain

	@property
	def result_apple(self):
		return self._result_apple

	def __str__(self):
		return str(self.apartment) + "\n" \
			+ "  to caltrain: %s" % self.result_caltrain + "\n" \
			+ "  to apple: %s" % self.result_apple + "\n"


def meters_to_miles(meters):
	return int(meters) / 1600.


def seconds_to_minutes(seconds):
	return int(seconds) / 60.


def calculate_directions(start, end, gmaps):
	directions = gmaps.directions(start, end)
	return Result(
		dist=meters_to_miles(directions['Directions']['Distance']['meters']),
		duration=seconds_to_minutes(directions['Directions']['Duration']['seconds'])
	)


def to_caltrain_station(address, city, gmaps):
	start = address
	end = city + ' caltrain station'
	return calculate_directions(start, end, gmaps)


def to_apple(address, gmaps):
	return calculate_directions(address, '1 infinite loop 95014', gmaps)


def to_derpbox(address, gmaps):
	return calculate_directions(address, '185 berry st san francisco', gmaps)
	

def apts_in(city, gmaps):
	apartments = set(
		apartmentscom.search_city(city)
		+ apartmentsguide.search_city(city)
	)
	caltrain_stop = '%s caltrain station' % city

	metrics = []

	for apartment in apartments:
		metrics.append(
			MetricsResults(
				apartment=apartment,
				result_caltrain=to_caltrain_station(apartment, city, gmaps),
				result_apple=to_apple(apartment, gmaps)
			)
		)

	return metrics


def googlemaps_example():
	# documentation: http://py-googlemaps.sourceforge.net/
	start = '3 ames street 02142'
	end = '465 bolivar st 02021'

	directions = gmaps.directions(start, end)
	print directions['Directions']['Duration']


def main():
	gmaps = googlemaps.GoogleMaps('AIzaSyBHMOZfCCSElPKRh7ub4FAiXWnuGarO5Mo')
	all_results = apts_in('san mateo', gmaps) \
		+ apts_in('redwood city', gmaps)

	for result in sorted(all_results, key=lambda mr: mr.result_caltrain.duration + mr.result_apple.duration):
		print result

if __name__ == '__main__':
	main()
