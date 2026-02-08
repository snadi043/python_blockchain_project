# This class is the blueprint for the "block" in the blockchain application.
# This class and its attributes and methods are responsbile for providing the skeleton of a "block" in the application.
# Using this "block" class it is easy to structure the code in a more organized and reusable way.

# importing the "time" package to use it in the class to represent the timestamp value.
from time import time
# importing the "printable" class from the printable file to use it as inheritance concept in the Block class to see the class attributes.
from utilities.printable import Printable
# Every class has to start with a "class" keyword followed by name of the class in CamelCase format. 
# The below line represents the expression of inheritance in python.
class Block(Printable):
    # In order to use the attributes by every instance of the class without modifying the original class attributes
    # all the attributes have to be initialized by the method "__init__()"
    # Also, it is important convention that in python the default initially set values for the attributes has to to the last when initializing. 
    def __init__(self, index, previous_hash, transactions, proof, timestamp = None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time() if timestamp is None else timestamp
