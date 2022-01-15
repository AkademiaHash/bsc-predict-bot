from predict.strategies.BaseBot import BaseBot
from predict.classes.RoundClass import Round
from predict.classes.BetClass import Bet, Direction

from typing import Optional, List
import time
import logging
import ccxt
import pandas as pd
from telegramHandler import sendMessage

###pqp
# NOTE: Class must be named Bot
class Bot(BaseBot):
  def get_bet(self, upcoming: Round) -> Optional[Bet]:
    # YYYY-MM-DD
    # This function returns either a Bet or None based on the upcoming round.
    # If it returns a Bet, then that bet will be made
    # upcoming is the upcoming round that you're betting on

    # bet in the last 30 seconds
    timestamp = time.time()
    if upcoming.lockTimestamp - timestamp > 30:
      return None

    # you also have access to `self.history` which is the entire history of the games
    # At any time, there is an upcoming round that you can bet on, a `live` round that has not yet closed and the history
    # here we filter on completed rounds or rounds that closed
    completed = [r for r in self.history if r.oracleCalled]
    last_winner = completed[-1]

    # binance = ccxt.binance()
    # bars = binance.fetch_ohlcv('BNB/USDT','5m',limit=133)

    # df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close','vol'])
    # dfC = df['close']
    # sma50 = df['close'].rolling(50).mean()

    sendMessage(f"Last Winner: {last_winner.winner}, epoch: {last_winner.epoch}")
    return Bet(direction=Direction.BEAR, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
    # if (dfC.iloc[-1] < sma50.iloc[-1]):
    #   return Bet(direction=Direction.BULL, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
    # elif (dfC.iloc[-1] > sma50.iloc[-1]):
    #   return Bet(direction=Direction.BEAR, amount_eth=self.bet_size_eth, epoch=upcoming.epoch)
 #