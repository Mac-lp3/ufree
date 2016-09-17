import json
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.view import view_config

def put_date_range(request):
	"""
	Update an existing date rang in this eventLanding

	If this eventLanding has existing date ranges, this will update
	the one with the correspodning composite id.
	"""

	return Response("Ya dang put")

def delete_date_range(request):
	"""
	Delete an existing date rang in this eventLanding

	If this eventLanding has existing date ranges, this will delete
	the one with the correspodning composite id.
	"""

	return Response("Ya dang del")

def post_date_range(request):
	"""
	Create a date rang in this eventLanding

	This will create a new date range with a generated composite id
	for this eventLanding.
	"""

	try: 
		postData = request.json_body
		print(postData);
	except json.decoder.JSONDecodeError:
		raise HTTPBadRequest

	postData = request.json_body

	return Response("Ya dang post")

def includeme(config):
	config.add_route('eventLanding', '/api/event/{hashId}')
	config.add_renderer('eventLanding', 'pyramid.renderers.json_renderer_factory')
	config.add_view(put_date_range, route_name='eventLanding', request_method="PUT")
	config.add_view(post_date_range, route_name='eventLanding', request_method="POST")
	config.add_view(delete_date_range, route_name='eventLanding', request_method="DELETE")


