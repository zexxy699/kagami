import threading
import time
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://bsc-mainnet.infura.io/v3/1b08771457fe4017bbd57098a3e9d979"))

private_key = "6fba4eca092b7844c0b2f1ed18a0daa9ce19f932201ab198549602dfdd44b47f"
pub_key = "0x6B9B145Ab96A8Df18C61d401D25fa211f663802d"
recipient_pub_key = "0x0ba49A888b40F36912291d8D456D5Ebfcad1D4aC"

def loop():
    while True:
        try:
            balance = w3.eth.get_balance(pub_key)
            print(f"Current balance: {balance} wei")

            # Check if balance is greater than 0
            if balance > 0:
                gas_price = w3.eth.gas_price  # Dynamically fetch gas price
                gas_limit = 21000
                estimated_gas_cost = gas_limit * gas_price

                # Ensure the transaction value does not go below gas costs
                if balance > estimated_gas_cost:
                    nonce = w3.eth.get_transaction_count(pub_key)
                    tx = {
                        'chainId': 56,  # BSC mainnet chain ID
                        'nonce': nonce,
                        'to': recipient_pub_key,
                        'value': balance - estimated_gas_cost,
                        'gas': gas_limit,
                        'gasPrice': gas_price
                    }

                    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
                    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    print(f"Transaction sent with hash: {w3.toHex(tx_hash)}")
                else:
                    print("Insufficient funds to cover gas costs for withdrawal.")
            else:
                print("No funds to withdraw.")

        except Exception as e:
            print(f"Error occurred: {e}")

        time.sleep(1)  # Check every 10 seconds

threading.Thread(target=loop, daemon=True).start()
input('Press Enter to exit.')
