# Importing all the packages in order to create the REST API's in the blockchain application.
# Flask is like a framework similar to express on top of existing python http module using which the development of
# API's is easy instead of writing everything from the scratch.
# CORS - Cross Origin Request Frogery, It is a procedure that makes the server understand that requests coming from the same origin
# like the browser/client has to be enabled and provide the response accordingly.

from flask import Flask, jsonify
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

# Initializing the Flask framework in the application.
app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
# Implementing the CORS features on the app by wrapping it. 
CORS(app)

# GET method to handle the initial request to checking the server response on the browser.
@app.route('/', methods=['GET'])
def get_ui():
    return 'This is working...'

# GET method to handle the respose to display the list of blocks in the blockchain.
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    blockchain_snapshot = blockchain.return__chain()
    # converting the blockchain list into a dictionary to avoid python parsing erros. 
    dict_blockchain_snapshot = [block.__dict__.copy() for block in blockchain_snapshot]
    # Also changing the internal data and its data type to avoid errors with respect to transactions.
    for dict_blockchain_block in dict_blockchain_snapshot:
        dict_blockchain_block['transactions'] = [tx.__dict__ for tx in dict_blockchain_block['transactions']]
    return jsonify(dict_blockchain_snapshot), 200

# GET method to handle the response to fetch the keys with respect to the wallet of the user
@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key
        }
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify(response), 200
    else:
        response = {
            'message': 'Unable to load keys.',
        }
        return jsonify(response), 500


# POST method to handle the response to post the keys with respect to the wallet of the user
@app.route('/wallet', methods=['POST'])
def save_keys():
    wallet.create_keys()
    if wallet.save_keys():
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key
        }
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        return jsonify(response), 201
    else:
        response = {
            'message': 'Unable to save keys.',
        }
        return jsonify(response), 500

# POST method to handle the response to add the block into the blockchain
@app.route('/mineblock', methods=['POST'])
def mineblock():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy() 
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Successfully added block to blockchain',
            'block': dict_block
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Unable to add the block.',
            'wallet-setup': wallet.public_key != None
        }
        return jsonify(response), 500


# Defining the host and the port for the server to run the application.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



