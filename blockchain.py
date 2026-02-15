# import is the keyword in python which is used to import packages or libraries which are not shipped with python itself.
# One of such important packages which is also popular is functools.
# In this functools package we can get the access to use the "reduce()" method which is helpful to optimize the complex math calulations.
from functools import reduce 

# json is another python built in library to convert the data types into strings and vice-versa.
import json

# Pickle is an package shipped with python which helps to handle the data more conviniently when dealing with dictionaries.
# Pickle converts the data into binary format and can revert back to python compatiable data formats.
import pickle

# Requests is the package which enables to create a connection using HTTP methods from within the application to other applications.
import requests


# OrderedDict is another method available from "Collections" package which is used to ensure that the order in the dictionary stays the same.
from collections import OrderedDict 

# Importing own custom modules from another file withing the application.
from utilities.hash_util import hash_block
from utilities.verification import Verification

# Importing the custom build "block" class into the file to refactor the "block" related code.
from block import Block
from transaction import Transaction
from wallet import Wallet

# This is the initial project setup file to understand the basics of python and make the mind around
# the blockchain and crypto currency environemnt using python principles.

# This is the basic python data type which is non primitive and is similar to arrays in JavaScript
# which is called a "List" in python and it's representation is same as in JS which is []


# This is the amount that will be added to the participant who is performing the mining process and gets it as a reward.
MINING_REWARD = 10

# Defining the variable owner which for now represents the sender for any transaction for the local instance of blockchain.
# owner = 'SAI'

# participant -> User who is willing to do a transacation.
# Participant here is data type of SET which ignores the duplicate values.
# participants = {'Manuel'}

class Blockchain:
    def __init__(self, public_key, node_id):

        # genesis_block - It is the first block of the blockchain transaction which initializes the blockchain transactions.
        # Refactored the genesis_block with the Block class instance 
        genesis_block = Block(0, '', [], 100, 0)
        # The term blockchain is the varibale representation in python.
        # There are no keywords like var, int, const in python.
        self.__chain = [genesis_block]
        # __open_transactions is a list which represents the transactions that are under build process.
        # If user wants to add coins then they will be adding that transaction to list of open transactions.
        self.__open_transactions = []
        self.public_key = public_key
        self.node_id = node_id
        # node is the private variable in the blockchain class which is of set data type which is unique and cannot be repetitive.
        self.__peer_nodes = set()
        # self.load_data()

    # Making the load_data() as the method of the block__chain. 
    # function to read file
    def load_data(self):
        # Using "try" keyword in python, here in load_data() function to execute the handling of errors in the code
        # more efficiently by addressing the errors which may lead to abrupt program execution and cause damange to 
        # the uuser experience.
            # So, the "try" block here first tries to execute the code within it whenever the load_data() function is
            # triggered in the application. And if there is no error in the code the result is generated from this block.
        try:
            with open('blockchain.txt-{}'.format(self.node_id), mode='rb') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()

                # blockchain = file_content['chain']
                # __open_transactions = file_content['ot']

                # print('pickle chain', file_content['chain'])
                # print('pickle __open_transactions', file_content['ot'])
                # json.loads() - as we already know that json package in python is used to convert string type to python dictionaries and vice-versa
                # So, inorder to convert stringifed version of blockchain and __open_transactions into python native dictionary format json helps us with loads() method.
                blockchain = json.loads(file_content[0][:-1])
                for block in blockchain:
                    updated_blockchain = []
                    # Refactoring the converted_tx by using the instance of the Transaction class 
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount'], tx['signature']) for tx in block['transactions']]
                    # Used the instance of the Block class and passed the attribute values.
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], 0)
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                __open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for transaction in __open_transactions:
                    # Refactoring the updated_transactions by using the instance of the Transaction class 
                    updated_transactions = Transaction(transaction['sender'], transaction['recipient'], transaction['amount'], transaction['signature'])
                    updated_transactions.append(updated_transactions)
                self.__open_transactions = updated_transactions
                peer_node = json.loads(file_content[2])
                self.__peer_nodes = set(peer_node)
        # So, it is also an convention that every try block should be continued with atleast one "except" block.
        # The purpose of except block is to handle the errors which the try block couldn't handle and which eventually
        # throws an error and stops the execution of further code.
        # Python, also gives some in-built Error related Keywords which are related to general error causing scenarios.
        # For example, In this case (FileNotFoundError) can be used.
        except (FileNotFoundError, IndexError):
            print('Handled the exceptions')
        # Finally, is the another keyword which can be combined with try/catch block of code which can be used to handle
        # any code block irrespective of whether it is handled in try or except code block, this code in finally will execute.
        # This code block is usually good to execute any clean up work that has to be happening for the function.
        finally:
            print('cleanup has to be handled here.')
        
        self.load_data()

    # function to output the private attributes of the block__chain class to avoid accessing these attributes elsewhere
    # in the application and refactoring them which helps to avoid unseen errors.
    def return__chain(self):
        return self.__chain[:]
    
    def return_open_transactions(self):
        return self.__open_transactions[:]
    
        
    # Making the save_data() as the method of the blockchain. 
    # function to write file
    def save_data(self):
        # with - this is built in keyword in python when dealing with files and it ensures that the file closes
        # automatically once the execution of the code is done without using of close() method.
        # open() - The method open() takes in two parameters 
        # name of the file
        # mode in with the file has to be handled.

        # using pickle  
        # - the extension of the file is changed from .txt to .p to make the file compatiable with pickle library.
        # - the mode is also changed from 'w' to 'wb' indicating that pickle works with binary format when writing into a file.

        try:
            with open('blockchain.txt-{}'.format(self.node_id), mode='w') as f:
                # here, blockchain and open_transacations are in list format. But, appending into files only works with string format data.
                # so using str() on the blockchain to avoid errors.
                # Also, as we know since pickle writes only binary data the line escape charector is not handled in pickle file.
                # so, the work around is to store the data that has to be modified by the pickle package and escape the line escape. 
                # pickle_data = {
                #     'chain': blockchain,
                #     'ot': __open_transactions
                # }
                # json.dumps() - as we already know that json package in python is used to convert python dictionaries to stringified versions and vice-versa
                # So, inorder to convert python dictionaries to stringified version of lists of blockchain and __open_transactions into python native dictionary format json helps us with dumps() method.
                    
                # converting the block into dict format to mitigate the errors.
                blockchain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(blockchain))
                f.write('\n')
                __open_transactions = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(__open_transactions))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print('Unble to write data to the file.')


    # proof_of_work() - This is the function which takes care of implementing the "valid_proof" functionality on
    # every transaction by looping it to ensure all the transactions from the open transactions which will be added 
    # to the blockchain are verified and authenticated.
    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof
    

    # function to check the balances (amount sent and amount recieved) of the participants in the blockchain environemnt.
    # Implementing the double list comprehension technique where in the 
    #   - first list the result is retreving the transaction.
    #       - In this transaction checking the conditions that identifies the participant if sender or recipient.
    #   - second list the result is retriving the amount from the transaction based on the participant.
    #   - Once the values of the sender amount and recipient amount are extracted then looping through all the transactions to get the balance.   
    def get_balance(self, sender=None):
        # Adding a new validation check to check if the "sender is none".
        # This becomes an important validation check when doing a broadcast transaction, because in the broadcast transaction when adding a transasction,
        # get_balanance method is required, then if the peer_node is the one which is checked with this validation, then we are missing the check who is
        # sending the amount in case of peer_node.
        # In order to handle this case, in the get_balance method, we accept sender parameter and set it accordingly. 
        if sender == None:
            # Validation to check if the public_key exists in the blockchain when fetching the balance.
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
    # Since, we changed the data type of block from 'dictionary' to a class Object the attributes are not accessed by [] but by . notation.

    # Refactoring the tx_sender, open_transaction_sender by properly accessing the attributes of the Transaction class 
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_transaction_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        # Here, the sender is checked with the balance for his transactions both in open transactions and processed transactions in the blockchain.
        # the reduce() takes in three arguments in which the 
            # first is a function to handle the elements in the list.
            # second is a iterable 
            # third is the list of values to be returned as a result.
        tx_sender.append(open_transaction_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

        return amount_recieved - amount_sent
        

    # following a convention that each function should perform single task for implementing code redability
    # and maintainability in the application.
    def get_last_transaction_value(self):
        """ Function to return the last block from the blockchain."""
        # checking the length of the blockchain list so that conditional ouputting of blocks can be handled.
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    # This is the syntax for defining a function in python, which is defined with a "def" keyword
    # followed by name of the function and () and :
    # The second line of the function has to be indented to get identified by the python compiler
    # in order to execute the code.
    # setting the attribute is_recieving, to check if the get_balanace method being used is for peer_nodes or actual blockchain block.
    def add_transaction(self, recipient, sender, signature, amount=1.0, is_recieving = False):
        if self.public_key == None:
            return False
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
        transaction = Transaction(sender, recipient, amount, signature)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            # Here, in the add-transactions method, since the application is now in a position which is to be scaled to communicate with
            # other nodes, it is neccessary to think about a connection from within this application to other hosting sites (nodes.)
            # In order to make such a functionality in python, there is an package called "requests".
            #  And this has to be implemented on each node in the connection list, which can be done using the for loop.
            if not is_recieving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json = {
                            'sender': sender,
                            'recipient': recipient,
                            'amount': amount,
                            'signature': signature
                        })
                        if response.status_codes == 400 or response.status_codes == 500:
                            print('Server Error. Something went wrong.')
                            return False
                    except requests.exceptions.ConnectionError:
                        print('Unable to connect to the node.')
                        continue
            return True
        return False
        # append() -> It is the built in python method for the List data type used to add values to the
        # list at the end of the existing list.
        # The values in the list can be accessed with the position which are called "index" which starts
        # from 0.
        # blockchain(-1) ->. represents the accessibility to values from the right, usually it is from left.
        # print() -> it is another python method used to output the values in the terminal when executed.


    # Function repsonsible to mine blocks and add the open transactions to actual list of processed transactions.
    # In order to add the __open_transactions to processed transaction a hashing mechanism has to be implemented to make
    # the blockchain secure while mining the blocks.
    def mine_block(self):
        if self.public_key == None:
            return None
        try:
            last_block = self.__chain[-1]
            # As mining process has to be secured the hashing process becomes more important to be implemented.
            # For now a easy way to implement hashing is to used the stringified version of all the key values from the block.
            # In order to do so, lets loop through all the keys in the block dictionary and access the values and convert the
            # values to the string format.
            hashed_block = hash_block(last_block)
            proof = self.proof_of_work()
            # print(hashed_block, 'hashed_block_output')
            # mining_reward_transaction is a document which is added to the open transaction for the contribution to perfom mining.
            # mining_reward_transaction = {
            #     'sender': 'MINING',
            #     'recipient': owner,
            #     'amount': MINING_REWARD
            # }

            # Using OrderedDict to represent mining_reward_transaction dictionary
            mining_reward_transaction = Transaction('MINING', self.public_key, '', MINING_REWARD)
            
            # [:] -> Represents the range selector in a list which creates a copy of the original list of all the elements from start to end 
            copied_transactions = self.__open_transactions[:]
            for tx in copied_transactions:
                if not Wallet.verify_transactions(tx):
                    return None
            copied_transactions.append(mining_reward_transaction)
            # Refactored the block variable with "Block" class instance.
            block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
            self.__chain.append(block)
            # Resetting the blockchain to empty block once the mining of block is finished.
            self.__open_transactions = []
            self.save_data()
            return block
        except IndexError:
            print('List Index may be out of range.')
        finally:
            print('Mine block code completed...')

    # add_node() -> It is the function responsible to add the node to the blockchain.
    # the node attribute here, refers to the another system or an host url which is considered as another user using the blockchain
    # application once, the blockchain application goes live into the production environment.
    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    
    # remove_node() -> It is the function responsible to remove the node from the blockchain.
    # the node attribute here, refers to the another system or an host url which is considered as another user using the blockchain
    # application once, the blockchain application goes live into the production environment.
    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()


    # geet_peer_nodes() -> It is the function responsible to fetch all the nodes from the blockchain.
    def get_peer_nodes(self):
        return list(self.__peer_nodes)[:]

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
#     - blockchain (chain, __open_transactions, methods)
#     - block (previous_hash, index, timestamp, transactions, proof_of_work)
#     - transactions (sender, recipient, amount)
#     - verification (verification methods)
#     - node (UI for accepting the user inputs)
