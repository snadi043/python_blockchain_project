# This file represents the verification class in which the methods from the "blockchain.py" file are executed to reuse them efficiently.

# Importing own custom modules from another file withing the application.
from hash_util import hash_256, hash_block
class Verification:
    # Function to check the authenticity of a transaction.
    def verify_transaction(self, transaction, get_balance):
        # Refactoring the balance by correctly accessing the attributes of the instance of the Transaction class. 
        sender_balance = get_balance()
        return sender_balance >= transaction.amount
    
    
    # Function to verify all the transactions.
    def verify_transactions(self, open_transactions, get_balance):
        return all ([self.verify_transaction(tx, get_balance) for tx in open_transactions])
    

    # valid_proof() - This is the function defined to verify the refactored hashing mechanism.
    # This function accepts three parameters
        # transactions -> these are all the transactions in the blockchain
        # previous_hash -> the hash value from the previous transactions in the blockchain
        # proof -> the code/identification that is integrated into the hash string to then verify among every transaction.
    def valid_proof(self, transactions, previous_hash, proof):
        # Using the Transaction class method "to_ordered_dict" on each transaction in the transactions dictionary.
        hash = (str([tx.to_ordered_dict() for tx in transactions]) + str(previous_hash) + str(proof)).encode()
        hashed_str = hash_256(hash)
        print(hashed_str)
        return hashed_str[0:2] == '00'

    # Function to verify the blockchain is valid by comparing the previous blocks in the blockchain by their values.
    def verify_blockchain(self, blockchain):
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


    



