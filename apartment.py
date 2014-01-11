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
		return self.street + ' ' + self.city + ', ' + self.state + ' ' + self.zipcode


class Apartment(object):
	def __init__(self, address):
		self._address = address

	@property
	def address(self):
		return self._address

	def __str__(self):
		return str(self.address)
