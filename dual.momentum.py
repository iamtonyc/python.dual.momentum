import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
import matplotlib.dates as date
import datetime
%matplotlib inline
from numpy.random import randn

#SPY
spyDf=pd.read_csv('SPY.csv',index_col='Date',parse_dates=True)
spyDailyReturns = spyDf['Adj Close'].pct_change()
spyMonthlyReturns = spyDf['Adj Close'].resample('M').ffill().pct_change()
spyMonthlyReturnsDf = pd.DataFrame(spyMonthlyReturns) 
spyLast12MonthSum = spyMonthlyReturnsDf['Adj Close'].rolling(window=12).sum()
spyLast12MonthSumDf = spyLast12MonthSum.to_frame()

#ACWX
acwxDf=pd.read_csv('ACWX.csv',index_col='Date',parse_dates=True)
acwxDailyReturns = acwxDf['Adj Close'].pct_change()
acwxMonthlyReturns = acwxDf['Adj Close'].resample('M').ffill().pct_change()
acwxMonthlyReturnsDf = pd.DataFrame(acwxMonthlyReturns) 
acwxLast12MonthSum = acwxMonthlyReturnsDf['Adj Close'].rolling(window=12).sum()
acwxLast12MonthSumDf = acwxLast12MonthSum.to_frame()


#AGG
aggDf=pd.read_csv('AGG.csv',index_col='Date',parse_dates=True)
aggDailyReturns = aggDf['Adj Close'].pct_change()
aggMonthlyReturns = aggDf['Adj Close'].resample('M').ffill().pct_change()
aggMonthlyReturnsDf = pd.DataFrame(aggMonthlyReturns) 
aggLast12MonthSum = aggMonthlyReturnsDf['Adj Close'].rolling(window=12).sum()
aggLast12MonthSumDf = aggLast12MonthSum.to_frame()


mergeDf = pd.merge(left=spyLast12MonthSumDf,right=acwxLast12MonthSumDf, left_on='Date', right_on='Date')
mergeDf = pd.merge(left=mergeDf,right=aggLast12MonthSumDf, left_on='Date', right_on='Date')
mergeDf.rename(columns={'Adj Close_x':'SPY','Adj Close_y':'ACWX','Adj Close':'AGG'},inplace=True)

mergeDf=mergeDf[mergeDf.ACWX.notnull()]
mergeDf=mergeDf.sort_values('Date',ascending=False)

mergeDf.loc[(mergeDf['SPY'] >= mergeDf['ACWX']) & (mergeDf['SPY'] >= mergeDf['AGG']), 'Buy'] = 'SPY' 
mergeDf.loc[(mergeDf['ACWX'] >= mergeDf['SPY']) & (mergeDf['ACWX'] >= mergeDf['AGG']), 'Buy'] = 'ACWX' 
mergeDf.loc[(mergeDf['AGG'] >= mergeDf['SPY']) &  (mergeDf['AGG'] >= mergeDf['ACWX']), 'Buy'] = 'AGG' 

print(mergeDf.head(20)) 