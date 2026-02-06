# import is the keyword in python which is used to import packages or libraries which are not shipped with python itself.
# One of such important packages which is also popular is functools.
# In this functools package we can get the access to use the "reduce()" method which is helpful to optimize the complex math calulations.
import functools

# json is another python built in library to convert the data types into strings and vice-versa.
import json

# Pickle is an package shipped with python which helps to handle the data more conviniently when dealing with dictionaries.
# Pickle converts the data into binary format and can revert back to python compatiable data formats.
import pickle

# OrderedDict is another method available from "Collections" package which is used to ensure that the order in the dictionary stays the same.
from collections import OrderedDict 

# Importing own custom modules from another file withing the application.
from hash_util import hash_256, hash_block

# Importing the custom build "block" class into the file to refactor the "block" related code.
from classes.block import Block
from classes.transaction import Transaction
from classes.verification import Verification

# This is the initial project setup file to understand the basics of python and make the mind around
# the blockchain and crypto currency environemnt using python principles.

# This is the basic python data type which is non primitive and is similar to arrays in JavaScript
# which is called a "List" in python and it's representation is same as in JS which is []

# This is the amount that will be added to the participant who is performing the mining process and gets it as a reward.
MINING_REWARD = 10

# The term blockchain is the varibale representation in python.
# There are no keywords like var, int, const in python.
blockchain = []
# Open_Transactions is a list which represents the transactions that are under build process.
# If user wants to add coins then they will be adding that transaction to list of open transactions.
open_transactions = []

# Defining the variable owner which for now represents the sender for any transaction for the local instance of blockchain.
owner = 'SAI'

# participant -> User who is willing to do a transacation.
# Participant here is data type of SET which ignores the duplicate values.
# participants = {'Manuel'}


# function to read file
def load_data():
    global blockchain
    global open_transactions
    # Using "try" keyword in python, here in load_data() function to execute the handling of errors in the code
    # more efficiently by addressing the errors which may lead to abrupt program execution and cause damange to 
    # the uuser experience.
        # So, the "try" block here first tries to execute the code within it whenever the load_data() function is
        # triggered in the application. And if there is no error in the code the result is generated from this block.
    try:
        with open('blockchain.txt', mode='rb') as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()

            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            # print('pickle chain', file_content['chain'])
            # print('pickle open_transactions', file_content['ot'])
            # json.loads() - as we already know that json package in python is used to convert string type to python dictionaries and vice-versa
            # So, inorder to convert stringifed version of blockchain and open_transactions into python native dictionary format json helps us with loads() method.
            blockchain = json.loads(file_content[0][:-1])
            for block in blockchain:
                updated_blockchain = []
                # Refactoring the converted_tx by using the instance of the Transaction class 
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transaction']]
                # Used the instance of the Block class and passed the attribute values.
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], 0)
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for transaction in open_transactions:
                # Refactoring the updated_transactions by using the instance of the Transaction class 
                updated_transactions = Transaction(transaction['sender'], transaction['recipient'], transaction['amount'])
                updated_transactions.append(updated_transactions)
            open_transactions = updated_transactions
    # So, it is also an convention that every try block should be continued with atleast one "except" block.
    # The purpose of except block is to handle the errors which the try block couldn't handle and which eventually
    # throws an error and stops the execution of further code.
    # Python, also gives some in-built Error related Keywords which are related to general error causing scenarios.
    # For example, In this case (FileNotFoundError) can be used.
    except (FileNotFoundError, IndexError):
        # genesis_block - It is the first block of the blockchain transaction which initializes the blockchain transactions.
        # Refactored the genesis_block with the Block class instance 
        genesis_block = Block(0, '', [], 100, 0)
        blockchain = [genesis_block]

    # Finally, is the another keyword which can be combined with try/catch block of code which can be used to handle
    # any code block irrespective of whether it is handled in try or except code block, this code in finally will execute.
    # This code block is usually good to execute any clean up work that has to be happening for the function.
    finally:
        print('cleanup has to be handled here.')
    
    
    load_data()


# function to write file
def save_data():
    # with - this is built in keyword in python when dealing with files and it ensures that the file closes
    # automatically once the execution of the code is done without using of close() method.
    # open() - The method open() takes in two parameters 
    # name of the file
    # mode in with the file has to be handled.

    # using pickle  
    # - the extension of the file is changed from .txt to .p to make the file compatiable with pickle library.
    # - the mode is also changed from 'w' to 'wb' indicating that pickle works with binary format when writing into a file.

    try:
        with open('blockchain.txt', mode='w') as f:
            # here, blockchain and open_transacations are in list format. But, appending into files only works with string format data.
            # so using str() on the blockchain to avoid errors.
            # Also, as we know since pickle writes only binary data the line escape charector is not handled in pickle file.
            # so, the work around is to store the data that has to be modified by the pickle package and escape the line escape. 
            # pickle_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # json.dumps() - as we already know that json package in python is used to convert python dictionaries to stringified versions and vice-versa
            # So, inorder to convert python dictionaries to stringified version of lists of blockchain and open_transactions into python native dictionary format json helps us with dumps() method.
                
            # converting the block into dict format to mitigate the errors.
            blockchain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(blockchain))
            f.write('\n')
            open_transactions = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(open_transactions))
    except IOError:
        print('Unble to write data to the file.')


# following a convention that each function should perform single task for implementing code redability
# and maintainability in the application.
def get_last_transaction_value():
    """ Function to return the last block from the blockchain."""
    # checking the length of the blockchain list so that conditional ouputting of blocks can be handled.
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

    
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


# proof_of_work() - This is the function which takes care of implementing the "valid_proof" functionality on
# every transaction by looping it to ensure all the transactions from the open transactions which will be added 
# to the blockchain are verified and authenticated.
def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


# Function repsonsible to mine blocks and add the open transactions to actual list of processed transactions.
# In order to add the open_transactions to processed transaction a hashing mechanism has to be implemented to make
# the blockchain secure while mining the blocks.
def mine_block():
    try:
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
        mining_reward_transaction = Transaction('MINING', owner, MINING_REWARD)
        
        # [:] -> Represents the range selector in a list which creates a copy of the original list of all the elements from start to end 
        copied_transactions = open_transactions[:]
        copied_transactions.append(mining_reward_transaction)
        # Refactored the block variable with "Block" class instance.
        block = Block(len(blockchain), hashed_block, copied_transactions, proof)
        blockchain.append(block)
        return True
    except IndexError:
        print('List Index may be out of range.')
    finally:
        print('Mine block code completed...')


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

    # Using Transaction class instance to refactor the ordered_transactions
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False
    # append() -> It is the built in python method for the List data type used to add values to the
    # list at the end of the existing list.
    # The values in the list can be accessed with the position which are called "index" which starts
    # from 0.
    # blockchain(-1) ->. represents the accessibility to values from the right, usually it is from left.
    # print() -> it is another python method used to output the values in the terminal when executed.


# function to check the balances (amount sent and amount recieved) of the participants in the blockchain environemnt.
# Implementing the double list comprehension technique where in the 
#   - first list the result is retreving the transaction.
#       - In this transaction checking the conditions that identifies the participant if sender or recipient.
#   - second list the result is retriving the amount from the transaction based on the participant.
#   - Once the values of the sender amount and recipient amount are extracted then looping through all the transactions to get the balance.   
def get_balance(participant):
# Since, we changed the data type of block from 'dictionary' to a class Object the attributes are not accessed by [] but by . notation.

# Refactoring the tx_sender, open_transaction_sender by properly accessing the attributes of the Transaction class 
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_transaction_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    # Here, the sender is checked with the balance for his transactions both in open transactions and processed transactions in the blockchain.
    # the reduce() takes in three arguments in which the 
        # first is a function to handle the elements in the list.
        # second is a iterable 
        # third is the list of values to be returned as a result.
    tx_sender.append(open_transaction_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_recieved - amount_sent
    

awaiting_input = True

# While loop is another built in python functionality to loop infinetly till a condition is meet.
# The syntax for the while loop is as follows.
while awaiting_input:
    print('Choose an option from below.')
    print('1: Add a new transaction value.')
    print('2: Mine Block')
    print('3: Output the blocks of the blockchain.')
    print('4: Verify all transactions validity.')
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
        verifier = Verification()
        if verifier.verify_transactions(open_transactions):
            print('All transactions are valid.')
        else: 
            print('Invalid transactions are present.')
    elif user_choice == 'q':
        # break -> breaks the current execution and quits out of the loop
        # continue -> continue stops executing the current condition and starts the loop execution  from the first.
        awaiting_input = False
        # continue
    else:
        print('Invalid input. Please select something from the list of choices.')
    # print('Checking the continue execution.')
    verifier = Verification()
    if not verifier.verify_blockchain(blockchain):
        print_blockchain_elements()
        print('Invalid blockchain.')
        break
    # format() -> It is a python built in method which displays the values in a string according to the 
    # orders in which they are mentioned in the method. Format accepts any number of variables.
    # The placeholder for displaying the varibale values when using the format method also accepts the 
    # formating in terms of decimal notations and limit of charecters in the string.
    print('Balance of {} is {:6.2f}'.format('Manuel', get_balance('nadipalli')))
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



# Dividng the code into more organized and granular blocks by implementing the concepts of classes.
# So, the idea is to have individual classes for
#     - blockchain (chain, open_transactions, methods)
#     - block (previous_hash, index, timestamp, transactions, proof_of_work)
#     - transactions (sender, recipient, amount)
#     - verification (verification methods)
#     - node (UI for accepting the user inputs)
