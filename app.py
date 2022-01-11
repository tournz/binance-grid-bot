print("Welcome to the Binance grid bot program")
print("What do you want to do?")
print("1- Launch a new bot")
print("2- Check on an existing bot")
print("3- Disable a bot")

choice = int(input())
if choice == 1:
   exec(open("launch_bot.py").read())
elif choice == 2:
   exec(open("display_grid.py").read())
elif choice == 3:
   exec(open("disable_bot.py").read())
else:
   print("Please choose 1, 2 or 3")
