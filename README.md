AirChip Blockchain & Cryptocurrency Project
=============================================

Overview
--------
AirChip is a hybrid blockchain project that integrates real-time stock market data with a custom token valuation algorithm.
The token value is determined by the ratio of the closing prices of two stocks (IBM representing "eggs" and AAPL representing "chickens"),
multiplied by 7 and normalized by the number of transactions created that day. This unique mechanism links real-world market data
to the value of the cryptocurrency, making it dynamic and reflective of current financial trends.

Token Value Calculation
-----------------------
The AirChip token value is calculated using the following formula:

    token_value = ((IBM_closing_price / AAPL_closing_price) * 7) / transaction_count

Where:
- **IBM_closing_price**: The most recent daily closing price of IBM (used as the "egg" value).
- **AAPL_closing_price**: The most recent daily closing price of AAPL (used as the "chicken" value).
- **transaction_count**: A simulated count of transactions for the day.

The integration with the Alpha Vantage API (using your provided API key) ensures that IBM and AAPL prices are updated in real time.
The current token rate is dynamically calculated each time the "Calculate AirChip Value" button is pressed in the GUI.

Current Token Rate
------------------
At runtime, the project will display the current token rate based on the live stock data and the simulated transaction count.
For example, if at the time of execution:
    - IBM closing price is $125.23
    - AAPL closing price is $190.45
    - Simulated transaction count is 50
then the token value would be calculated as follows:

    ratio = 125.23 / 190.45 ≈ 0.6575
    adjusted value = 0.6575 * 7 ≈ 4.6025
    token value = 4.6025 / 50 ≈ 0.0921

Thus, the current AirChip token rate would be approximately 0.0921. (Note: Actual numbers will vary with live data.)

Features
--------
- **Blockchain Implementation**: 
  - Custom proof-of-work algorithm with adjustable difficulty.
  - Transaction management and token ledger updates.
- **Hybrid Token Calculation**:
  - Integrates live market data from Alpha Vantage.
  - Uses a unique formula linking stock prices and transaction volume.
- **User-Friendly GUI**:
  - Built with Tkinter for easy interaction.
  - Allows mining, adding sample transactions, and calculating the token value.
- **Puzzle-Based Mining Bonus**:
  - Optional bonus puzzle challenge to earn extra tokens during mining.

Installation & Running the Project
------------------------------------
1. **Prerequisites**:
   - Python 3.x installed on your system.
   - Required Python packages: `requests`, `tkinter` (usually included with Python).

2. **Clone the Repository**:

3. **Set Up**:
- Ensure your Alpha Vantage API key is correctly set in the `airchip.py` script.

4. **Run the Project**:

5. **Using the GUI**:
- Click "Add Sample Transactions" to populate the blockchain with example transactions.
- Click "Mine Block" to mine a new block and earn rewards.
- Click "Calculate AirChip Value" to fetch current market data and see the live token rate.

Support & Contributions
-----------------------
If you encounter any issues or have suggestions for improvement, please open an issue or submit a pull request on GitHub.

License
-------
This project is released under the MIT License.

Enjoy building and exploring the unique world of AirChip!
