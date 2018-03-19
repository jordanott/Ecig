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
PLACE_DETAIL_PATH = '/details/json?'

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
    url = '{0}placeid={1}&key={2}'.format(url,url_params['id'],url_params['key'])
    print url

    response = requests.request('GET', url)

    return response.json()

def search(api_key, ID):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'id': ID,
        'key': api_key
    }
    return request(API_HOST, PLACE_DETAIL_PATH, url_params=url_params)



def query_api(ID):
    """Queries the API by the input values from the user.
    Args:
        zip_code (str): The zip_code of the business to query.
    """
    response = search(API_KEY, ID)['result']
    #print response
    print "response recieved"

    with open('google_results_final_unique.csv','a') as r:
        # id,lat,long,name,address,category,zip,phone,closed

        results = {
            'id':response['place_id'].encode('utf-8').strip(),
            'lat':response['geometry']['location']['lat'],
            'long':response['geometry']['location']['lng'],
            'name':response['name'].encode('utf-8').strip().replace(',',''),
            'address':response['formatted_address'].encode('utf-8').strip().replace(',',''),
            'category':' '.join(response['types']).encode('utf-8').strip(),
            'zip':'Google',
            'phone':response['formatted_phone_number'].encode('utf-8').strip().replace('(','').replace(')','').replace(' ',''),
            'closed':response['opening_hours']['open_now']
        }
        line = '{id},{lat},{long},{name},{address},{category},{zip},{phone},{closed}\n'.format(**results)
        print line
        r.write(line)


def main():

    #read in Yelp YelpResults
    df = pandas.read_csv('google_results_unique.csv')
    ids = df.id
    #ids = ['ChIJ2ZXz2xtm0FQRgeg37d6jGLM','ChIJW7EPKARX0VQR-XIQ22tYNi4']
# id,lat,long,name,address,category,zip,phone,closed

    # write header line
    with open('google_results_final_unique.csv','w') as f1:
        f1.write('id,lat,long,name,address,category,zip,phone,closed\n')

    for ID in ids:
        try:
            query_api(ID)
        except Exception, e:
            print 'ERROR'
            print e


if __name__ == '__main__':
    main()
