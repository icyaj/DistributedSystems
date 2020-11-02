# Webservice 1 - 'https://api.postcodes.io/postcodes/'

# Imports all libraries required.
import Pyro4
import urllib.request
import json

# Webservice Class.
@Pyro4.expose
class WebService(object):

    # Initialises the api url.
    def __init__(self):
        self.url = 'https://api.postcodes.io/postcodes/'

    # Returns the address of the Postcode in the form longitude & latitude.s
    def getAddress(self, postcode):
        # Try, Except - Will return False if an error has occurred i.e. if the Postcode is not found or can not access the api.
        try:
            # Response from the api is stored in response before being decoded and converted to json format in js.
            response = urllib.request.urlopen('{0}/{1}'.format(self.url, postcode.replace(" ", "")))
            strResponse = response.read().decode('utf-8')
            js = json.loads(strResponse)
            # Returns Error if not successful. Else returns the address.
            if js['status'] != 200:
                return 404, 'Error - POSTCODE Not Found. Webservice 1 - https://api.postcodes.io/postcodes/'
            else:
                return 200, {'longitude': js['result']['longitude'], 'latitude': js['result']['latitude']}

        except urllib.request.HTTPError:
            return 404, 'Error - POSTCODE Not Found. Webservice 1 - https://api.postcodes.io/postcodes/'
        except OSError:
            return 503, 'Error - API {0} Failed To Connect.  Webservice 1 - https://api.postcodes.io/postcodes/'.format(self.url)


# Create a Daemon and locate Name Server.
daemon = Pyro4.Daemon()
uri = daemon.register(WebService)

# Registers the webserver
ns = Pyro4.locateNS()
ns.register("WS1", uri)

# Prints the server is online
print("Server WS1 Online: Object uri =", uri)

# PYRO4 request loop.
daemon.requestLoop()
