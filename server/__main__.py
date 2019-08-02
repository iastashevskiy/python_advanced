from argparse import ArgumentParser
import socket
import yaml
import json
from protocol import validate_req, response
from actions import resolve
import logging



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

# logger = logging.getLogger('main')
# formatter = logging.formatter('%(asctime)s - %(levelname)s - %(message)s')

# file_handler = logging.FileHandler('main.log')
# stream_handler = logging.StreamHandler()
# file_handler.setlevel(logging.DEBUG)
# stream_handler.setlevel(logging.DEBUG)

# file_handler.setformatter(formatter)
# stream_handler.setformatter(formatter)

# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)
# logger.setlevel(logging.DEBUG)

logging.basicConfig(
	level = logging.DEBUG
	format = '%(asctime)s - %(levelname)s - %(message)s'
	handlers = [
		logging.FileHandler('main.log'),
		logging.StreamHandler()
	]

)


host, port = config.get('host'),config.get('port')

try:
	sock = socket.socket()
	sock.bind((host, port))
	sock.listen(5)
	logging.info(f'Server started with {host}: {port}')

	while True:
		client, address = sock.accept()
		logging.info(f'Client{address[0]}:{address[1]}')

		b_request = client.recv(config.get('buffersize'))

		request = json.loads(b_request.decode())

		if validate_req(request):

			action_name = request.get('action')
			controller = resolve(action_name)
			
			if controller:	
				try:
					logging.info('Request valid', request)
					response = controller(request)
				except Exception as error:
					logging.critical('Internal error', error)
					response = request(request, 500, 'Internal error')
			else: 
				logging.error('Invalid action name: ', action_name)
				response = response(request, 404,'Action not found')

		else:
			logging.error('Request invalid', request)
			response = response(request, 404, 'Invalid request')
			
		str_res = json.dumps(response)
		client.send(str_res.encode())


except KeyboardInterrupt:
	print('Server shutdown')