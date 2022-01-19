# binance-grid-bot
This program implements a grid strategy trading bot on Binance using API keys.

<strong>About the trading strategy:</strong>
The grid trading strategy performs well when the trading pair oscillates within a predefined price range.
The bot is launched with an equal amount of currency on each side of the pair; sell and buy limit orders are placed in an evenly spaced manner, respectively above and below the current pair price, all the way to the interval's higher and lower bounds.
When a sell order is executed, it is replaced by a buy order 1 rung (i.e. the trading grid's interval) below. Likewise, an executed buy order is replaced by a sell order 1 rung above.

<strong>How to run the app:</strong>

<strong>Prerequisites:</strong>
1) the app runs with Python3
2) you need to have your Binance API_key and API_secret stored as environment variables
3) you need to pip install the following Python packages:
    - python-binance, to interact with the Binance API
    - pickle, to store information about your trading bots objects in local files
    - inquirer, to be able to select the bot you want to interact with from the CLI
4) i recommend running the app from a remote server, so that the cron job can run when your own computer is not turned on

<strong>To run the app</strong>:
- run python3 app.py
- select option number 1 by pressing 1
- choose each currency of the pair; you need to have a non-nul balance in at least 1 of the 2 currencies
- choose the amount of quote currency you want to invest on each side

<strong>To have the bot rebalance orders every minute</strong>: write the following cron job: * * * * * python3 path_to_repo/binance_bot/adjust_grid.py

<strong>To check on your bot:</strong>
- Option 1 - Use the display_grid.py script:
    - run python3 app.py
    - select option number 2 by pressing 2
    - the script will make you choose among the active bots for the selected pair
    - you will be able to see the current grid

- Option 2 - Read the log file:
    - in the binance_bot repo, access the gridbots folder followed by the right currency pair folder
    - you will be able to see snapshots of the order grid over time

<strong>To disable your bot:</strong>
- run python3 app.py
- select option number 3 by pressing 3
- all standing orders associated with your bot will be cancelled
- your bot file and log file will be marked as disabled
