# import is the keyword in python which is used to import packages or libraries which are not shipped with python itself.
# One of such important packages which is also popular is functools.
# In this functools package we can get the access to use the "reduce()" method which is helpful to optimize the complex math calulations.
import functools

# json is another python built in library to convert the data types into strings and vice-versa.
import json

# hashlib is a python package which is packed with hashing related functions/methods which are useful in this application.
# This package is imported from python standard library.
import hashlib

# OrderedDict is another method available from "Collections" package which is used to ensure that the order in the dictionary stays the same.
from collections import OrderedDict 

# Importing own custom modules from another file withing the application.
from hash_util import hash_256, hash_block

# This is the initial project setup file to understand the basics of python and make the mind around
# the blockchain and crypto currency environemnt using python principles.

# This is the basic python data type which is non primitive and is similar to arrays in JavaScript
# which is called a "List" in python and it's representation is same as in JS which is []

# genesis_block - It is the first block of the blockchain transaction which initializes the blockchain transactions.
genesis_block = {
    'previos_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}

# This is the amount that will be added to the participant who is performing the mining process and gets it as a reward.
MINING_REWARD = 10

# The term blockchain is the varibale representation in python.
# There are no keywords like var, int, const in python.
blockchain = [genesis_block]
# Open_Transactions is a list which represents the transactions that are under build process.
# If user wants to add coins then they will be adding that transaction to list of open transactions.
open_transactions = []

# Defining the variable owner which for now represents the sender for any transaction for the local instance of blockchain.
owner = 'SAI'

# participant -> User who is willing to do a transacation.
# Participant here is data type of SET which ignores the duplicate values.
participants = {'Manuel'}


# function to read file
def load_data():
    with open('blockchain.txt', mode='r') as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions
        # json.loads() - as we already know that json package in python is used to convert string type to python dictionaries and vice-versa
        # So, inorder to convert stringifed version of blockchain and open_transactions into python native dictionary format json helps us with loads() method.
        blockchain = json.loads(file_content[0][:-1])
        for block in blockchain:
            updated_blockchain = []
            updated_block = {
                'previous_hash': block['previous_hash'],
                'index': block['index'],
                'proof': block['proof'],
                'transactions': [OrderedDict([
                    ('sender', tx['sender']), 
                    ('recipient', tx['recipient']), 
                    ('amount', tx['amount'])]) 
                for tx in block['transactions']],
            }
            updated_blockchain.append(updated_block)
        blockchain = updated_blockchain
        open_transactions = json.loads(file_content[1])
        updated_transactions = []
        for transaction in open_transactions:
            updated_transactions = OrderedDict(
                [
                    ('sender', transaction['sender']),
                    ('recipient', transaction['recipient']),
                    ('amount', transaction['amount'])
                ]
            )
            updated_transactions.append(updated_transactions)
        open_transactions = updated_transactions 
 
load_data()


# function to write file
def save_data():
    # with - this is built in keyword in python when dealing with files and it ensures that the file closes
    # automatically once the execution of the code is done without using of close() method.
    # open() - The method open() takes in two parameters 
    # name of the file
    # mode in with the file has to be handled.
    with open('blockchain.txt', mode='w') as f:
        # here, blockchain and open_transacations are in list format. But, appending into files only works with string format data.
        # so using str() on the blockchain to avoid errors.
        # json.dumps() - as we already know that json package in python is used to convert python dictionaries to stringified versions and vice-versa
        # So, inorder to convert python dictionaries to stringified version of lists of blockchain and open_transactions into python native dictionary format json helps us with dumps() method.
        f.write(json.dumps(blockchain))
        f.write('/n')
        f.write(json.dumps(open_transactions))


# following a convention that each function should perform single task for implementing code redability
# and maintainability in the application.
def get_last_transaction_value():
    """ Function to return the last block from the blockchain."""
    # checking the length of the blockchain list so that conditional ouputting of blocks can be handled.
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# function to check the balances (amount sent and amount recieved) of the participants in the blockchain environemnt.
# Implementing the double list comprehension technique where in the 
#   - first list the result is retreving the transaction.
#       - In this transaction checking the conditions that identifies the participant if sender or recipient.
#   - second list the result is retriving the amount from the transaction based on the participant.
#   - Once the values of the sender amount and recipient amount are extracted then looping through all the transactions to get the balance.   
def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_transaction_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    # Here, the sender is checked with the balance for his transactions both in open transactions and processed transactions in the blockchain.
    # the reduce() takes in three arguments in which the 
        # first is a function to handle the elements in the list.
        # second is a iterable 
        # third is the list of values to be returned as a result.
    tx_sender.append(open_transaction_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_recieved - amount_sent


# Function to check the authenticity of a transaction.
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

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
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    # Refactoring the transactions from regular dictionary into OrderedDict to ensure the order of key,value paris remain same.
    # OrderedDict accepts list of tuples in a (key, value) format.
    ordered_transactions = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(ordered_transactions):
        open_transactions.append(ordered_transactions)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False
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

# tx_amount = get_transaction_value()
# add_transaction(tx_amount)

# valid_proof() - This is the function defined to verify the refactored hashing mechanism.
# This function accepts three parameters
    # transactions -> these are all the transactions in the blockchain
    # previous_hash -> the hash value from the previous transactions in the blockchain
    # proof -> the code/identification that is integrated into the hash string to then verify among every transaction.
def valid_proof(transactions, previous_hash, proof):
    hash = (str(transactions) + str(previous_hash) + str(proof)).encode()
    hashed_str = hash_256(hash)
    print(hashed_str)
    return hashed_str[0:2] == '00'


# proof_of_work() - This is the function which takes care of implementing the "valid_proof" functionality on
# every transaction by looping it to ensure all the transactions from the open transactions which will be added 
# to the blockchain are verified and authenticated.
def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof




# Function repsonsible to mine blocks and add the open transactions to actual list of processed transactions.
# In order to add the open_transactions to processed transaction a hashing mechanism has to be implemented to make
# the blockchain secure while mining the blocks.
def mine_block():
    last_block = blockchain[-1]
    # As mining process has to be secured the hashing process becomes more important to be implemented.
    # For now a easy way to implement hashing is to used the stringified version of all the key values from the block.
    # In order to do so, lets loop through all the keys in the block dictionary and access the values and convert the
    # values to the string format.
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # print(hashed_block, 'hashed_block_output')
    # mining_reward_transaction is a document which is added to the open transaction for the contribution to perfom mining.
    # mining_reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }

    # Using OrderedDict to represent mining_reward_transaction dictionary
    mining_reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    
    # [:] -> Represents the range selector in a list which creates a copy of the original list of all the elements from start to end 
    copied_transactions = open_transactions[:]
    copied_transactions.append(mining_reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transaction': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True

# Function to verify all the transactions.
def verify_transactions():
    return all ([verify_transaction(tx) for tx in open_transactions])


# Function to verify the blockchain is valid by comparing the previous blocks in the blockchain by their values.
def verify_blockchain():
    # modifying the verify_blockchain function which verifies the current block with previous blocks.
    # Veification is done by comparing the hash key values which is "previous_hash" in every block.
    # So in order to compare the list [blockchain] with the dictionary {transaction} in a loop, python has a build in
    # method called enumerate -> enumerate() converts the list into tuple which in terms looks alike like a dictionary. 
    for (index, block) in enumerate(blockchain):
        # print(block, 'verify_block')
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transaction'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is not valid.')
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
    print('4: Output list of participants.')
    print('5: Verify all transactions validity.')
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
        if add_transaction(tx_recipient, amount=tx_amount):
            print('Successfully Added Transaction.')
        else:
            print('Transaction Failed.')
    elif user_choice == '2':
        if mine_block():
            # Resetting the blockchain to empty block once the mining of block is finished.
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid.')
        else: 
            print('Invalid transactions are present.')
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
    # format() -> It is a python built in method which displays the values in a string according to the 
    # orders in which they are mentioned in the method. Format accepts any number of variables.
    # The placeholder for displaying the varibale values when using the format method also accepts the 
    # formating in terms of decimal notations and limit of charecters in the string.
    print('Balance of {} is {:6.2f}'.format('Manuel', get_balance('SAI')))
print('DONE.')


# Transaction - Dictionary // key,value pairs
# Outstanding_transactions - list // Order doesnt matter
# blockchain - list // order matters 
# block - dictionary // 
# participants - set //

# shallow copy - Results in only copy of the outer data type but no the internal elements of the outer data type.
    # shallow copy of [{'name': 'Max'}] -> result in copy of outer list [], but whnen you edit the internal elements like "name"
    #  the value of the "name" changes in the copied list.
# Deep copy - Results in the copy of complete value and the data type even for the internal elements which are nested.

# "is" key word is not same as "=="
    # == just compares the values and the data type of two varaibles but not their reference in memory
    # is in addition to ==, "is" also compares references in memory.
