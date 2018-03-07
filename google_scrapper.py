import argparse
import json
import pprint
import requests
import sys
import urllib

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
PLACE_DETAIL_PATH = '/details/json?'  # Business ID will come after slash.
LATLONG = [(42,124),(42,123),(42,122),(42,121),(42,120),
           (41,124),(41,123),(41,122),(41,121),(41,120),
           (40,124),(40,123),(40,122),(40,121),(40,120),
                    (39,123),(39,122),(39,121),(39,120),
                    (38,123),(38,122),(38,121),(38,120),(38,119),
                             (37,122),(37,121),(37,120),(37,119),(37,118),(37,117),
                             (36,122),(36,121),(36,120),(36,119),(36,118),(36,117),(36,116),
                                               (35,120),(35,119),(35,118),(35,117),(35,116),(35,115),
                                                        (34,119),(34,118),(34,117),(34,116),(34,115),
                                                                 (33,118),(33,117),(33,116),(33,115)]
RADIUS = 50000

D = {}
YelpResults = {}


# query=123+main+street&location=42.3675294,-71.186966&radius=10000&key=YOUR_API_KEY

def request(host, path, url_params=None):
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
    url_params = url_params or {}
    url = '{0}{1}'.format(host, path)
    url = '{0}query={1}&location={2}&radius={3}&key={4}'.format(url,url_params['query'],url_params['location'],url_params['radius'],url_params['key'])
    print url

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url)

    return response.json()

def search(api_key, lat, lon, radius):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'query': 'ecig',
        'location': '{0},{1}'.format(lat,lon),
        'radius': radius,
        'key': api_key
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def query_api(lat, lon):
    """Queries the API by the input values from the user.
    Args:
        zip_code (str): The zip_code of the business to query.
    """
    response = search(API_KEY, lat, lon, 80000)
    #print response
    businesses = response.get('results')

    for business in businesses:
        print("Name: {0} ID: {1} Types: {2}".format(business['name'],business['id'],business['types']))

    # if not businesses:
    #     print(u'No businesses for __ in {1} found.'.format(zip_code))
    #     return
    #
    # print zip_code, len(businesses)
    #
    # with open('yelp_results.csv','a') as f:
    #     for business in businesses:
    #         if business['id'].encode('utf-8').strip() not in D:
    #             if not business['is_closed']:
    #                 D[business['id'].encode('utf-8').strip()] = 1
    #                 categories = ''
    #                 for cat_dict in business['categories']:
    #                     categories += cat_dict['alias'] + ' '
    #                 results = {
    #                     'id':business['id'].encode('utf-8').strip(),
    #                     'lat':business['coordinates']['latitude'],
    #                     'long':business['coordinates']['longitude'],
    #                     'name':business['name'].encode('utf-8').strip(),
    #                     'address':u' '.join(business['location']['display_address']).encode('utf-8').strip().replace(',',''),
    #                     'category':categories.encode('utf-8').strip(),
    #                     'zip':zip_code.encode('utf-8').strip(),
    #                     'phone':business['phone'].encode('utf-8').strip(),
    #                     'closed':business['is_closed']
    #                     }
    #                 line = '{id},{lat},{long},{name},{address},{category},{zip},{phone},{closed}\n'.format(**results)
    #                 f.write(line)

def main():
    # write header line
    with open('google_results.csv','w') as f:
        f.write('id,lat,long,name,address,zip,phone,closed\n')

    query_api(34.0522,-118.2437)

    # for lat,lon in LATLONG:
    #     print("LAT {0} LONG {1}".format(lat,lon))
    #     try:
    #         query_api(lat,lon)
    #     except Exception, e:
    #         print e


if __name__ == '__main__':
    main()
