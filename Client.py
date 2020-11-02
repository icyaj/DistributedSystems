import Pyro4
from datetime import datetime


def divider():
    print('\n-------------------------------------\n')


# Displays the options to the user.
def displayOptions():
    divider()
    print("Please Enter The Option Number You Require.")
    print("0 : Create A New Order")
    print("1 : View Existing Orders")
    print("2 : Display Menu")
    print("3 : Quit")

    while True:
        option = input('\nEnter Your Option: ').strip()
        if option in ['0', '1', '2', '3']:
            return option
        else:
            print('\nInvalid Option, Please Enter A Valid Option.')


# Checks if the user is on the database and returns the welcome message from the server.
# Returns True if it can access the server, else it returns False.
def checkCustomer(name):
    try:
        print(justHungry.initConnect(name))
        return True
    # Error catching in case server can not be accessed.
    except:
        print('Error - Could not connect to server. Try again later')
        return False


# Retrieves and displays the menu to the client.
def printMenu(fullMenu):
    divider()
    print('Displaying Food Menu:')
    print('\nFood Code : Dish Name : Price')

    print('\nStarter:')
    for item in fullMenu[0]:
        print('{0} : {1} : £{2}'.format(item[0], item[1], item[2]))

    print('\nMains:')
    for item in fullMenu[1]:
        print('{0} : {1} : £{2}'.format(item[0], item[1], item[2]))

    print('\nDesert:')
    for item in fullMenu[2]:
        print('{0} : {1} : £{2}'.format(item[0], item[1], item[2]))


# Finds item in menu.
def searchMenu(menu, foodCode):
    # preliminary check to see if in menu.
    if foodCode[0] in ['s', 'm', 'd']:

        # Narrows down the search space to starters, mains or dessert.
        if foodCode[0] == 's':
            course = 0
        elif foodCode[0] == 'm':
            course = 1
        else:
            course = 2

        # Checks all dishes in the specific course and returns if a match is found.
        for item in menu[course]:
            if foodCode == item[0]:
                return item

    # Returns false if dish can not be found.
    return False


# Client enters there food order followed by the amount.
def createOrder(menu):
    divider()
    print('To create your order please enter the food codes followed by the number you wish to order.')
    print('Keep input blank once you have added all your dishes to the order.')

    # Stores the clients order.
    order = []

    while True:
        # Client enters food code
        item = input('\nEnter the food code: ').lower().strip()

        # If blank returns the order. (Order finished)
        if item == '':
            return order

        # Checks if food code is valid.
        response = searchMenu(menu, item)

        # Prints error if valid, Else asks for amount of the dish & appends to order.
        if not response:
            print('\nError - Invalid Food code, Try Again.')
        else:
            # Checks for valid integer.
            valid = False
            while not valid:
                # Asks client for the amount of said dish.
                amount = input('Enter the amount: ').strip()

                # Appends to order if positive integer. Else prints error.
                if amount.isdigit():
                    order.append((item, amount))
                    valid = True
                else:
                    print('\nError - Invalid Amount Must Be A Positive Integer, Try Again.\n')


# Returns the dietary requirements of the client.
def dietryRequirements():
    divider()
    return input('Do you have any dietary requirements? (Input if yes, else keep blank): ').strip()


# Gets the clients address details from the Postcode
def getPostcode():
    divider()
    while True:
        # Asks user for postcode and parses to Front-End
        postcode = input('Enter Your Postcode: ').strip().upper()
        print('\nJust fetching your address details...')
        try:
            status, address = justHungry.getPostcode(postcode)
        # Error catching in case server can not be accessed.
        except:
            print('\nError - Could not connect to server. Try again later')
            return False, postcode, {}
        # If Valid prints the address
        if status == 'success':
            print('\nFrom our database we calculated your is address: ')
            for key in address:
                print('    {0} : {1}'.format(key, address[key]))

            return 'success', postcode, address
        # Postcode Failure.
        elif status == 'failure':
            print('\nError - Postcode Server is unavailable... Please try again later.')
            return 'failure', postcode, address
        else:
            print('\nError - Invalid Postcode, Sorry your postcode does not appear to be valid.\n')


# Displays the final order details to the client.
def confirmOrder(name, menu, foodOrder, requirements, postcode, address):
    divider()
    # Order total
    orderTotal = 0

    # Displays the order details.
    print('Your Order: ')

    print('\nName: {0}'.format(name))
    print('Dietary Requirements: {0}'.format(requirements))

    print('\nPostcode: {0}'.format(postcode))
    print('Address:')
    # Displays the Address of the postcode:
    for key in address:
        print('    {0} : {1}'.format(key, address[key]))

    print('\nDishes: ')
    # Displays all items in the food order.
    for items in foodOrder:
        # Finds the dish in the menu.
        dish = searchMenu(menu, items[0])

        # Dish total.
        total = int(items[1]) * dish[2]

        # Displays Dish.
        print('    {0} - {1}'.format(dish[0], dish[1]))
        print('        Quantity: {0} | Each: £{1} | Total: £{2}'.format(items[1], dish[2], total))

        # Adds dish total to overall total.
        orderTotal += total

    print('\nOrder Total: £{0}'.format(orderTotal))

    # Asks the user to confirm if sending the order.
    confirm = False
    while confirm not in ['y', 'n']:
        confirm = input('\nWould you like to confirm your order? (y/n): ').strip().lower()

        # User Confirms sending order.
        if confirm == 'y':
            divider()
            print('Sending Order.')

            # Packages the order into an array and sends to the Server awaiting confirmation.
            order = [requirements, postcode, foodOrder, orderTotal, address]
            confirmation, orderNumber, orderTime = justHungry.postOrder(name, order)

            # Tells the user if the order was successful or if an error occurs.
            if confirmation == 'Success':
                print('\nSuccess! Order confirmed at: {0}'.format(
                    datetime.fromtimestamp(orderTime).strftime('%Y-%m-%d %H:%M:%S')))
                print('Here is your order Number: {0}'.format(orderNumber))
                print('\nYour order will be with you shortly. Thank you for using Just Hungry'.format(orderNumber))
            else:
                print('Error - Processing your order, Please try again later.')

        # User declines not sending order.
        elif confirm == 'n':
            print('\nCancelling Order')

        # Error Incorrect Order.
        else:
            print("Error - Invalid Option, Please Enter 'y' or 'n'")


# Finds order in orders.
def searchOrder(orders, orderNumber):
    # Appends to order if positive integer. Else returns False.
    if orderNumber.isdigit():
        # Checks all dishes in the specific course and returns if a match is found.
        for item in orders:
            if int(orderNumber) == item[0][0]:
                return item

    return False


def displayOrder(response, menu):
    divider()
    # Displays the order details.
    print('Your Order: {0} - Ordered: {1}'.format(response[0][0],
                                                  datetime.fromtimestamp(response[0][1]).strftime('%Y-%m-%d %H:%M:%S')))

    print('\nName: {0}'.format(response[0][2]))
    print('Dietary Requirements: {0}'.format(response[1][0]))

    print('\nPostcode: {0}'.format(response[1][1]))
    print('Address:')
    # Displays the Address of the postcode:
    for key in response[1][4]:
        print('    {0} : {1}'.format(key, response[1][4][key]))

    print('\nDishes: ')
    # Displays all items in the food order.
    for items in response[1][2]:
        # Finds the dish in the menu.
        dish = searchMenu(menu, items[0])

        # Dish total.
        total = int(items[1]) * dish[2]

        # Displays Dish.
        print('    {0} - {1}'.format(dish[0], dish[1]))
        print('        Quantity: {0} | Each: £{1} | Total: £{2}'.format(items[1], dish[2], total))

    print('\nOrder Total: £{0}'.format(response[1][3]))

    divider()
    print('Keep Blank To Go Back To Main Menu')


# Retrieves all the clients orders.
def viewOrder(name, menu):
    divider()
    print('\nRetrieving Your Recent Orders: ')

    # Gets all the order numbers with the times.
    try:
        orders = justHungry.getOrders(name)
        # Error catching in case server can not be accessed.
    except:
        print('\nError - Could not connect to server. Try again later')
        return False

    if not orders:
        print('\nNo Recent Orders.')
    else:
        print('\nOrder Number : Time of Order : Postcode')
        for order in orders:
            print('    {0} : {1} : {2}'.format(order[0][0],
                                               datetime.fromtimestamp(order[0][1]).strftime('%Y-%m-%d %H:%M:%S'),
                                               order[1][1]))

        print('\nTo Find Out More About An Order Enter Order Number.')
        print('Otherwise Keep Blank To Go Back To Main Menu')

        search = True
        while search:

            # Client enters food code
            orderNumber = input('\nEnter the Order Number: ').strip().lower()

            # If blank returns to Main Menu.
            if orderNumber == '':
                search = False
            # Else Goes to Order.
            else:
                # Checks if order code is valid.
                response = searchOrder(orders, orderNumber)

                # Prints error if valid, Else Displays the order.
                if not response:
                    print('\nError - Invalid Order Number, Try Again.')
                else:
                    displayOrder(response, menu)
    return True

# Main Function.
def main():
    try:
        divider()
        # Print Welcome Message and asks client name.
        print('Welcome to Just Hungry, An online food ordering system!')

        name = ''
        while not name:
            name = input("To continue, please enter your name: ").strip()

            if not name:
                print('\nError - Invalid Name, Must Be More Than One Character\n')

        # Creates a Client Obj a new customer or gets existing customer on Database server.
        status = checkCustomer(name)

        # Gets Food Menu.
        if status:
            menu = justHungry.getMenu()

        while status:
            # Displays the options to the user.
            option = displayOptions()

            # Create a new order
            if option == '0':

                printMenu(menu)

                # Asks what food the client wants
                foodOrder = createOrder(menu)

                # Asks the client about any dietary requirements / allergies
                requirements = dietryRequirements()

                # Gets client postcode if applicable else Sets the client postcode
                status, postcode, address = getPostcode()

                # If no postcode server found go to main menu.
                if status == 'failure':
                    continue
                # If no connection to server quit.
                elif status == False:
                    continue

                # Order Confirmation
                confirmOrder(name, menu, foodOrder, requirements, postcode, address)

            # View existing orders
            elif option == '1':
                status = viewOrder(name, menu)

            # Display Menu
            elif option == '2':
                printMenu(menu)

            # Quit (Option 3)
            else:
                status = False

    # Error catching in case server can not be accessed.
    except ConnectionRefusedError:
        print('Error - Could not connect to server. Try again later')


# use name server object lookup uri shortcut
justHungry = Pyro4.Proxy("PYRONAME:JustHungry.FrontEnd")

## Starts the Main Function.
main()
