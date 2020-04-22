from config import * 
from statsmodels.tsa.stattools import adfuller
from statsmodels.regression.linear_model import OLS 
from statsmodels.api import add_constant
from hurst import compute_Hc
from numpy import * 


lookback = 100 # number of days for dataset
# tickers = get_sp_tickers()

def is_series_adf_stationary(series): #adf evaluates whether or not time series cna be called stationary with 90% certainty
    adf_result = adfuller(series,maxlag=1)
    if adf_result[0] <= adf_result[4]['10%']:
        print(adf_result)
        return 'null hypothesis rejectable, with pval = {pval} '.format(pval=str(adf_result[1])) # series is mean reverting according to adf test 
    return None # series is not 


def evaluate_adf_stationarity(tickers):
    print('evaluating...')
    failed_tickers = []
    for asset in tickers: 
        try: 
            price_series = api.polygon.historic_agg_v2(asset,1,'day',_from=datetime.date.today()-datetime.timedelta(days =lookback),to=datetime.date.today()).df
            adf_test = is_series_adf_stationary(price_series['close'])
            if adf_test:
                print(asset + ' : ' + adf_test)
        except: 
            failed_tickers.append(asset)
    print('done')
    return failed_tickers


### statistical tests for mean reversion #####
def compute_hurst(ts): # hurst evaluates how strong the mean reversion is 
    # calculate standard deviation of differenced series using various lags
    lags = range(2, 20)
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    # calculate Hurst as slope of log-log plot
    m = polyfit(log(lags), log(tau), 1)
    hurst = m[0]*2.0
    return hurst

def variance_ratio_test(ts, lag = 2): # source: https://breakingdownfinance.com/finance-topics/finance-basics/variance-ratio-test/
    """
    Returns the variance ratio test result
    """
    # make sure we are working with an array, convert if necessary
    ts = asarray(ts)
    
    # Apply the formula to calculate the test
    n = len(ts)
    mu  = sum(ts[1:n]-ts[:n-1])/n
    m=(n-lag+1)*(1-lag/n)
    b=sum(square(ts[1:n]-ts[:n-1]-mu))/(n-1)
    t=sum(square(ts[lag:n]-ts[:n-lag]-lag*mu))/m
    vratio = t/(lag*b) # this is converted to a standardized test statistic by the following: 
    t_statistic = (sqrt(2*n)*(vratio-1))/sqrt(2) # this value should be between [-1.96,1.96] to reject null hypothesis with 5% significance
    return t_statistic

def compute_half_life(series): #moving average for the mean should be determined as some multiple of this beta 
    ylag = series.shift(1).dropna()
    deltay = (series - ylag).dropna()
    ylag = add_constant(ylag) 
    model = OLS(deltay,ylag)
    beta = model.fit().params[1] # regression_coefficient
    return -log(2)/beta # unit will be the barset time period (days)

    
asset = api.polygon.historic_agg_v2('CPB',1,'day',_from=datetime.date.today()-datetime.timedelta(days =lookback),to=datetime.date.today()).df
print('the hurst is {hurst}'.format(hurst = compute_hurst(log(asset[['close']])))) # the notation for calling price series is really odd
# hurst is strongly reverting closer to 0, 0.5 = no significance, and strongly trending closer to 1  
print(variance_ratio_test(log(asset['close'])))
print(compute_half_life(asset['close']))

# so, step 1 is evaluate adf to determine stationarity, 
# Step 2 is evaluate hurst exponent to determine strength of mean reversion/trending behaviour 0 < H < 0.25 ideal range ** needs to be proven 
# step 3 compute half life to determine moving average lookback period, and standard deviation to determine suitable entry
# step 4 compare suitable entry with current price and determine whether or not to enter trade 
# technically, the remainder of stocks that failed adf can be revaluated with the half life as the new period, if a small universe is considered like s&p


