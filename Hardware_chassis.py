import requests
import json
import os
import traceback
from docopt import docopt
from prettytable import PrettyTable
import csv
requests.packages.urllib3.disable_warnings()

__version__ = '1.0'
__revision__ = '20190626'
__deprecated__ = False

data = {}
def get_headers():
	# Function that will return the headers and the Auth for the API
	headers = {
		"Content-Type":"application/json",
		"X-Auth-User": 'root',
		"X-Auth-Key": 'password'

	}
	return headers

def get_args():

	usage = """
	Usage:
		Hardware_chassis.py -s <STORAGE> -d 
		Hardware_chassis.py -s <STORAGE> -d --csv <FILENAME>
		Hardware_chassis.py -s <STORAGE> -d --csv <FILENAME> --json <JSON_FN>
		Hardware_chassis.py --version
		Hardware_chassis.py -h | --help

	Options:
		-h --help            Show this message and exit
		-s <STORAGE>         ZFS appliance/storage name

	"""
	# version = '{} VER: {} REV: {}'.format(__program__, __version__, __revision__)
	# args = docopt(usage, version=version)
	args = docopt(usage)
	return args	


def api_list():

	url = [	
			'/hardware/v1/chassis',]

	return url


def get_data(storage):

	header = get_headers()
	base_url = 'https://{}:215'.format(storage)
	
	url = api_list()

	for i in url:
		ch1_uri = '{}/api'.format(base_url)+i
		r = requests.get(ch1_uri, verify=False, headers = header)
		j = r.json()
		data.update(j)


def get_val(args):

	def get_chassis(args):
		print('\n')
		print('+'+'-'*30+'+')
		print('  *** CHASSIS INFORMATION ***\n')
		table = PrettyTable()
		for i in data['chassis']:
			table.field_names = ["Name","Faulted","Manufacturer",
							"model","Part","Type","RPM","Path",
							"Serial","HREF"]

			if 'part' in i:
				part = i['part']
			else:
				part = " "

			if 'rpm' in i:
				rpm = i['rpm']
			else:
				rpm = " "
			if 'path' in i:
				path = i['path']
			else:
				path = " "
			if 'href' in i:
				hr = i['href']
			else:
				hr = " "


			table.add_row([i['name'],i['faulted'],i['manufacturer'],i['model']
				,part,i['type'],rpm,path,i['serial'][:30]+"\n"+i['serial'][30:],hr])


			print(table)
		if not args['--json']:
			out_csv(args['<FILENAME>'])

		elif args['--json']:
			out_csv(args['<FILENAME>'])
			out_json(args['<JSON_FN>'])


	get_chassis(args)
def out_csv(fl):
	datafs={}
	filename = str(fl)+'.csv'


	datafs = data['chassis']
	data_file = open(filename, 'w')
	csv_ = csv.writer(data_file)

	c = 0
	for item in data['chassis']:
		if c == 0:
			header = item.keys()
			csv_.writerow(header)
			c +=1

		csv_.writerow(item.values())
	data_file.close()

def out_json(fl):
	filename = str(fl)+'.json'
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, indent = 2)

def main(args):
	storage = args['<STORAGE>']
	get_data(storage)
	get_val(args)



if __name__ == '__main__':
	try:
		ARGS = get_args()

		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except Exception:
	    ETRACE = traceback.format_exc()
	    print(ETRACE)
	except KeyError:
		print("data")