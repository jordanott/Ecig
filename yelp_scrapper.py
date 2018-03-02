from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import json
import io

# read API keys
with io.open('keys.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

params = {
    'categories': 'vapeshops',
}


zip_codes = open('CA_ZIPCODES.csv')
zip_codes.next()

with open('yelp_results.csv','w') as f:
    f.write('id,lat,long,name,address,category,zip,phone,closed\n')
    for line in zip_codes:
        zip_code = line.strip()
        response = client.search(location=zip_code,**params)

        for business in response.businesses:
            if business.categories:
                for category in business.categories:
                    if category.alias == 'vapeshops':
                        results = {
                            'id':business.id,
                            'lat':business.location.coordinate.latitude,
                            'long':business.location.coordinate.longitude,
                            'name':business.name,
                            'address':' '.join(business.location.address),
                            'category':category.alias,
                            'zip':zip_code,
                            'phone':business.phone,
                            'closed':business.is_closed
                            }
                        line = '{id},{lat},{long},{name},{address},{category},{zip},{phone},{closed}\n'.format(**results)
                        f.write(line)
