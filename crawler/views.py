from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .scraper import findIfJQueryExists

# Create your views here.
class ListURLDetails(APIView):
	def get(self, request):
		url = request.query_params.get('url', None)
		get_version = request.query_params.get('getversion', None)
		verbose = request.query_params.get('verbose', None)

		if url is not None and url != "":
			data_list = findIfJQueryExists(url) 
			
			if get_version is not None and get_version == "yes":
				if data_list[0]:
					if data_list[1] == 1:
						if data_list[2] is not None:
							data = {"success" : True, "uses_jquery" : "yes", "version" : data_list[2]}
						else:
							data = {"success" : True, "uses_jquery" : "yes", "version" : "could not detect"}	
					elif data_list[1] == 0:
						data = {"success" : True, "uses_jquery" : "maybe", "version" : data_list[2]}
					elif data_list[1] == -1:
						data = {"success" : True, "uses_jquery" : "no", "version" : data_list[2]}	
					return Response(data)
				else:
					data = {"success" : False, "uses_jquery" : "no", "version" : data_list[2]}
					return Response(data)

			if verbose is not None and verbose == "yes":
				if data_list[0]:
					if data_list[1] == 1:
						data = {"success" : True, "uses_jquery" : "yes", "found_in_line" : data_list[3]}
					elif data_list[1] == 0:
						data = {"success" : True, "uses_jquery" : "maybe", "found_in_line" : data_list[3]}
					elif data_list[1] == -1:
						data = {"success" : True, "uses_jquery" : "no", "found_in_line" : data_list[3]}	
					return Response(data)
				else:
					data = {"success" : False, "uses_jquery" : "no", "found_in_line" : data_list[3]}
					return Response(data)		

			if data_list[0]:
				if data_list[1] == 1:
					data = {"success" : True, "uses_jquery" : "yes"}
				elif data_list[1] == 0:
					data = {"success" : True, "uses_jquery" : "maybe"}
				elif data_list[1] == -1:
					data = {"success" : True, "uses_jquery" : "no"}	
				return Response(data)
			else:
				data = {"success" : False, "uses_jquery" : "no"}
				return Response(data)

		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)			 
