from blockchain import Blockchain
from utilities.verification import Verification
from uuid import uuid4
from wallet import Wallet

# This file is responsible for representing the user choices of the blockchain application and all the functions from the 
# blockchain.py file are refactored into the methods of this Node class.
class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    # Function to fetch the transaction value/data which should now fetch recipient data and amount value.
    # The return type of the function is a tuple becasue it is supposed to be immutatble.
    def get_transaction_value(self):
        """ Function that is responsible to fetch the user inputs in the float format."""
        tx_recipient = input('Please enter the name of the recipient: ')
        tx_amount = float(input('Please enter an amount: '))
        return (tx_recipient, tx_amount)


    # Function to fetch the user input
    def get_user_choice(self):
        user_input = input('Choose an option: ')
        return user_input


    # Function to print blockchain elements.
    def print_blockchain_elements(self):
        # For loop is the in built python functionality which helps to loop through the iterable data types, here it is "list".
        # The syntax of for loop is as written below.
        for block in self.blockchain.return__chain():
            print('Outputting the blocks.')
            print(block)
        else:
            print('-' * 20)


    # function that is responsible to execute all the user choices from within the Node class
    def accepting_user_inputs(self):
        awaiting_input = True

        # While loop is another built in python functionality to loop infinetly till a condition is meet.
        # The syntax for the while loop is as follows.
        while awaiting_input:
            print('Choose an option from below.')
            print('1: Add a new transaction value.')
            print('2: Mine Block')
            print('3: Output the blocks of the blockchain.')
            print('4: Verify all transactions validity.')
            print('5: Create Keys')
            print('6: Load Keys')
            print('7: Save Keys')
            print('q: Quit')

            user_choice = self.get_user_choice()
            if user_choice == '1':
                # input() -> It is also an built in python method which accepts the user inputs from the terminal commandline.
                # float() -> It is a data type method to convert the usual user string input to required float format for tx.
                tx_data = self.get_transaction_value()

                # To execute the function just call it by the function name along with ().
                # To add_transaction, the tx_amount has to be passed as argument for which tuple unpacking is needed.
                #  Tuple unpacking is similar to using JS ES6 Feature of Spread and Rest operators.
                tx_recipient, tx_amount = tx_data
                signature = self.wallet.sign_transactions(self.wallet.public_key, tx_recipient, tx_amount)
                if self.blockchain.add_transaction(tx_recipient, self.wallet.public_key, signature, amount=tx_amount):
                    print('Successfully Added Transaction.')
                else:
                    print('Transaction Failed.')
                print(self.blockchain.return_open_transactions())    
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Unable to mine a block. Wallet not available.')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.return_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid.')
                else: 
                    print('Invalid transactions are present.')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                # break -> breaks the current execution and quits out of the loop
                # continue -> continue stops executing the current condition and starts the loop execution  from the first.
                awaiting_input = False
                # continue
            else:
                print('Invalid input. Please select something from the list of choices.')
            # print('Checking the continue execution.')
            if not Verification.verify_blockchain(self.blockchain.return__chain()):
                self.print_blockchain_elements()
                print('Invalid blockchain.')
                break
            # format() -> It is a python built in method which displays the values in a string according to the 
            # orders in which they are mentioned in the method. Format accepts any number of variables.
            # The placeholder for displaying the varibale values when using the format method also accepts the 
            # formating in terms of decimal notations and limit of charecters in the string.
            print('Balance of {} is {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
        print('DONE.')


# Configuiring __name__ and __main__
# Similar to all other dhunder (__) methods, python provides us with another dhunder method which is __main__
# The main purpose of __name__ and __main__ method, is to know whether the particular file is being executed when we call for 
# the file execution like python3 name_of_file.py
# or if the file is being imported when any other file is called by python and gets executed.

# This condition seems to be not so useful, until the condition which is similar to the below code.
# Here, we are calling for the execution of the node.py file and if this is the case then we start the process of executing
# the application accordingly by accepting the user inputs.

# checking the condition 
if __name__ == "__main__":
    node = Node()
    node.accepting_user_inputs()

print(__name__)
