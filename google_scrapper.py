from math import cos, asin, sqrt
import argparse
import json
import pprint
import requests
import sys
import urllib
import pandas
import time

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


API_HOST = 'https://maps.googleapis.com/maps/api/place/'
API_KEY = 'AIzaSyB64uYpz5jkKuLJsPGNKSRiOzpApaKfNEs'
SEARCH_PATH = 'textsearch/json?'
PLACE_DETAIL_PATH = '/details/json?'  # Business ID will come after slash.
LATLONG = [(42,-124),(42,-123),(42,-122),(42,-121),(42,-120),
           (41,-124),(41,-123),(41,-122),(41,-121),(41,-120),
           (40,-124),(40,-123),(40,-122),(40,-121),(40,-120),
                     (39,-123),(39,-122),(39,-121),(39,-120),
                     (38,-123),(38,-122),(38,-121),(38,-120),(38,-119),
                               (37,-122),(37,-121),(37,-120),(37,-119),(37,-118),(37,-117),
                               (36,-122),(36,-121),(36,-120),(36,-119),(36,-118),(36,-117),(36,-116),
                                                   (35,-120),(35,-119),(35,-118),(35,-117),(35,-116),(35,-115),
                                                             (34,-119),(34,-118),(34,-117),(34,-116),(34,-115),
                                                                       (33,-118),(33,-117),(33,-116),(33,-115)]
RADIUS = 50000
D = {}
YelpResults = {}


# query=123+main+street&location=42.3675294,-71.186966&radius=10000&key=YOUR_API_KEY

def request(host, path, url_params, nextpage = None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, path)

    if nextpage is None:
        url_params = url_params or {}
        url = '{0}location={2}&radius={3}&key={4}&query={1}'.format(url,url_params['query'],url_params['location'],url_params['radius'],url_params['key'])
    else:
        time.sleep(3)
        url ="{0}key={1}&pagetoken={2}".format(url,url_params,nextpage)

    response = requests.request('GET',url)

    return response.json()

def search(word,api_key, lat, lon, radius):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'query': word,
        'location': '{0},{1}'.format(lat,lon),
        'radius': radius,
        'key': api_key
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def query_api(lat, lon, word, compare):
    """Queries the API by the input values from the user.
    Args:
        zip_code (str): The zip_code of the business to query.
    """
    response = search(word,API_KEY, lat, lon, RADIUS)

    while True:

        businesses = response.get('results')

        dis = 0

        print('{3} businesses for {0} in {1},{2} found.'.format(word,lat,lon,len(businesses)))

        with open('google_results_unique.csv','a') as u:
            with open('google_results_all.csv','a') as a:
                for business in businesses:
                    if 'CA' in business['formatted_address']:
                        if business['place_id'].encode('utf-8').strip() not in D:
                            D[business['place_id'].encode('utf-8').strip()] = 1
                            results = {
                                'id':business['place_id'].encode('utf-8').strip(),
                                'lat':business['geometry']['location']['lat'],
                                'long':business['geometry']['location']['lng'],
                                'name':business['name'].encode('utf-8').strip(),
                                'address':business['formatted_address'].encode('utf-8').strip().replace(',',''),
                                'category':word.encode('utf-8').strip()
                                }
                            line = '{id},{lat},{long},{name},{address},{category}\n'.format(**results)

                            for name, la, lo in compare:
                                if(la == 'None' or lo == 'None' or business['geometry']['location']['lat']== 'None' or  business['geometry']['location']['lng']== 'None'):
                                    continue

                                dis = abs(distance(la,lo,business['geometry']['location']['lat'],business['geometry']['location']['lng']))
                                if(name == business['name'] and dis <= 1):
                                    a.write(line)
                                    break

                                if dis <= 0.07:
                                    a.write(line)
                                    break
                            if dis > 0.7:
                                print "****************"
                                print line
                                print  "****************"
                                a.write(line)
                                u.write(line)

            if 'next_page_token' not in response:
                break


            response = request(API_HOST, SEARCH_PATH,API_KEY,response.get('next_page_token'))




def distance(lat1, lon1, lat2, lon2):
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin...

def main():
    nextpageremember = "hi"

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
