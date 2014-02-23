class Address(object):
    def __init__(self, street, city, state, zipcode):
        self._street = street
        self._city = city
        self._state = state
        self._zipcode = zipcode

    @property
    def street(self):
        return self._street

    @property
    def city(self):
        return self._city

    @property
    def state(self):
        return self._state

    @property
    def zipcode(self):
        return self._zipcode

    def __str__(self):
        return self.street + ' ' + self.city + ', ' + self.state + ' ' \
            + self.zipcode

    def __eq__(self, o):
        return self.street == o.street and self.city == o.city and \
            self.state == o.state and self.zipcode == o.zipcode

    def __hash__(self):
        return str(self).__hash__()


class Apartment(object):
    def __init__(self, name, link, address):
        self._name = name
        self._link = link
        self._address = address

    @property
    def name(self):
        return self._name

    @property
    def link(self):
        return self._link

    @property
    def address(self):
        return self._address

    def __str__(self):
        return "\n".join([self.name, self.link, str(self.address)])

    def __eq__(self, o):
        return self.address == o.address

    def __hash__(self):
        return str(self).__hash__()
