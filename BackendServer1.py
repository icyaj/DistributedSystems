# Replica Server 1

import Pyro4
from datetime import datetime

@Pyro4.expose
class Database(object):

    def __init__(self):
        # Available Meals.
        self.starters = [('s0', 'Peking Duck', 5.00), ('s1', 'Spring Rolls', 6.00), ('s2', 'Crispy Won-Ton', 4.50)]
        self.main = [('m0', 'Chicken Rice', 8.50), ('m1', 'Lamb with Cumin & Coriander', 10.00), ('m2', 'King Prawns Kung-Po Style', 9.75)]
        self.dessert = [('d0', 'Mint Choc Chip Ice Cream', 2.50), ('d1', 'Lemon Drizzle Cake', 3.00), ('d2', 'Cheese Cake', 3.50)]

        # Stores all the Client details including orders.
        self.clients = {}

        # The number of orders on the database.
        self.orders = 0

        # Replica Servers (slave).
        self.replicaServers = {'R2': R2, 'R3': R3}

        # Webservice Servers (slave).
        self.webServers = {'WS1': WS1, 'WS2': WS2}

    # Initial Connection.
    def initConnect(self, name):
        if name in self.clients:
            return '\nWelcome back {0}, fetching your account details.'.format(name)
        else:
            self.clients[name] = []

            self.postUpdate()

            return '\nHi {0}, We currently do not have you as an existing customer. We have added your name to the database.'.format(name)

    # Returns the Menu
    def getMenu(self):
        return [self.starters, self.main, self.dessert]

    # Stores the user orders
    def postOrder(self, name, order):
        print('Order Posted by user {0}'.format(name))
        self.orders += 1

        # Stores Order Time.
        timestamp = datetime.timestamp(datetime.now())

        self.clients[name].append([[self.orders, timestamp, name], order])

        # Updates the other replicas.
        self.postUpdate()
        return 'Success', self.orders, timestamp

    # Returns the clients orders from the
    def getOrders(self, name):
        print('Previous Orders Requested by user {0}'.format(name))
        return self.clients[name]

    # Returns the clients orders from the
    def getAllOrders(self):
        return self.clients, self.orders

    # Returns the address to the client returned from the webservice server.
    def getPostcode(self, postcode):
        for server in self.webServers:
            try:
                response, address = self.webServers[server].getAddress(postcode)
                if response == 200:
                    print('Success, {0} Retrieved POSTCODE Address.'.format(server))
                    return 'success', address
                else:
                    print(address)
            except:
                print('Error - Could not establish a connection to WebServer {0}.'.format(server))

        print('Error - Could not establish a connection to Any WebServer')
        return 'failure', {'longitude': 0, 'latitude': 0}

    # Posts the updates to the other replica servers.
    def postUpdate(self):
        print('Sending Update To Slave Replicas {0}'.format(self.replicaServers.keys()))
        for server in self.replicaServers:
            try:
                response = self.replicaServers[server].recieveUpdate('R1')

                if response == 'Success':
                    print('Success, Updated server {0}.'.format(server))

            except:
                print('Error - Unsuccessful Update Of Server {0}.'.format(server))
                pass

    # Receives the updates from the primary server.
    def recieveUpdate(self, primary):
        print('Receiving Update From Master {0}.'.format(primary))
        clients, orders = self.replicaServers[primary].getAllOrders()
        self.clients, self.orders = clients, orders
        return 'Success'



# Registers the other Backend Servers
R2 = Pyro4.Proxy("PYRONAME:R2")  # Replica 2
R3 = Pyro4.Proxy("PYRONAME:R3")  # Replica 3

# Registers the Web Service Servers
WS1 = Pyro4.Proxy("PYRONAME:WS1")  # Replica 1
WS2 = Pyro4.Proxy("PYRONAME:WS2")  # Replica 2

a = Database()
# Create a Daemon and locate Name Server.
daemon = Pyro4.Daemon()
uri = daemon.register(a)

# Registers the Replica Server
ns = Pyro4.locateNS()
ns.register("R1", uri)

print("Server R1 Online: Object uri = {0}\n".format(uri))

# PYRO4 request loop.
daemon.requestLoop()

