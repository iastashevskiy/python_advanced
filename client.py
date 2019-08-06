from argparse import ArgumentParser
import socket
import yaml
import json
from datetime import datetime
import zlib


WRITE_MODE = 'write'
READ_MODE = 'read'

def make_request(sock, action, data):
	request = {
		'action': action,
		'time': datetime.now().timestamp(),
		'data': data,
	}

parser =ArgumentParser()

parser.add_argument('-c', '--config', type = str, required = False, help = 'Config file path')

parser.add_argument(
		'-n', '--mode', type = str, default = WRITE_MODE,
		help = 'Set client mode'
	)

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

	while True:
		if args.mode == WRITE_MODE:
			action = input('Enter action needed: ')
			data = input('Enter request: ')

			request = make_request(action, data)
			str_request = json.dumps(request)

			bytes_request = zlib.compress(str_request.encode())

			sock.send(bytes_request)


			print('Request sent: ', request)
		elif args.mode == READ_MODE:
			response = sock.recv(config.get('buffersize'))
			bytes_response = zlib.decompress(response)

			print('Response received', bytes_response)

			
except KeyboardInterrupt:
	print('Client shutdown')