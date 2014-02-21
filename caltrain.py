import datetime


class Caltrain(object):
    """
    Loads the caltrain.csv timetable.
    CSV from https://github.com/alex-hofsteede/caltrain_timetable/blob/master/caltrain-nb.csv
    """
    def __init__(self):
        self._northbound = {}
        self._southbound = {}
        self._cities = []

        with open('caltrain_nb.csv') as f:
            self._cities = f.readline().strip().split(',')[1:]
            self._northbound = {city: {} for city in self._cities}
            for l in f:
                toks = l.strip().split(',')
                train_number = int(toks[0])
                for city, arrival_time in zip(self._cities, toks[1:]):
                    if len(arrival_time) > 0:
                        self._northbound[city][train_number] = self._parse_timestr(arrival_time)
        with open('caltrain_sb.csv') as f:
            cities = f.readline().strip().split(',')[1:]
            self._southbound = {city: {} for city in cities}
            for l in f:
                toks = l.strip().split(',')
                train_number = int(toks[0])
                for city, arrival_time in zip(cities, toks[1:]):
                    if len(arrival_time) > 0:
                        self._southbound[city][train_number] = self._parse_timestr(arrival_time)

    def _parse_timestr(self, s):
        """
        Custom parsing logic to handle 24:02.
        """
        try:
            return datetime.datetime.strptime(s, "%H:%M")
        except:
            newstr = str(int(s[:2]) - 24) + s[2:]
            dt = datetime.datetime.strptime(newstr, "%H:%M")
            return dt + datetime.timedelta(days=1)

    def get_trains(self, city):
        return self._northbound.get(city, [])

    def get_cities(self):
        return self._northbound.keys()

    def get_minimum_duration(self, city_a, city_b):
        """
        Returns the minimum duration from city_a to city_b.
        """
        min_duration = float('inf')
        idx_a = self._cities.index(city_a)
        idx_b = self._cities.index(city_b)
        schedule = self._northbound if idx_a < idx_b else self._southbound
        trains = set(schedule[city_a].keys()) & set(schedule[city_b].keys())

        for train in trains:
            min_duration = min(
                min_duration,
                self._subtract_times(
                    schedule[city_b][train],
                    schedule[city_a][train]
                )
            )

        return min_duration

    def _subtract_times(self, a, b):
        """
        Returns the difference of a - b in minutes.
        """
        td = a - b
        return td.days * 24 * 60 + td.seconds // 60
