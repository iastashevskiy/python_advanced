from argparse import ArgumentParser
import socket
import yaml
import json
from datetime import datetime

parser =ArgumentParser()

parser.add_argument('-c', '--config', type = str, required = False, help = 'Config file path')

args = parser.parse_args()

config = {
	'host':'localhost',
	'port': 8000,
	'buffersize': 1024
}

if args.config:
	with open(args.config) as file:
		file_config = yaml.load(file, Loader = yaml.loader)
		config.update(file_config)

host, port = config.get('host'), config.get('port')

try:
	sock = socket.socket()
	sock.connect((host, port))

	action = input('Enter action needed: ')
	data = input('Enter request: ')
	request = {
		'action': action,
		'time': datetime.now().timestamp(),
		'data': data,
	}

	str_request = json.dumps(request)

	sock.send(str_request.encode())
	print('Request sent: ', request)

	b_response = sock.recv(config.get('buffersize'))

	print('Response received', b_response)
except KeyboardInterrupt:
	print('Client shutdown')