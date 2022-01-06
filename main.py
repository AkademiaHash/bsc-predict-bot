import argparse
from dotenv import load_dotenv
import os
import strategies

if __name__ == "__main__":
  load_dotenv()
  
  parser = argparse.ArgumentParser(description='Trading bot for Pancake Swap Prediction Markets or BSC-Predict')
  parser.add_argument(
    '--strategy',
    dest='strategy',
    action='store',
    required=True,
    help="Strategies are file names defined in the strategies/ folder (e.g. SimpleBot)"
  )
  parser.add_argument(
    '--size',
    dest='size_eth',
    action='store',
    type=float,
    required=True,
    help="Amount in eth to bet",
  )
  parser.add_argument(
    '--min',
    dest='min_balance_eth',
    action='store',
    type=float,
    required=False,
    default=0,
    help="The minimum balance of your account before the bot stops playing",
  )
  parser.add_argument(
    '--dry',
    dest='dry',
    action='store_true',
    required=False,
    default=False,
    help="Dry run",
  )


  SECRET_KEY = os.getenv('secret')
  ACCOUNT = os.getenv('account')

  args = parser.parse_args()
  strategy = args.strategy
  bet_size_eth = args.size_eth
  min_balance_eth = max(0, args.min_balance_eth)

  if (SECRET_KEY is None and not args.dry):
    raise Exception("SECRET_KEY is not defined in .env")
  elif (ACCOUNT is None and not args.dry):
    raise Exception("ACCOUNT is not defined in .env")

  
  __import__(f'strategies.{strategy}', locals(), globals())
  import strategies

  bot = getattr(strategies, strategy)
  bot = bot.Bot(dry=args.dry, account=ACCOUNT, secret_key=SECRET_KEY, bet_size_eth=bet_size_eth, min_balance_eth=min_balance_eth)
  bot.run()

