# Importing all the packages in order to create the REST API's in the blockchain application.
# Flask is like a framework similar to express on top of existing python http module using which the development of
# API's is easy instead of writing everything from the scratch.
# CORS - Cross Origin Request Frogery, It is a procedure that makes the server understand that requests coming from the same origin
# like the browser/client has to be enabled and provide the response accordingly.

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain

# importing the package "ARGUMENT PARSER", to add/configure arguments to the commands in the terminal.
# Here, in order to scale the blockchain functionality to work with multiple nodes, it is important to run the application
# over multiple ports, for which it is important to use argmentParser and set port arguments.
from argparse import ArgumentParser

# Initializing the Flask framework in the application.
app = Flask(__name__)

parser = ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=5000)
args = parser.parse_args()
print(args, 'args')
port = args.port
# Configuring to Initialize the wallet and the blockchain classes in every hosting machine with respect to the port specified
# in the command line inorder to provision the multiple nodes functionality.
wallet = Wallet(port)
blockchain = Blockchain(wallet.public_key, port)

# Defining the host and the port for the server to run the application.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)

# Implementing the CORS features on the app by wrapping it. 
CORS(app)

# GET method to handle the GET request to render the server response on the browser for fetching the landing page.
@app.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')


# GET method to handle the GET request to render the server response on the browser for fetching the network page.
@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')

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
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
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
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Unable to save keys.',
        }
        return jsonify(response), 500

# POST method to handle the response to add the block into the blockchain
@app.route('/mineblock', methods=['POST'])
def mineblock():
    if blockchain.resolve_conflict:
        response = {
            'message': 'Resolve conflicts first, blocks are missing'
        }
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy() 
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Successfully added block to blockchain',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Unable to add the block.',
            'wallet-setup': wallet.public_key != None
        }
        return jsonify(response), 500

# GET method to handle the response to fetch the balance with respect to the wallet of the user.
@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Successfully fetched the balance.',
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Unable to fetch the balance.',
            'wallet_setup': wallet.public_key != None
        }
        return jsonify(response), 500

# GET method to handle the response to fetch all the transactions.
@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = blockchain.return_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


# POST method to handle the response to post the transaction with respect to the input given by the user using request().
@app.route('/add-transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'Wallet is not available.'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'User Input Values are not fetched.'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all (field in values for field in required_fields):
        response = {
            'message': 'Required fields in the transactions are not available.',
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transactions(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': 'Successfully added all the transaction data.',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Unable to add transaction to the blockchain.'
        }
        return jsonify(response), 500
    

@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Values needed from the broadcast transactions doesnot exists.'
        }
        return jsonify(response), 400
    required_values = ['sender', 'recipient', 'amount', 'signature']
    if not all (key in values for key in required_values):
        response = {
            'message': 'Some values required are missing.'
        }
        return jsonify(response), 400
    success = blockchain.add_transaction(values['recipient'], values['sender'], values['signature'], values['amount'], is_recieving=True)
    if success:
        response = {
            'message': 'Successfully added transaction',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'signature': values['signature'],
                'amount': values['amount']
            }
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Unable to add transaction to the blockchain.'
        }
        return jsonify(response), 500


# broadcast_block is the method which is triggered and is designed to take action when peer node blocks are to matched on all the nodes
# of the blockchain application, because only then it is possible to make proper transactions from peer_nodes and blockchain nodes and open_transactions.
@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Unable to find the values from the request object.'
        }
        return jsonify(response), 400
    if not 'block' in values:
        response = {
            'message': 'The block value from the values request object is missing.'
        }
        return jsonify(response), 400
    block = values['block']
    # this is the condition to check if current block index is same than the incoming block index.
    # this is the case which is accurate to add the transaction to the blockchain and can confirm there are no missing block in between.
    if block['index'] == blockchain.__chain[-1].index:
        if blockchain.add_block(block):
            response = {
                'message': 'Block added successfully'
            }
            return jsonify(response), 201
        else: 
            response = {
                'message': 'Block seems to be invalid'
            }
            return jsonify(response), 500
    elif block['index'] > blockchain.__chain[-1].index + 1: 
        blockchain.resolve_conflict = True
        response = {
            'message': 'The Local blockchain is shorter and is missing the nodes from the peer nodes.',
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'Missing blocks in between the transactions.'
        }
        return jsonify(response), 409


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'message': 'Successfully fetched all the peer nodes.',
        'peer_nodes': nodes
    }
    return jsonify(response), 200


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'Something went wrong.'
        }
        return jsonify(response), 401
    if 'peer_nodes' not in values:
        response = {
            'message': 'Node details not available.'
        }
        return jsonify(response), 402
    node = values['peer_nodes']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Successfully added the peer node to the blockchain network.',
        'peer_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
            'message': 'Node not found to delete.'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Successfully deleted the node from the blockchain network.',
        'peer_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200





