# binance-grid-bot
This program implements a grid strategy trading bot on Binance using API keys.

<h4><strong>About the trading strategy:</strong></h4>
The grid trading strategy performs well when the trading pair oscillates within a predefined price range.
The bot is launched with an equal amount of currency on each side of the pair; sell and buy limit orders are placed in an evenly spaced manner, respectively above and below the current pair price, all the way to the interval's higher and lower bounds.
When a sell order is executed, it is replaced by a buy order 1 rung (i.e. the trading grid's interval) below. Likewise, an executed buy order is replaced by a sell order 1 rung above.

<h4><strong>How to run the app:</strong></h4>

<strong>Prerequisites:</strong>
1) the app runs with Python3
2) you need to have your Binance API_key and API_secret stored as environment variables
3) you need to pip install the following Python packages:
    - python-binance, to interact with the Binance API
    - pickle, to store information about your trading bots objects in local files
    - inquirer, to be able to select the bot you want to interact with from the CLI
4) i recommend running the app from a remote server, so that the cron job can run when your own computer is not turned on

<strong>To launch the bot</strong>:
- run python3 launch_bot.py
- choose each currency of the pair; you need to have a non-nul balance in at least 1 of the 2 currencies

<strong>To have the bot rebalance orders every minute</strong> (WORK IN PROGRESS, AS SOME EXECUTED ORDERS ARE SOMETIMES NOT DETECTED):
- write the following cron job: * * * * * python3 path_to_repo/binance_bot/adjust_grid.py

<strong>To check on your bot:</strong>
Option 1: Use the display_grid.py script
- run display_grid.py
- the script will make you choose among the active bots
- you will be able to see the current grid

Option 2: Read the log file
- in the binance_bot repo, access the gridbots folder followed by the right currency pair folder
- you will be able to see snapshots of the order grid at 1 minute intervals, when the adjust_grid.py script is run automatically by the cron job

<strong>To disable your bot:</strong>
- run disable_bot.py
- all standing orders associated with your bot will be cancelled
- your bot file and log file will be marked as disabled
