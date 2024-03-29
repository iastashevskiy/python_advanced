import zlib
from functools import wraps

def compression_middleware(func):
	@wraps(func)
	def wrapper(request, *args, **kwargs):
		bytes_request = zlib.decompress(request)
		bytes_response = func(request, *args, *kwargs)
		return zlib.compress(bytes_response)
	return wrapper


def encryption_middleware(func):
	@wraps(func)
	def wrapper(request, *args, **kwargs):
		#decrypt request
		bytes_response = func(request, *args, **kwargs)
		#encrypt
		return bytes_response
	return wrapper