from argparse import ArgumentParser
import socket
import yaml

parser =ArgumentParser()

parser.add_argument('-c', '--config', type = str, required = false, help = 'Config file path')

args = parser.parse_args()

config = {
	'host':'localhost',
	'port': 7777,
	'buffersize': 1024
}

if args.config:
	with open(args.config) as file:
		file_config = yaml.load(file, Loader = yaml.loader)
		config.update(file_config)


host, port = config.get('host'),config.get('port')

try:
	sock = socket.socket()
	sock.bind(host, port)
	sock.listen(5)
	print('Server started with', host, port)

	while True:
		client, address = sock.accept()
		print(f'Client{address[0]}:{address[1]}')

		b_request = client.recv(config.get('buffersize'))
		print(f'Client message: {b_request.decode()}')
		client.send(b_request)
		client.close()

except KeyboardInterrupt:
	print('Server shutdown')