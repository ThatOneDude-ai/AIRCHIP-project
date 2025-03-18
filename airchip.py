import hashlib
import json
from datetime import datetime
import random
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import requests

# --------------------------
# AirChip Token Calculation Functions
# --------------------------

# Your Alpha Vantage API key
API_KEY = "TKTW303LZCG3PS3R"

def fetch_stock_market_value(symbol):
    """
    Fetch the current closing price for the given stock symbol using the
    Alpha Vantage TIME_SERIES_DAILY endpoint.
    
    Parameters:
        symbol (str): The stock symbol (e.g., "IBM" or "AAPL").
        
    Returns:
        float: The latest closing price.
        
    Raises:
        ValueError: If the data for the symbol cannot be retrieved.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        time_series = data["Time Series (Daily)"]
        latest_date = sorted(time_series.keys(), reverse=True)[0]
        latest_data = time_series[latest_date]
        return float(latest_data["4. close"])
    except KeyError:
        raise ValueError(f"Could not retrieve data for symbol {symbol}. Response: {data}")

def fetch_today_transaction_count():
    """
    Simulate fetching the number of transactions created today.
    In a real-world scenario, this would come from a blockchain or transaction
    tracking API. Here we simply simulate it with a random number.
    
    Returns:
        int: Simulated transaction count.
    """
    return random.randint(10, 100)

def calculate_airchip_token_value():
    """
    Calculates the AirChip token value based on:
      - The current value of 'eggs' (IBM's stock price).
      - The current value of 'chickens' (AAPL's stock price).
      - The number of transactions created today (simulated).
    
    The formula is:
          token_value = ((egg_value / chicken_value) * 7) / transaction_count
    
    Returns:
        tuple: (token_value, egg_value, chicken_value, transaction_count)
    """
    egg_value = fetch_stock_market_value("IBM")
    chicken_value = fetch_stock_market_value("AAPL")
    transaction_count = fetch_today_transaction_count()
    
    if transaction_count == 0:
        raise ValueError("Transaction count must be greater than 0.")
    
    token_value = ((egg_value / chicken_value) * 7) / transaction_count
    return token_value, egg_value, chicken_value, transaction_count

# --------------------------
# Blockchain and Mining Classes
# --------------------------

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions  # list of transaction dicts
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        # Compute the block's hash (do not include the hash attribute itself)
        self.hash = self.compute_hash()

    def compute_hash(self):
        # Build a dictionary with the block's data (exclude the 'hash' attribute)
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 4  # Increased difficulty: requires hash to start with 4 zeros

    def __init__(self):
        self.unconfirmed_transactions = []  # Pending transactions
        self.chain = []
        self.token_ledger = {}  # Dictionary for token balances
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], str(datetime.now()), "0")
        self.chain.append(genesis_block)
        # Mint an initial supply for the genesis account
        self.token_ledger["genesis"] = 1_000_000

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        # Loop until a hash is found that satisfies the difficulty criteria
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        # Validate that the new block links correctly with the last block
        if self.last_block.hash != block.previous_hash:
            return False
        # Validate the proof of work
        if not proof.startswith('0' * Blockchain.difficulty) or proof != block.compute_hash():
            return False
        block.hash = proof
        self.chain.append(block)
        self.update_token_ledger(block.transactions)
        return True

    def update_token_ledger(self, transactions):
        for tx in transactions:
            sender = tx.get("from")
            recipient = tx.get("to")
            amount = tx.get("amount", 0)
            if sender not in ["genesis", "system"]:
                self.token_ledger[sender] = self.token_ledger.get(sender, 0) - amount
            self.token_ledger[recipient] = self.token_ledger.get(recipient, 0) + amount

    def add_transaction(self, sender, recipient, amount):
        if sender not in ["genesis", "system"]:
            if self.token_ledger.get(sender, 0) < amount:
                print(f"Insufficient funds for {sender}")
                return False
        tx = {
            "from": sender,
            "to": recipient,
            "amount": amount,
            "timestamp": str(datetime.now())
        }
        self.unconfirmed_transactions.append(tx)
        return True

    def solve_puzzle(self, parent):
        """
        Presents a tougher math puzzle using a GUI dialog.
        Returns True if solved correctly, False otherwise.
        """
        num1 = random.randint(10, 50)
        num2 = random.randint(10, 50)
        correct_answer = num1 + num2
        question = f"Puzzle Challenge: What is {num1} + {num2}?"
        user_answer = simpledialog.askinteger("Puzzle Challenge", question, parent=parent)
        if user_answer is None:
            messagebox.showinfo("Puzzle", "No answer provided. Puzzle failed.", parent=parent)
            return False
        if user_answer == correct_answer:
            messagebox.showinfo("Puzzle", "Correct! You've earned the full reward.", parent=parent)
            return True
        else:
            messagebox.showinfo("Puzzle", "Incorrect. You'll receive a reduced reward.", parent=parent)
            return False

    def mine(self, miner_address, parent):
        if not self.unconfirmed_transactions:
            messagebox.showinfo("Mining", "No transactions to mine.", parent=parent)
            return False

        # Ask via GUI if the user wants to try the bonus puzzle challenge
        if messagebox.askyesno("Bonus Puzzle", "Would you like to try a bonus puzzle challenge for extra tokens?", parent=parent):
            if self.solve_puzzle(parent):
                reward_amount = 30  # Full reward if puzzle solved
            else:
                reward_amount = 10  # Reduced reward if puzzle failed
        else:
            reward_amount = 10

        # Append the miner's reward transaction
        reward_tx = {
            "from": "system",
            "to": miner_address,
            "amount": reward_amount,
            "timestamp": str(datetime.now())
        }
        self.unconfirmed_transactions.append(reward_tx)

        new_block = Block(self.last_block.index + 1,
                          self.unconfirmed_transactions,
                          str(datetime.now()),
                          self.last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        # Clear pending transactions after block is mined
        self.unconfirmed_transactions = []
        return new_block.index

# --------------------------
# GUI Application using Tkinter
# --------------------------

class BlockchainGUI:
    def __init__(self, master):
        self.master = master
        master.title("AirChip Blockchain - Hybrid Mining")
        master.geometry("700x600")

        self.blockchain = Blockchain()

        # ScrolledText widget to display blockchain information
        self.display_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.display_area.pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=5)

        # Button to trigger mining of a new block
        self.mine_button = tk.Button(button_frame, text="Mine Block", command=self.mine_block)
        self.mine_button.grid(row=0, column=0, padx=5)

        # Button to add sample transactions (for demonstration)
        self.add_tx_button = tk.Button(button_frame, text="Add Sample Transactions", command=self.add_sample_transactions)
        self.add_tx_button.grid(row=0, column=1, padx=5)

        # Button to calculate AirChip token value
        self.calc_token_button = tk.Button(button_frame, text="Calculate AirChip Value", command=self.calculate_airchip_value)
        self.calc_token_button.grid(row=0, column=2, padx=5)

        # Update display with initial blockchain state
        self.update_display()

    def add_sample_transactions(self):
        # For demonstration, add two sample transactions
        self.blockchain.add_transaction("genesis", "alice", 100)
        self.blockchain.add_transaction("alice", "bob", 30)
        messagebox.showinfo("Transactions", "Sample transactions added.", parent=self.master)
        self.update_display()

    def mine_block(self):
        # Trigger mining for a hardcoded miner address (e.g., "miner1")
        block_index = self.blockchain.mine("miner1", self.master)
        if block_index:
            messagebox.showinfo("Mining", f"Block {block_index} mined!", parent=self.master)
        self.update_display()

    def calculate_airchip_value(self):
        """
        Calls the AirChip token value calculation function and displays
        the result along with the fetched data.
        """
        try:
            token_value, egg_value, chicken_value, tx_count = calculate_airchip_token_value()
            message = (
                f"IBM (Egg) closing price: {egg_value:.2f}\n"
                f"AAPL (Chicken) closing price: {chicken_value:.2f}\n"
                f"Simulated transaction count: {tx_count}\n\n"
                f"Calculated AirChip token value: {token_value:.4f}"
            )
            messagebox.showinfo("AirChip Token Value", message, parent=self.master)
        except Exception as e:
            messagebox.showerror("Error", f"Error calculating token value:\n{e}", parent=self.master)

    def update_display(self):
        # Clear the display area and update it with current blockchain and ledger information
        self.display_area.delete("1.0", tk.END)
        chain_info = "Blockchain:\n"
        for block in self.blockchain.chain:
            chain_info += (
                f"Block {block.index} [{block.timestamp}]:\n"
                f"  Hash: {block.hash}\n"
                f"  Previous: {block.previous_hash}\n"
                f"  Transactions: {block.transactions}\n"
                + "-" * 30 + "\n"
            )
        ledger_info = "Token Ledger:\n"
        for address, balance in self.blockchain.token_ledger.items():
            ledger_info += f"  {address}: {balance}\n"
        self.display_area.insert(tk.END, chain_info + "\n" + ledger_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainGUI(root)
    root.mainloop()
