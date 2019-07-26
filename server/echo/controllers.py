from protocol import response

def get_echo(request):
	data = request.get('data')
	return response(request, 200, data)