from argparse import ArgumentParser
import socket
import yaml
import json
from protocol import validate_req, response
from actions import resolve
import logging
from handlers import handle_default_request
import select



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
	level = logging.DEBUG,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers = [
		logging.FileHandler('main.log'),
		logging.StreamHandler()
	]

)

requests = []
connections = []

host, port = config.get('host'),config.get('port')

try:
	sock = socket.socket()
	sock.bind((host, port))
	sock.setblocking(False)
	sock.settimeout(0)
	sock.listen(5)
	logging.info(f'Server started with {host}: {port}')

	while True:
		try:
			client, address = sock.accept()
			logging.info(f'Client {address[0]}:{address[1]}')
			connections.append(client)
		except:
			pass

		rlist, wlist, xlist = select.select(
			connections, connections, connections, 0
			)

		for read_client in rlist:
			bytes_request = read_client.recv(config.get('buffersize'))
			requests.append(bytes_request)


		if requests:
			bytes_request = requests.pop()
			bytes_response = handle_default_request(bytes_request)
			for write_client in wlist:
				write_client.send(bytes_response)


except KeyboardInterrupt:
	print('Server shutdown')