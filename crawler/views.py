from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .scraper import findIfJQueryExists


class ListURLDetails(APIView):
    def get(self, request):
        url = request.query_params.get('url', None)
        get_version = request.query_params.get('getversion', None)
        verbose = request.query_params.get('verbose', None)

        if url is not None and url != "":
            data_dict = findIfJQueryExists(url)

            if get_version is not None and get_version == "yes":
                data_dict.pop('found_in_line', None)
                return Response(data_dict)

            elif verbose is not None and verbose == "yes":
                data_dict.pop('version', None)
                return Response(data_dict)

            else:
                data_dict.pop('found_in_line', None)
                data_dict.pop('version', None)
                return Response(data_dict)

        else:
            return Response({"message": "No URL provided"},
                            status=status.HTTP_400_BAD_REQUEST)
