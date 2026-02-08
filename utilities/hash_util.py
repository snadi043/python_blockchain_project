# hashlib is a python package which is packed with hashing related functions/methods which are useful in this application.
# This package is imported from python standard library.
import hashlib
# json is another python built in library to convert the data types into strings and vice-versa.
import json

def hash_256(string):
    return hashlib.sha256(string).hexdigest()

# Function to generate the hashed output of a transaction by expecting a block a input.
def hash_block(block):
    # return '-'.join([str(block[keys]) for keys in block])
    # sha256() - this is a hashing algorithm which is designed to generate the 64 bit hash codes for identical inputs and 
    # ensures that for every input the hash remains same and cannot be altered. 
    # block - here the data format of the block is a dictonary but sha256() accepts "string" types only.
    # so json() - this is used to convert the dictionary into stringified version by using it's internal method dumps().
    # hexdigest() - Return the digest value as a string of hexadecimal digits.
    # sort_keys = True - Ensures that all the key, value pairs in the dictionary stay always in the same order. 
    
    # converting the block into dict format to mitigate the errors.
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_256(json.dumps(hashable_block, sort_keys=True).encode())

# from the data type module in python, we have seen that in python dictionaries are internally unordered map.
# which means when a dictionary is being used in the code there are chances that can happen during the (processing of code or linting of the code,
# execution of code or assigning the memory to the variables by python from the code) the order of the (key,value) pairs in the dictionary might change.
# For example, If that sligthest mistake has happend in the application, then the hashing mechanism can be exposed to a bug and can cause big damange.
# So to avoid this from happening, we can do a work around by dealing with "sort_keys and Ordered dictionaries".
