from mean_reversion import * 
from backtest import * 


#print(api.polygon.historic_agg_v2('SPY',1,'minute',_from=today - datetime.timedelta(days=7),to=today,limit = 100).df)

def get_universe():
    try: 
        alpaca_list = [asset.symbol for asset in api.list_assets() if (asset.tradable and asset.shortable)]
        sp_tickers = get_sp_tickers()
        universe = [ticker for ticker in sp_tickers if (ticker in alpaca_list)] 
        return universe 
    except: 
        print('error initializing')

#OPTIMIZABLE VARIABLES: 
lookback = 100 
open_positions = [] # schema:- {security: {sellprice:int, shares: int, side: 'buy' or 'sell'}}
maxhalflife = 10
max_hurst = 0.40
new_pos_multiplier = 0.1 

universe = get_universe()
today = datetime.date.today()
dlimit = today - datetime.timedelta(days=3) # so enough data is received even on a monday


while api.get_clock().is_open:
    for security in universe:
       if security not in open_positions:
            priceseries = api.polygon.historic_agg_v2(security,1,'minute',_from= dlimit,to=today,limit= lookback).df
            current_price = priceseries['close'].iloc[-1]
            if half_life_test(priceseries['close'],halflifelimit=maxhalflife):
                sma = priceseries['close'].rolling(maxhalflife).mean()
                sma_sd = sma.std()
                is_potential_short = (current_price > (sma.iloc[-1] + sma_sd)) # what if margin is not significant? 
                is_potential_long = current_price < (sma.iloc[-1] - sma_sd) 
                if is_series_adf_stationary(priceseries['close']) and hurst_exponent_test(priceseries['close']) and variance_ratio_test(priceseries['close']) and (is_potential_short or is_potential_long):
                    funds = new_pos_multiplier*api.get_account().cash
                    shares = math.floor(funds/current_price)
                    if shares >= 1: 
                        side = ('sell' if is_potential_short else 'buy')
                        api.submit_order(
                            symbol = security,
                            side = side, 
                            qty = shares,
                            time_in_force = 'gtc',
                            order_class = 'bracket',
                            take_profit = dict(
                                limit_price = sma.iloc[-1]
                                ),
                            stop_loss = dict(
                                stop_price =  math.floor(sma.iloc[-1]/2), # written so essentially will never come into effect
                                limit_price = math.floor(sma.iloc[-1]/2) - 0.01 # maybe can be changed so its actually used 
                                )
                        )
                        open_positions.append(security)
    