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
open_positions = []
maxhalflife = 10
max_hurst = 0.40
new_pos_multiplier = 0.1 
stop_loss_margin = 0.10 # 10 percent 

universe = get_universe()
today = datetime.date.today().strftime("%m/%d/%Y")
dlimit = (datetime.date.today() - datetime.timedelta(days=3)).strftime("%m/%d/%Y") # so enough data is received even on a monday
traded_assets = []

while api.get_clock().is_open:
    for security in universe:
        try:
            if (security not in open_positions) and (security not in traded_assets):
                priceseries = api.polygon.historic_agg_v2(security,1,'minute',_from= dlimit,to=today,limit=lookback).df
                current_price = float(api.get_last_trade(security).price)
                if half_life_test(priceseries['close'],halflifelimit=maxhalflife):
                    sma = priceseries['close'].rolling(maxhalflife).mean()
                    sma_sd = sma.std()
                    is_potential_short = (current_price >= (sma.iloc[-1] + sma_sd)) # what if margin is not significant? 
                    is_potential_long = current_price <= (sma.iloc[-1] - sma_sd) 
                    if is_series_adf_stationary(priceseries['close']) and hurst_exponent_test(priceseries['close']) and variance_ratio_test(priceseries['close']) and (is_potential_short or is_potential_long):
                        funds = new_pos_multiplier*float(api.get_account().cash)
                        shares = math.floor(funds/current_price)
                        if shares >= 1: 
                            side = ('sell' if is_potential_short else 'buy')
                            try:
                                api.submit_order(
                                    symbol = security,
                                    side = side, 
                                    qty = shares,
                                    type = 'market',
                                    time_in_force = 'gtc',
                                    order_class = 'bracket', # not sure if this will work for sell, maybe oto will work better 
                                    take_profit = dict(
                                        limit_price = (sma.iloc[-1] - sma_sd) if side == 'buy' else (sma.iloc[-1] + sma_sd)
                                        ),
                                    stop_loss = dict(
                                        stop_price =  ((1-stop_loss_margin)*current_price if side == 'buy' else ((1+stop_loss_margin)*current_price)), # written so essentially will never come into effect
                                        limit_price = (((1-stop_loss_margin)*current_price)-0.01 if side == 'buy' else (((1+stop_loss_margin)*current_price)+0.01)) # maybe can be changed so its actually used 
                                        )
                                )
                                traded_assets.append(security)
                            except: 
                                print('error submitting order on {s}'.format(s=security))
        except:
            print('error evaluating {s}, skipped'.format(s=security))
    open_positions = [asset.symbol for asset in api.list_positions()]
    
print('markets closed')

    
    