from protocol import response
from decorators import logged

@logged
def get_echo(request):
	data = request.get('data')
	return response(request, 200, data)