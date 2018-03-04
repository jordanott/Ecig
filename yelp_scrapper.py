# -*- coding: utf-8 -*-
import argparse
import json
import pprint
import requests
import sys
import urllib
from keys import API_KEY

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
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


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'vape'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 50

D={}

def request(host, path, api_key, url_params=None):
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
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, location):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        #'term': 'ecig+ecigarette+vape+vapor+vaper+vapin+vaping+electronic+cigarette',
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'categories': 'vapeshops'
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(zip_code):
    """Queries the API by the input values from the user.
    Args:
        zip_code (str): The zip_code of the business to query.
    """
    response = search(API_KEY, zip_code)
    #print response
    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for __ in {1} found.'.format(zip_code))
        return

    print zip_code, len(businesses)

    with open('yelp_results.csv','a') as f:
        for business in businesses:
            if business['id'].encode('utf-8').strip() not in D:
                if not business['is_closed']:
                    D[business['id'].encode('utf-8').strip()] = 1
                    categories = ''
                    for cat_dict in business['categories']:
                        categories += cat_dict['alias'] + ' '
                    results = {
                        'id':business['id'].encode('utf-8').strip(),
                        'lat':business['coordinates']['latitude'],
                        'long':business['coordinates']['longitude'],
                        'name':business['name'].encode('utf-8').strip(),
                        'address':u' '.join(business['location']['display_address']).encode('utf-8').strip().replace(',',''),
                        'category':categories.encode('utf-8').strip(),
                        'zip':zip_code.encode('utf-8').strip(),
                        'phone':business['phone'].encode('utf-8').strip(),
                        'closed':business['is_closed']
                        }
                    line = '{id},{lat},{long},{name},{address},{category},{zip},{phone},{closed}\n'.format(**results)
                    f.write(line)


def main():
    # write header line
    with open('yelp_results.csv','w') as f:
        f.write('id,lat,long,name,address,category,zip,phone,closed\n')

    # read zip codes file
    zip_codes = open('CA_ZIPCODES.csv')
    # skip header line
    zip_codes.next()
    for line in zip_codes:
        zip_code = line.strip()
        try:
            query_api(zip_code)
        except Exception, e:
            print e


if __name__ == '__main__':
    main()
