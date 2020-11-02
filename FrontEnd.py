# FrontEnd Server

import Pyro4

@Pyro4.expose
class FrontEnd(object):

    def __init__(self):
        # Replica Servers (slave).
        self.replicaServers = {'R1': R1, 'R2': R2, 'R3': R3}
        self.primaryReplica = 'R1'
        self.slaveReplicas = ['R2', 'R3']

    # Initial Connection.
    def initConnect(self, name):
        for x in range(3):
            try:
                return self.replicaServers[self.primaryReplica].initConnect(name)
            except:
                self.changePrimary()
        return 'Error - Could not connect to server try again later.'

    # Gets the menu from the Replica Servers
    def getMenu(self):
        for x in range(3):
            try:
                return self.replicaServers[self.primaryReplica].getMenu()
            except:
                self.changePrimary()
        return []

    # Passes the order to the Replica Servers
    def postOrder(self, name, order):
        for x in range(3):
            try:
                return self.replicaServers[self.primaryReplica].postOrder(name, order)
            except:
                self.changePrimary()
        return 'Failure', 0, 0

    # Gets the user orders from the Replica Servers
    def getOrders(self, name):
        for x in range(3):
            try:
                print(self.replicaServers[self.primaryReplica].getOrders(name))
                return self.replicaServers[self.primaryReplica].getOrders(name)
            except:
                self.changePrimary()
        return {}

    # Gets the address from the Replica Servers
    def getPostcode(self, postcode):
        for x in range(3):
            try:
                return self.replicaServers[self.primaryReplica].getPostcode(postcode)
            except:
                self.changePrimary()
        return 'failure', {'longitude': 0, 'latitude': 0}

    # Changes the primary replica server.
    def changePrimary(self):
        self.slaveReplicas.append(self.primaryReplica)
        self.primaryReplica = self.slaveReplicas.pop(0)

# Registers the Backend Servers
R1 = Pyro4.Proxy("PYRONAME:R1")  # Replica 1
R2 = Pyro4.Proxy("PYRONAME:R2")  # Replica 2
R3 = Pyro4.Proxy("PYRONAME:R3")  # Replica 3

# Create a Daemon and locate Name Server.
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

# register the greeting maker as a Pyro object
uri = daemon.register(FrontEnd)

# register the object with a name in the name server
ns.register("JustHungry.FrontEnd", uri)

print("Server FE Online: Object uri =", uri)

# start the event loop of the server to wait for calls
daemon.requestLoop()