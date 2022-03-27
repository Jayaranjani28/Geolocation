
from base64 import encode
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from urllib.parse import urlencode
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element,tostring

api_key = settings.GOOGLE_MAPS_API_KEY

@api_view(['POST'])
def getAddressDetails(request):
    output_format = request.data["output_format"]
    address = request.data
    if output_format == 'json':
        json_data ={}
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{output_format}"
        params = {"address":address,"key":api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        res = requests.get(url)   # Passing url
        latlng = res.json()['results'][0]['geometry']['location'] # Select location field in json format
        data1 = res.json()['results'][0]['formatted_address'] # select Address field in json format
        json_data["coordinates"] = latlng
        json_data['coordinates']['address'] = data1 # Add address data into json_data
        return Response(json_data)
    elif output_format == 'xml':
        xmlDict = {}
        endpoint = f"https://maps.googleapis.com/maps/api/geocode/{output_format}"
        params = {"address":address,"key":api_key}
        url_params = urlencode(params)
        url = f"{endpoint}?{url_params}"
        res = requests.get(url)
        root = res.content # displays data as bytes
        root_string = root.decode() # convert into String
        root1 = ET.fromstring(root_string) # String to xml
        # Iterate each tags and remove unnecessary tags
        for elem in root1.iter():
            for child in list(elem):
                if (child.tag == 'address_component' or child.tag == 'type' or child.tag == 'place_id' or child.tag == 'status' or child.tag == 'location_type' or child.tag == 'viewport' or child.tag == 'bounds' or child.tag == 'partial_match'):
                    elem.remove(child)
        xmlstr = ET.tostring(root1,encoding='utf-8',method='xml') # Changes applied to ElementTree
     
        data = xmlstr.decode()
        data1 = []
        # Removing spaces and newlines and again converts to string
        for x in data:
            data1.append(x.replace("\n",""))
        xml_data = ''.join([str(elem) for elem in data1])
        return Response(xml_data)


    


