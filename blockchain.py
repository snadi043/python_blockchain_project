# This is the initial project setup file to understand the basics of python and make the mind around
# the blockchain and crypto currency environemnt using python principles.

# This is the basic python data type which is non primitive and is similar to arrays in JavaScript
# which is called a "List" in python and it's representation is same as in JS which is []

# genesis_block - It is the first block of the blockchain transaction which initializes the blockchain transactions.
genesis_block = {
    'previos_hash': '',
    'index': 0,
    'transactions': []
}

# The term blockchain is the varibale representation in python.
# There are no keywords like var, int, const in python.
blockchain = [genesis_block]
# Open_Transactions is a list which represents the transactions that are under build process.
# If user wants to add coins then they will be adding that transaction to list of open transactions.
open_transactions = []

# Defining the variable owner which for now represents the sender for any transaction for the local instance of blockchain.
owner = 'SAI'

# following a convention that each function should perform single task for implementing code redability
# and maintainability in the application.
def get_last_transaction_value():
    """ Function to return the last block from the blockchain."""
    # checking the length of the blockchain list so that conditional ouputting of blocks can be handled.
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# This is the syntax for defining a function in python, which is defined with a "def" keyword
# followed by name of the function and () and :
# The second line of the function has to be indented to get identified by the python compiler
# in order to execute the code.
def add_transaction(recipient, sender = owner, amount=1.0):
    """ Function to perfom the task of adding value/data to the block.

    Arguments: 
        : sender: Person who is willing to send the coins.
        : recipient: Person who is suppose to recieve the coins.
        : amount: Number of coins being used for the transaction.
    """

    # Defining a transaction which is a dictionary with key/value pairs.
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)

    # append() -> It is the built in python method for the List data type used to add values to the
    # list at the end of the existing list.
    # The values in the list can be accessed with the position which are called "index" which starts
    # from 0.
    # blockchain(-1) ->. represents the accessibility to values from the right, usually it is from left.
    # print() -> it is another python method used to output the values in the terminal when executed.

    
# Function to fetch the transaction value/data which should now fetch recipient data and amount value.
# The return type of the function is a tuple becasue it is supposed to be immutatble.
def get_transaction_value():
    """ Function that is responsible to fetch the user inputs in the float format."""
    tx_recipient = input('Please enter the name of the recipient: ')
    tx_amount = float(input('Please enter an amount: '))
    return (tx_recipient, tx_amount)

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
    else:
        print('-' * 20)

tx_amount = get_transaction_value()
add_transaction(tx_amount)

# Function to generate the hashed output of a transaction by expecting a block a input.
def hash_block(block):
    return '-'.join([str(block[keys]) for keys in block])

# Function repsonsible to mine blocks and add the open transactions to actual list of processed transactions.
# In order to add the open_transactions to processed transaction a hashing mechanism has to be implemented to make
# the blockchain secure while mining the blocks.
def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''
    # As mining process has to be secured the hashing process becomes more important to be implemented.
    # For now a easy way to implement hashing is to used the stringified version of all the key values from the block.
    # In order to do so, lets loop through all the keys in the block dictionary and access the values and convert the
    # values to the string format.
    hashed_block = hash_block(last_block)
    print(hashed_block)
    
    block = {
        'previous_hash': 'XYZ',
        'index': len(blockchain),
        'transaction': open_transactions
    }

    blockchain.append(block)

# Function to verify the blockchain is valid by comparing the previous blocks in the blockchain by their values.
def verify_blockchain():
    # modifying the verify_blockchain function which verifies the current block with previous blocks.
    # Veification is done by comparing the hash key values which is "previous_hash" in every block.
    # So in order to compare the list [blockchain] with the dictionary {transaction} in a loop, python has a build in
    # method called enumerate -> enumerate() converts the list into tuple which in terms looks alike like a dictionary. 
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True

awaiting_input = True

# While loop is another built in python functionality to loop infinetly till a condition is meet.
# The syntax for the while loop is as follows.
while awaiting_input:
    print('Choose an option from below.')
    print('1: Add a new transaction value.')
    print('2: Mine Block')
    print('3: Output the blocks of the blockchain.')
    print('h: Manipulate the block.')
    print('q: Quit')

    user_choice = get_user_choice()
    if user_choice == '1':
        # input() -> It is also an built in python method which accepts the user inputs from the terminal commandline.
        # float() -> It is a data type method to convert the usual user string input to required float format for tx.
        tx_data = get_transaction_value()

        # To execute the function just call it by the function name along with ().
        # To add_transaction, the tx_amount has to be passed as argument for which tuple unpacking is needed.
        #  Tuple unpacking is similar to using JS ES6 Feature of Spread and Rest operators.
        tx_recipient, tx_amount = tx_data
        add_transaction(tx_recipient, amount=tx_amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transaction': [{
                    'sender': 'Chris',
                    'recipient': 'Max',
                    'amount': 100.0
                }]
            }

    elif user_choice == 'q':
        # break -> breaks the current execution and quits out of the loop
        # continue -> continue stops executing the current condition and starts the loop execution  from the first.
        awaiting_input = False
        # continue
    else:
        print('Invalid input. Please select something from the list of choices.')
    # print('Checking the continue execution.')
    if not verify_blockchain():
        print_blockchain_elements()
        print('Invalid blockchain.')
        break

print('DONE.')


# Transaction - Dictionary // key,value pairs
# Outstanding_transactions - list // Order doesnt matter
# blockchain - list // order matters 
# block - dictionary // 
# participants - set //
