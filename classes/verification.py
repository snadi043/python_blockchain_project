# This file represents the verification class in which the methods from the "blockchain.py" file are executed to reuse them efficiently.

# Importing own custom modules from another file withing the application.
from hash_util import hash_256, hash_block
class Verification:
    # Function to check the authenticity of a transaction.
    @staticmethod
    def verify_transaction(transaction, get_balance):
        # Refactoring the balance by correctly accessing the attributes of the instance of the Transaction class. 
        sender_balance = get_balance()
        return sender_balance >= transaction.amount
    
    
    # Function to verify all the transactions.
    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all ([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
    

    # valid_proof() - This is the function defined to verify the refactored hashing mechanism.
    # This function accepts three parameters
        # transactions -> these are all the transactions in the blockchain
        # previous_hash -> the hash value from the previous transactions in the blockchain
        # proof -> the code/identification that is integrated into the hash string to then verify among every transaction.
    @staticmethod
    def valid_proof(transactions, previous_hash, proof):
        # Using the Transaction class method "to_ordered_dict" on each transaction in the transactions dictionary.
        hash = (str([tx.to_ordered_dict() for tx in transactions]) + str(previous_hash) + str(proof)).encode()
        hashed_str = hash_256(hash)
        print(hashed_str)
        return hashed_str[0:2] == '00'

    # Function to verify the blockchain is valid by comparing the previous blocks in the blockchain by their values.
    @classmethod
    def verify_blockchain(cls, blockchain):
        # modifying the verify_blockchain function which verifies the current block with previous blocks.
        # Veification is done by comparing the hash key values which is "previous_hash" in every block.
        # So in order to compare the list [blockchain] with the dictionary {transaction} in a loop, python has a build in
        # method called enumerate -> enumerate() converts the list into tuple which in terms looks alike like a dictionary. 
        for (index, block) in enumerate(blockchain):
            # print(block, 'verify_block')
            if index == 0:
                continue
            # Correctly accessing the class attributes of the block from its class instance.
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            # Correctly accessing the class attributes of the block from its class instance.
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is not valid.')
                return False
        return True


    

# In python when dealing with classes, there is a flexibility to combine the 
# methods of the class as per how each attribute and each method in the class is being used.
# To do so, python gives us the features called decorators and annotations, using which we can modify the methods in a class.

# classmethod
# @classmethod - The classmethod is used, when a method in the class accepts the attributes from the class and uses it in its method.
#              - The method which is converted into the classmethod will be replaced with "cls" instead of "self" in its constructor.
#              - This "cls" keyword helps to access the "attributes / methods" from the class to use it in the method.
# staticmethod
# @staticmethod - The staticmethod is used, when a method in the class doesn't deal with any attributes/methods from the class
#               - instead, does perform the tasks by its own then those methods can be converted into static methods.

# The purpose of using the above mentioned classmethods and staticmethods is to handle the use of more instances of a class whenever
# needed in the application. So, with these decorators the classes and their methods can be easily accessed without calling instances of the class.