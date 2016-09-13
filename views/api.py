from pyramid.response import Response
from pyramid.view import view_config

def put_date_range(request):
	"""
	Update an existing date rang in this hashLanding

	If this hashLanding has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	return Response("Ya dang put")

def delete_date_range(request):
	"""
	Delete an existing date rang in this hashLanding

	If this hashLanding has existing date ranges, this will delete
	the one with the correspodning composite id.
	"""

	return Response("Ya dang del")

def post_date_range(request):
	"""
	Create a date rang in this hashLanding

	This will create a new date range with a generated composite id
	for this hashLanding.
	"""

	return Response("Ya dang post")

def includeme(config):
	config.add_route('hashLanding', '/api/{hashId}')
	config.add_view(put_date_range, route_name='hashLanding', request_method="PUT")
	config.add_view(post_date_range, route_name='hashLanding', request_method="POST")
	config.add_view(delete_date_range, route_name='hashLanding', request_method="DELETE")
	"""config.add_view(post_date_range, route_name='hashLanding')"""