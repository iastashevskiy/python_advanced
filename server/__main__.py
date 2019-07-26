from argparse import ArgumentParser
import socket
import yaml
import json
from protocol import validate_req, response
from actions import resolve



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


host, port = config.get('host'),config.get('port')
try:
	sock = socket.socket()
	sock.bind((host, port))
	sock.listen(5)
	print(f'Server started with {host}: {port}')

	while True:
		client, address = sock.accept()
		print(f'Client{address[0]}:{address[1]}')

		b_request = client.recv(config.get('buffersize'))

		request = json.loads(b_request.decode())

		if validate_req(request):

			action_name = request.get('action')
			controller = resolve(action_name)
			
			if controller:	
				try:
					print('Request valid', request)
					response = controller(request)
				except Exception as error:
					print('Internal error', error)
					response = request(request, 500, 'Internal error')
			else: 
				print('Invalid action name: ', action_name)
				response = response(request, 404,'Action not found')

		else:
			print('Request invalid', request)
			response = response(request, 404, 'Invalid request')
			
		str_res = json.dumps(response)
		client.send(str_res.encode())


except KeyboardInterrupt:
	print('Server shutdown')