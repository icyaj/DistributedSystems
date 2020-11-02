## Hkxx26 - Just Hungry 

# How to Use:

To start: 

    - Make sure pyro4 is installed. 
    
    - Open a terminal & for each enter terminal one the following.
    
    /: pyro4-ns (runs the pyro4 name service)
    /: python Client.py (Client Program)
    /: python FrontEnd.py (FrontEnd Server)
    /: python BackendServer1.py (Backend server 1)
    /: python BackendServer2.py (Backend server 2)
    /: python BackendServer3.py (Backend server 3)
    /: python WebService1.py (webservice server 1)
    /: python WebService2.py (webservice server 2)
    
# Webservices used:

I used to two seperate webservice apis to get the address's from the postcodes entered by the user.
    
    - 'https://api.postcodes.io/postcodes/' (Webservice Server 1)
    - 'http://api.getthedata.com/postcode' (Webservice Server 2)

# Notes:

Throughout all the FrontEnd, Backend & Webservice servers all actions and status's are logged.

# Client.py
Once the user starts the Client.py they would be asked for there name. 
This name is the username of the users account which would store all the users recent orders.
If the user enters a name already existing on the database they would be greeted back. 
If the user is not already registered they would be added to the database.

The user is then greeted by a main menu. This menu has 4 options. 
    
    - Option 0 : Create A New Order
    - Option 1 : View Existing Orders
    - Option 2 : Display Menu
    - Option 3 : Quit

There are 4 stages if Option 0 is selected.

    / Stage 1
    - The menu will be displayed.
    - Followed by the user being asked to enter the food/dish code and amount of the dish they require.
    - Once the user has entered all the dishes to there order they will leave the input blank to move to stage 2.
    
    / Stage 2
    - The user would be asked if they have any dietary requirements. 
    
    / Stage 3
    - The user would be asked to enter there postcode.
    - If the postcode is invalid the user would be notified and asked to enter it again.
    - If both the postcode webservice servers are unavaliable the user will be notified and be sent back to main menu.
    
    / Stage 4
    - The whole finalised order will be displayed to the user.
    - The user than is asked to confirm or deny the order.
    - if the user confirms the order it is sent and discarded otherwise.
    
There are 4 stages if Option 1 is selected.

    - The client program will retreive all recent orders displaying them to the user.
    - These displayed orders are filtered by 'Order Number : Time of Order : Postcode'
    - The user can input the order number to display the full order.
    
There are 4 stages if Option 2 is selected.

    - The menu will be displayed.
    
If Option 3 is selected.  

    - The Program Quits.
 
Throughout the whole client.py program there is error checking in every function.

# FrontEnd.py 

The frontend forwards the clients requests to the backend replica servers. 

The frontend server fulfills the replication transparency by assigning a server to the be the primary backend server. 
If connection to the primary backend server can not be established the frontend will cycle through the other servers 
assigning them to be the primary server until a full cycle is completed. 
If a full cycle is complete the user will be notified that the servers are unavailable and to try again later. 

# BackendServer.py

There are 3 backend servers. They store the menu, client and there orders, number of orders on the Database, 
The other replica backup servers and the webservers. 

The Replica servers process the requests made by the clients passed on from the frontend. 
These are then forwarded back to the client.

When the getPostcode() function is invoked the backend replica server will forward the request to the webservice servers. 
Alike in the FrontEnd the server cycles through both the webService servers in case one is unavailable. 
The server will log and return the appropriate response depending on the WebServices error code. 

If the server is the primary server it will invoke the postUpdate() function which will update all the other backend replica servers.
The other Backend servers will then run the recieveUpdate() function updating the servers state.

# WebService.py

2 Webservices are used, one for each webServer in case one webservice is unavaliable. 
The webservice will return the appropriate error code followed by response to the Backend server.

This includes: 
 
    - STATUS CODE: 200 - Success
    - STATUS CODE: 404 - POSTCODE not found
    - STATUS CODE: 503 - The Server failed to connect to the API