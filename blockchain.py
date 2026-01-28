# This is the initial project setup file to understand the basics of python and make the mind around
# the blockchain and crypto currency environemnt using python principles.

# This is the basic python data type which is non primitive and is similar to arrays in JavaScript
# which is called a "List" in python and it's representation is same as in JS which is []

# The term blockchain is the varibale representation in python.
# There are no keywords like var, int, const in python.
blockchain = [1]

# following a convention that each function should perform single task for implementing code redability
# and maintainability in the application.
def get_last_transaction_value():
    """ Function to return the last block from the blockchain."""
    return blockchain[-1]


# This is the syntax for defining a function in python, which is defined with a "def" keyword
# followed by name of the function and () and :
# The second line of the function has to be indented to get identified by the python compiler
# in order to execute the code.
def add_block(transaction_amount, last_transaction=[1]):
    """ Function to perfom the task of adding value/data to the block.

    Arguments: 
        : transaction_amount: this is a float value to be entered by the user.
        : last_transaction: this is a block which is last block in the blockchain.
    """
    blockchain.append([last_transaction, transaction_amount]) 
    # append() -> It is the built in python method for the List data type used to add values to the
    # list at the end of the existing list.
    # The values in the list can be accessed with the position which are called "index" which starts
    # from 0.
    # blockchain(-1) ->. represents the accessibility to values from the right, usually it is from left.
    # print() -> it is another python method used to output the values in the terminal when executed.

    
# Function to fetch the transaction value
def get_transaction_value():
    """ Function that is responsible to fetch the user inputs in the float format."""
    user_input = float(input('Please enter an amount: '))
    return user_input

# Function to fetch the user input
def get_user_choice():
    user_input = input('Choose an option: ')
    return user_input

# Function to print blockchain elements.
def print_blockchain_elements():
    # For loop is the in built python functionality which helps to loop through the iterable data types, here it is "list".
    # The syntax of for loop is as written below.
    for block in blockchain:
        print('Outputting the blocks.')
        print(block)

tx_amount = get_transaction_value()
add_block(tx_amount)


# While loop is another built in python functionality to loop infinetly till a condition is meet.
# The syntax for the while loop is as follows.
while True:
    print('Choose an option from below.')
    print('1: Add a transaction.')
    print('2: Output the blocks of the blockchain.')
    print('q: Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        # input() -> It is also an built in python method which accepts the user inputs from the terminal commandline.
        # float() -> It is a data type method to convert the usual user string input to required float format for tx.
        tx_amount = get_transaction_value()
        # To execute the function just call it by the function name along with ().
        add_block(tx_amount, get_last_transaction_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'q':
        # break -> breaks the current execution and quits out of the loop
        # continue -> continue stops executing the current condition and starts the loop execution  from the first.
        break
        # continue
    else:
        print('Invalid input. Please select something from the list of choices.')
    # print('Checking the continue execution.')
        

print('DONE.')