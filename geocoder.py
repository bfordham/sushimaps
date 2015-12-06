import anydbm
import json
from urllib import urlencode
import urllib2

class Geocoder:
	URL = 'https://maps.googleapis.com/maps/api/geocode/json?'

	def __init__(self):
		self.cache = anydbm.open('cache.db', 'c')

	def geocode(self, location):
		# normalize
		normalized = ' '.join(location.upper().split())

		point = False
		# do we have it already?
		if self.cache.has_key(normalized):
			point = json.loads(self.cache[normalized])
		else:
			params = urlencode({'address': normalized})
			url = "%s%s" % (self.URL, params)
			data = json.load(urllib2.urlopen(url))
			if len(data['results']) > 0:
				point = data['results'][0]['geometry']['location']
				point['label'] = location
				self.cache[normalized] = json.dumps(point)
		return point

	def close(self):
		self.cache.close()
