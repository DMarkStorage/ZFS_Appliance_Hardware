import requests
import json
import os
import traceback
from docopt import docopt
from prettytable import PrettyTable
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
		Hardware_Details.py -s <STORAGE> --diag
		Hardware_Details.py --version
		Hardware_Details.py -h | --help

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
			'/hardware/v1/cluster', 
			'/system/v1/disks',
			'/system/v1/memory',
			'/storage/v1/pools',
			'/network/v1/routes', 
			'/service/v1/services',
			'/system/v1/updates', 
			'/system/v1/version', 
  
			]

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

	with open('output.json', 'w') as outfile:
		json.dump(data, outfile, indent = 2)

def get_val():


	def get_cluster():
		t = PrettyTable()
		print('\n')
		print('+'+'-'*30+'+')
		print('  *** Cluster DETAILS***\n')	
		t.field_names = [
		'Name',
		'Status',
		'Details'
		]

		t.add_row(
			[('Cluster Enabled'),
			data['cluster']['state'],
			data['cluster']['description']
			]
			)
		print(t)

	def get_disk():

		def con_mb(mb):
			gb = (mb/1024)

			if gb > 100:
				pb = (gb/1.126e+6)

				out = str("{:.2f}".format(pb))+" Pib"
				return out
			else:
				out = str("{:.2f}".format(gb))+" Gib"
				return out

		root = con_mb(data['disks']['root'])
		var = con_mb(data['disks']['var'])
		update = con_mb(data['disks']['update'])
		stash = con_mb(data['disks']['stash'])
		dump = con_mb(data['disks']['dump'])
		cores = con_mb(data['disks']['cores'])
		free = con_mb(data['disks']['free'])

		t = PrettyTable()
		print('\n')
		print('+'+'-'*30+'+')
		print('  *** DISK DETAILS***\n')	
		t.field_names = [
		'Profile',
		'Root',
		'Var',
		'Update',
		'Stash',
		'Dump',
		'Cores',
		'Free'
		]

		t.add_row(
			[
			data['disks']['profile'],
			root,
			var,
			update,
			stash,
			dump,
			cores,
			free,
			]
			)
		print(t)

	def get_memory():

		def con_mb(mb):
			gb = (mb/1024)

			if gb > 100:
				pb = (gb/1.126e+6)

				out = str("{:.2f}".format(pb))+" Pib"
				return out
			else:
				out = str("{:.2f}".format(gb))+" Gib"
				return out

		cache = con_mb(data['memory']['cache'])
		unused = con_mb(data['memory']['unused'])
		management = con_mb(data['memory']['management'])
		other = con_mb(data['memory']['other'])
		kernel = con_mb(data['memory']['kernel'])

		t = PrettyTable()
		print('\n')
		print('+'+'-'*30+'+')
		print('  *** MEMORY ***\n')
		t.field_names = [
		'Cache',
		'Unused',
		'Management',
		'other',
		'kerne',
		]

		t.add_row(
			[
			cache,
			unused,
			management,
			other,
			kernel,
			]
			)
		print(t)


	def get_pool():

		def con_mb(mb):
			gb = (mb/1024)

			if gb > 100:
				pb = (gb/1.126e+6)

				out = str("{:.2f}".format(pb))+" Pib"
				return out
			else:
				out = str("{:.2f}".format(gb))+" Gib"
				return out

		if len(data['pools']) == 1:
			t = PrettyTable()
			d = data['pools']
			c = len(d[0]['name'])
			s = len(d[0]['status'])
			total = con_mb(d[0]['usage']['total'])
			available = con_mb(d[0]['usage']['available'])
			used = con_mb(d[0]['usage']['used'])
			Dedup = d[0]['usage']['dedupsize']

			print('\n')
			print('+'+'-'*30+'+')
			print('  *** POOL DETAILS***\n')
			t.field_names = [
				'Pool',
				'State',
				'Version',
				'Total',
				'Used',
				'Available',
				'Dedup',
				]
			t.add_row(
			[
			d[0]['name'],
			d[0]['status'],
			d[0]['owner'],
			total,
			used,
			available,
			Dedup,
			]
			)
			print(t)

			print('\n')

		else:
			pass

	def get_route():
		
		t = PrettyTable()

		print('\n')
		print('+'+'-'*30+'+')
		print('  *** Additional Information***\n')
		t.field_names = [
			'ROUTE',
			'DESTINATION',
			'GATEWAY',
			'INTERFACE',
			'TYPE',
			'STATUS',
		]

		e = 0
		for i in data['routes']:
			des = len(i['destination'])
			gate = len(i['gateway'])
			face = len(i['interface'])
			types = len(i['type'])
			stat = len(i['status'])
			route = ('route-00'+str(e))
			t.add_row(
			[	
				route,
				i['destination'],
				i['gateway'],
				i['interface'],
				i['type'],
				i['status']

			]
			)
			e+=1

		print(t)


	def get_services():
		t = PrettyTable()
		print('\n')
		print('+'+'-'*50+'+')
		print(' '*17+'*** SERVICES ***\n')
		t.field_names = [
			'Name',
			'Status',
			'Details',

		]

		for i in data['services']:
			t.add_row(
			[	
				i['name'],
				i['<status>'],
				' '
			]
			)
		print(t)


	def get_updates():
		t = PrettyTable()
		print('\n')
		print('+'+'-'*30+'+')
		print(' '*10+'*** UPDATES ***\n')
		t.field_names = [
			'Name',
			'Version',
			'Status',

		]

		t.add_row(
			[	
				data['updates'][0]['release_name'],
				data['updates'][0]['version'],
				data['updates'][0]['status']
			]
			)
		print(t)


	def get_version():
		t = PrettyTable()

		print('\n')
		print('+'+'-'*30+'+')
		print('  *** General Information***\n')

		t.field_names = [
			'Product Name',
			'Version',
			'Asn',
			'Csn',
			'part Name',
			'ak_version',
			'os_version',
			'bios_version'
		]

		if len(data['version']['version']) >= 20:
			version = str(data['version']['version'][:20])+"\n"+str(data['version']['version'][21:])

		# if len(data['version']['asn']) >= 20:
		# 	asn = str(data['version']['asn'][:20])+"\n"+str(data['version']['asn'][21:])
		
		asn1 = ""
		for i, letter in enumerate(data['version']['asn']):
		    if i % 20 == 0:
		        asn1 += '\n'
		    asn1 += letter

		asn = asn1[1:] 

		csn = ""
		for i, letter in enumerate(data['version']['csn']):
		    if i % 20 == 0:
		        csn += '\n'
		    csn += letter

		csn = csn[1:] 

		part = ""
		for i, letter in enumerate(data['version']['part']):
		    if i % 20 == 0:
		        part += '\n'
		    part += letter

		part = part[1:] 

		ak_version = ""
		for i, letter in enumerate(data['version']['ak_version']):
		    if i % 20 == 0:
		        ak_version += '\n'
		    ak_version += letter

		ak_version = ak_version[1:] 

		os_version = ""
		for i, letter in enumerate(data['version']['os_version']):
		    if i % 20 == 0:
		        os_version += '\n'
		    os_version += letter

		os_version = os_version[1:]

		bios_version = ""
		for i, letter in enumerate(data['version']['bios_version']):
		    if i % 20 == 0:
		        bios_version += '\n'
		    bios_version += letter

		bios_version = bios_version[1:]

		t.add_row(
			[	
				data['version']['product'],
				version,
				asn,
				csn,
				part,
				ak_version,
				os_version,
				bios_version
			]
			)
		print(t)


	get_updates()
	get_services()
	get_route()
	get_pool()
	get_memory()
	get_disk()
	get_cluster()
	get_version()


def main(args):
	storage = args['<STORAGE>']
	get_data(storage)
	get_val()


if __name__ == '__main__':
	try:
		ARGS = get_args()

		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except Exception:
	    ETRACE = traceback.format_exc()
	    print(ETRACE)