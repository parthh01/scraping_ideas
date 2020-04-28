from config import *
import math 
import matplotlib.pyplot as plt 
from pandas.plotting import register_matplotlib_converters
from mean_reversion import * 

register_matplotlib_converters() # pandas thing, just have to do it 

def plot_series_returns(series,label='SPY returns',starting_balance = 10000):
    starting_shares = math.floor(starting_balance/series.iloc[0])
    residue = starting_balance - starting_shares*series.iloc[0]
    sp_benchmark_return = (starting_shares*series.iloc[-1]) + residue 
    series['benchmark'] = starting_shares*series + residue 
    plt.plot(series['benchmark'],label = label)
    plt.legend()
    plt.ylabel('returns')
    plt.show()
    return sp_benchmark_return # returns portfolio value at end of backtest period 

# every day, loop through universe evaluate each test, buy/sell accordingly. 
# for active positions if limit price is between daily high/low position is sold
#sp_tickers = get_sp_tickers()

def run_mean_reversion_backtest(universe,backtest_period=365,lookback=100,start_balance=10000,max_halflife=7):
    start_day = datetime.date.today() - datetime.timedelta(days=1)
    end_day = start_day - datetime.timedelta(days=backtest_period)
    spy = api.polygon.historic_agg_v2('SPY',1,'day',_from=end_day,to=start_day).df
    start_bal = start_balance
    track_balance = [start_bal]
    current_balance = start_bal
    open_positions = {}
    new_position_multiplier = 0.1
    transaction_log = []
    def is_trading_day(day):
        if day in spy.index.date:
            return True
        return False 
    for i in range(1,backtest_period): 
        print('day {i}'.format(i=i))
        current_day = datetime.date.today()-datetime.timedelta(days=backtest_period-i) # first date is 2019-04-24 last day is 2020-04-21
        if is_trading_day(current_day): # evaluate strategy, assumed at market open
            for asset in universe:
                current_price_action = api.polygon.historic_agg_v2(asset,1,'day',_from=current_day,to=current_day + datetime.timedelta(days = 1)).df
                current_price = current_price_action['open'].iloc[0]
                if asset in open_positions: # look if position can be offloaded
                    if (current_price_action['low'].iloc[0] < open_positions[asset]['sellprice'] < current_price_action['high'].iloc[0]):
                        current_balance += open_positions[asset]['shares']*(open_positions[asset]['sellprice'] - open_positions[asset]['buyprice'])
                        transaction_log.append('sold {s} of {a} for {p} on {d}'.format(s = str(open_positions[asset]['shares']),a = asset,p = str(open_positions[asset]['sellprice']),d = str(current_day)))
                        del open_positions[asset]
                else: 
                    priceseries = api.polygon.historic_agg_v2(asset,1,'day',_from=current_day - datetime.timedelta(days=lookback),to=current_day).df
                    if half_life_test(priceseries['close']):
                        sma = priceseries['close'].rolling(max_halflife).mean()
                        sma_sd = sma.std()
                        is_potential_short = (current_price > (sma.iloc[-1] + sma_sd)) # what if margin is not significant? 
                        is_potential_long = current_price < (sma.iloc[-1] - sma_sd) # ditto 
                        if is_series_adf_stationary(priceseries['close']) and hurst_exponent_test(priceseries['close']) and variance_ratio_test(priceseries['close']):
                            if is_potential_long or is_potential_short:
                                funds = new_position_multiplier*current_balance
                                shares = math.floor(funds/current_price)
                                current_balance -= shares*current_price
                                if shares >= 1: 
                                    if is_potential_short:
                                        shares = -1*shares
                                    open_positions[asset] = {'buyprice':current_price,'shares':shares,'sellprice':sma.iloc[-1]}  #shares < 0 if short 
                                    transaction_log.append('bought {s} of {a} for {p} on {d}'.format(s = str(shares),a = asset,p = str(current_price),d = str(current_day)))
        track_balance.append(current_balance)
    plt.plot(track_balance,label='returns')
    plt.legend()
    plt.show()
    print(transaction_log)
    return current_balance,open_positions
                                
#run_mean_reversion_backtest(backtest_period=21)