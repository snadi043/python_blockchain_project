# Importing all the packages in order to create the REST API's in the blockchain application.
# Flask is like a framework similar to express on top of existing python http module using which the development of
# API's is easy instead of writing everything from the scratch.
# CORS - Cross Origin Request Frogery, It is a procedure that makes the server understand that requests coming from the same origin
# like the browser/client has to be enabled and provide the response accordingly.

from flask import Flask
from flask_cors import CORS
from wallet import Wallet

# Initializing the Flask framework in the application.
app = Flask(__name__)
wallet = Wallet()
# Implementing the CORS features on the app by wrapping it. 
CORS(app)

# GET method to handle the initial request to checking the server response on the browser.
@app.route('/', methods=['GET'])
def get_ui():
    return 'This is working...'

# Defining the host and the port for the server to run the application.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



