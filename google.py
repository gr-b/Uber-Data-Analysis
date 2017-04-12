
import googlemaps
import urllib2

key = 'AIzaSyDVASMakv-4diGu3FRUmh8s3DMtct82ze0'

#Gets the JSON data for a google location
def getData(origin, dest, mode = '', depart_time = ''):
    origin = 'origin=' + origin #start location (name or coords)
    dest = '&destination=' + dest #destination (name or coords)
    #mode = '&mode=' + mode #mode of transportation
    APIKey = '&key=' + key #API key
    #depart_time = '&departure_time=' + depart_time
    url = 'https://maps.googleapis.com/maps/api/directions/json?' + origin + dest + APIKey
    json = urllib2.urlopen(url)
    json = json.read()
    return json

print getData('Montreal', 'Toronto')
