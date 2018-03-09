import argparse
import json
import pprint
import requests
import sys
import urllib
import pandas

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


API_HOST = 'https://maps.googleapis.com/maps/api/place'
API_KEY = 'AIzaSyB64uYpz5jkKuLJsPGNKSRiOzpApaKfNEs'
SEARCH_PATH = '/textsearch/json?'
PLACE_DETAIL_PATH = '/details/json?'


def main():

    #read in Yelp YelpResults
    df = pandas.read_csv('yelp_results.csv')
    exisitng_names = df.name
    existing_latitudes = df.lat
    exisiting_longitudes = df.long
    exisiting_latlongs = zip(exisitng_names, existing_latitudes,exisiting_longitudes)

    # write header line
    with open('google_results_all.csv','w') as f1:
        f1.write('id,lat,long,name,address,word\n')

    with open('google_results_unique.csv','w') as f2:
        f2.write('id,lat,long,name,address,word\n')

    keywords = ['ecig','ecigarette','vape','vapor','vaper','vapin','vaping','electronic+cigarette']

    for word in keywords:
        for lat,lon in LATLONG:
            print("LAT {0} LONG {1}".format(lat,lon))
            try:
                query_api(lat,lon,word,exisiting_latlongs)
            except Exception, e:
                print e


if __name__ == '__main__':
    main()
