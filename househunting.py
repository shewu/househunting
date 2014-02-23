import apartmentscom
import apartmentguide
import caltrain

import googlemaps


c = caltrain.Caltrain()
gmaps = googlemaps.GoogleMaps('AIzaSyBHMOZfCCSElPKRh7ub4FAiXWnuGarO5Mo')


class Result(object):
    def __init__(self, dist=float('inf'), duration=float('inf')):
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
        self._min_caltrain_ride_duration = c.get_minimum_duration(
            self._apartment.address.city,
            'San Francisco'
        )

    def eval(self):
        return self.result_caltrain.duration**2 \
            * self.result_apple.duration \
            * self._min_caltrain_ride_duration

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
            + "  caltrain ride: %f" % self._min_caltrain_ride_duration + "\n" \
            + "  to caltrain: %s" % self.result_caltrain + "\n" \
            + "  to apple: %s" % self.result_apple + "\n"


def meters_to_miles(meters):
    return int(meters) / 1600.


def seconds_to_minutes(seconds):
    return int(seconds) / 60.


def calculate_directions(start, end):
    try:
        directions = gmaps.directions(start, end, mode='transit')
        return Result(
            dist=meters_to_miles(
                directions['Directions']['Distance']['meters']
            ),
            duration=seconds_to_minutes(
                directions['Directions']['Duration']['seconds']
            )
        )
    except Exception, e:
        print "Couldn't get directions from %s to %s" % (start, end)
        return Result()


def to_caltrain_station(address, city):
    start = address
    end = city + ' caltrain station'
    return calculate_directions(start, end)


def to_apple(address):
    return calculate_directions(address, '1 infinite loop 95014')


def to_derpbox(address):
    return calculate_directions(address, '185 berry st san francisco')


def apts_in(city):
    apartments = set(
        apartmentscom.search_city(city)
        + apartmentguide.search_city(city)
    )
    caltrain_stop = '%s caltrain station' % city

    metrics = []

    metrics = [
        MetricsResults(
            apartment=apartment,
            result_caltrain=to_caltrain_station(apartment.address, city),
            result_apple=to_apple(apartment.address)
        )
        for apartment in apartments
    ]

    return metrics


def googlemaps_example():
    """
    Simple demonstration and reference of googlemaps package.
    """
    # documentation: http://py-googlemaps.sourceforge.net/
    start = '3 ames street 02142'
    end = '465 bolivar st 02021'

    # XXX testing kwargs -- they don't work
    directions = gmaps.directions(
        start,
        end,
        kwargs={
            'mode': 'transit',
            'avoid': 'highways',
            'units': 'imperial'
        }
    )
    route = directions['Directions']['Routes'][0]
    for step in route['Steps']:
        print step['descriptionHtml']


def main():
    all_results = apts_in('san mateo') \
        + apts_in('redwood city') \
        + apts_in('burlingame') \
        + apts_in('south san mateo') \
        + apts_in('redwood shores') \
        + apts_in('belmont') \
        + apts_in('foster city') \
        + apts_in('san carlos') \
        + apts_in('millbrae') \
        + apts_in('san bruno')

    for result in sorted(all_results, key=lambda mr: mr.eval()):
        print result

if __name__ == '__main__':
    main()
