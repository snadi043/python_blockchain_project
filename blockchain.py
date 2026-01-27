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
    return blockchain[-1]


# This is the syntax for defining a function in python, which is defined with a "def" keyword
# followed by name of the function and () and :
# The second line of the function has to be indented to get identified by the python compiler
# in order to execute the code.
def add_block(transaction_amount, last_transaction=[1]):
    blockchain.append([last_transaction, transaction_amount]) 
    # append() -> It is the built in python method for the List data type used to add values to the
    # list at the end of the existing list.
    # The values in the list can be accessed with the position which are called "index" which starts
    # from 0.
    # blockchain(-1) ->. represents the accessibility to values from the right, usually it is from left.
    # print() -> it is another python method used to output the values in the terminal when executed.

# Function to get user input and use it where ever needed in the code to reduce code repetition.
def get_user_input():
    return float(input('Please enter an amount: '))


# input() -> It is also an built in python method which accepts the user inputs from the terminal commandline.
# float() -> It is a data type method to convert the usual user string input to required float format for tx.
tx_amount = get_user_input()

# To execute the function just call it by the function name along with ().
add_block(tx_amount, get_last_transaction_value())
print(blockchain)