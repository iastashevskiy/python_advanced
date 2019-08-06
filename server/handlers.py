import json
import logging

from protocol import validate_req
from actions import resolve
from protocol import response
from middlewares import compression_middleware, encryption_middleware

@compression_middleware
@encryption_middleware
def handle_default_request(bytes_request):
		request = json.loads(bytes_request.decode())

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
		return str_res.encode()