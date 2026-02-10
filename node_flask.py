from flask import Flask
from flask_cors import CORS

from wallet import Wallet

wallet = Wallet()

app = Flask(__name__)
CORS(app)