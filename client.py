from argparse import ArgumentParser
import socket
import yaml

parser =ArgumentParser()

parser.add_argument('-c', '--config', type = str, required = false, help = 'Config file path')

args = parser.parse_args()

config = {
	'host':'localhost',
	'port': 7777
	'buffersize': 1024
}

if args.config:
	with open(args.config) as file:
		file_config = yaml.load(file, Loader = yaml.loader)
		config.update(file_config)


try:
	sock = socket.socket()
	sock.connect((host, port))

	req = input('Enter request: ')
	sock.send(req.encode())

	print('Request sent', req)
	b_response = sock.recv(config.get('buffersize'))

	print('Response received', b_response)
except KeyboardInterrupt:
	print('Client shutdown')