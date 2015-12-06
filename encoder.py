import csv
import json
import sys

sys.path.append('.')
import geocoder

def create_config(filename):
	f = open(filename)
	reader = csv.reader(f)
	columns = reader.next()
	f.close()

	fields = {}

	for column in columns:
		if not column:
			continue
		if fields.has_key(column):
			if not fields[column].has_key('array'):
				fields[column]['array'] = 1
		else:
			field = '_'.join(column.lower().split())
			fields[column] = {'field': field, 'type': 'string'}

	config = {'fields': fields, 'aggregate': []}
	outfile = open('config.json', 'w')
	json.dump(config, outfile, indent=4)
	outfile.close()

def parse(filename):
	# read in configuration
	with open('config.json') as infile:
		config = json.load(infile)

	fields = config['fields']

	gc = geocoder.Geocoder()

	# Place to store things	
	data = []

	# start processing the file
	with open(filename) as infile:
		reader = csv.reader(infile)
		# read in columns
		columns = reader.next()

		# Go through the others, and map things out
		for row in reader:
			parsed = {}
			for i in range(len(columns)):
				column = columns[i]
				value = row[i]
				if fields.has_key(column):
					cfg = fields[column]
					field = cfg['field']
					if cfg.has_key('geocode'):
						parsed['_point'] = gc.geocode(value)
					if cfg['type'] == 'int':
						value = int(value)
					if cfg.has_key('array'):
						if value:
							if parsed.has_key(field):
								parsed[field].append(value)
							else:
								parsed[field] = [value]
					else:
						parsed[field] = value
			data.append(parsed)
		with open('data.json', 'w') as outfile:
			json.dump(data, outfile)


if __name__ == '__main__':
	parse('2015CURRENT.csv')