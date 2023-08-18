
# Step 1  : Import Dependent library
import pandas as pd
from datetime import datetime as dt , datetime
import plotly.graph_objects as go

"Variable defining"
mtype ="type"
mClose = "close"
mOpen = "open"
mhigh = "high"
mLow = "low"
mVolume = "volume"
mOi = "oi"
mDate = "date"
mMA10 = "MA10"
mMA20 = "MA20"
mMA50 = "MA50"
mMA29 = "MA29"
mMA100 = "MA100"

"""Step 2: Load CSV file into memory """
path = ".//Data//512023+2023-01-05.csv"
df = pd.read_csv( path )
print(df)

#  Allow Data from  Range( 9:15 to 15:30)   //2023-01-05 14:54:00
# df["Date"] =  pd.to_datetime(df[mDate] , format='%Y-%m-%d').dt.date

""" EXTRACT or  SET OUR STRATEGY TARDING(CALCULATION) TIME """
df[ "Time" ] = pd.to_datetime( df[ mDate ] ).dt.time

filterdata = (df[ "Time" ] >= datetime.strptime( "09:15:00" , '%H:%M:%S' ).time( )) & (
            df[ "Time" ] <= datetime.strptime( "15:20:00" , '%H:%M:%S' ).time( ))

# df["Timer"] =pd.to_datetime(df[mDate] , format= '%H' )
df = df.where( filterdata ).dropna( )

"""Step3 : Extract FUTURE Data : 
# logic : type == "XX" -> as Future

"""

filterxx = (df[ mtype ] == "XX")  & (df["strike"] == 1)
df_future = df.where( filterxx ).dropna()
# df_future = df_future.dropna( )
# print(df_future)

"""Step4 : Extract option Data :
# logic : type != "XX" -> as options   or || type == "CE" || type ="PE"
"""

fitercepe = df[ mtype ] != "XX"  # df[mtype] == "PE"
# fitercedatetime915to330 =
df_options = df.where( fitercepe )
df_options = df_options.dropna( )
# print(df_options)

"""CALCULATE moving Average """


""" WHILE BACK TESTING (I Got Best Result) """
# df_future[ mMA10 ] = df_future[ mClose ].rolling( window = 10 ).mean( )
# df_future[ mMA29 ] = df_future[ mClose ].rolling( window = 21 ).mean( )
# df_future[ mMA100 ] = df_future[ mClose ].rolling( window = 55 ).mean( )

""" PROFIT/LOSS RATIO = 2.51 """
# df_future[ mMA10 ] = df_future[ mClose ].rolling( window = 10 ).mean( )
# df_future[ mMA29 ] = df_future[ mClose ].rolling( window = 29 ).mean( )
# df_future[ mMA100 ] = df_future[ mClose ].rolling( window = 55 ).mean( )

""" PROFIT/LOSS RATIO = 2.22 """
df_future[ mMA10 ] = df_future[ mClose ].rolling( window = 10 ).mean( )
df_future[ mMA29 ] = df_future[ mClose ].rolling( window = 29 ).mean( )
df_future[ mMA100 ] = df_future[ mClose ].rolling( window = 100 ).mean( )

""" PROFIT/LOSS RATIO = 2.8 """
# df_future[ mMA10 ] = df_future[ mClose ].rolling( window = 10 ).mean( )
# df_future[ mMA29 ] = df_future[ mClose ].rolling( window = 29 ).mean( )
# df_future[ mMA100 ] = df_future[ mClose ].rolling( window = 60 ).mean( )


""" PROFIT/LOSS RATIO = 2.8 """
# df_future[ mMA10 ] = df_future[ mClose ].rolling( window = 10 ).mean( )
# df_future[ mMA29 ] = df_future[ mClose ].rolling( window = 29 ).mean( )
# df_future[ mMA100 ] = df_future[ mClose ].rolling( window = 100 ).mean( )

# df_future[ mMA10 ] = df_future[ mClose ].rolling( window = 10 ).mean( )
# df_future[ mMA29 ] = df_future[ mClose ].rolling( window = 14 ).mean( )
# df_future[ mMA100 ] = df_future[ mClose ].rolling( window = 51 ).mean( )
# print(df_future)


""" Df_trades is My Datastructure Where Auto generated Trades WIll be Stored  (FUTURE TRADE WILL BE GENERATED)"""
df_Trades = pd.DataFrame(
    columns = [ "DateTime" , "BuySell" , "EntryPrice" , "ltp" , "Status" , "Exitprice" , "Sl" , "TP" , "PnL" ]
    )

""" if closing price greater than MA 29 days , MA14 , MA100 : Generate Buy CE """
""" Logic to Generate  Trades  -- CROSSOVER OF MOVING AVERAGES for Different TIME PERIOD
 1. Calculated moving Average 
    MA for 14 Days - Faster Reaction
    MA for 29 Days - 
    MA for 100 Days - Less React
 
 2.Logic 
 As LTP is not Present, so In this example I have assumed Closing Price(Final price) as LTP
 
 3. Conditions to generate Trades
  a) Close >= MA for 14 Days
  b) MA of 14 Days >= MA of 29 Days  
  c) MA of 29 Days >= MA of  100 Days
  
  if all three Condition a & b & C satisfies : Take Entry or Generate Buy Signal
  
  4. how to Exit Trades ?
  a) Stop loss Hit: Have assumed Fixed Value for Stop loss
        If ltp is below  SL : Exit trades (for Buy Signal )
  b) Target points Hit: Have assumed Fixed Value for Stop Loss
        If ltp is above the TP : Exit Trades  (For Buy Signal)
  c)Suppose after My trading Strategies Time (i Have Set 3:20 as MIS SQUARE OFF)    
    The Trades which is Opened (Status  =1) , Close with  3:20 Time 
    ltp is Close (Assumed)        

 """



"""  When this Will Not Works  
1. To Calculate Moving Average : We ned bar data till X period
  If One of the Moving average  is not calculated , Then this Will not generate trades for that time
  in My Case : I have MA14, MA29, MA100 Days, -: Below  First 100(Larger Time Period MA)  bar, NO TRADES SIGNAL WILL BE GENERATED 
    


"""
df_future['Entry']  =""
df_future['Exit']  =""

for index , bar in df_future.iterrows( ) :
    if pd.isna( bar[ mMA100 ] ) == True :
        continue

    # print(bar[mDate])
    # Update pnl of openTrades
    for id , trade in df_Trades.iterrows( ) :
        if (trade[ "Status" ] == 0) :
            continue

        ltp = bar[ mClose ]

        trade[ "ltp" ] = ltp
        df_Trades.loc[ id , "ltp" ] = ltp
        pnl = round( ltp-trade[ "EntryPrice" ] , 2 )
        if (trade[ "BuySell" ] == "B") :
            trade[ "PnL" ] = pnl
            df_Trades.loc[ id , "PnL" ] = pnl

            #         for exit trades
        if (trade[ "Sl" ] >= ltp) :  # close the trades

            trade[ "Status" ] = 0  # close
            df_Trades.loc[ id , "Status" ] = 0
            df_Trades.loc[ id , "Exitprice" ] = ltp
            df_future.loc[ index , "Exit" ] = ltp
            continue

        if (trade[ "TP" ] <= ltp) :  # close the trades

            trade[ "Status" ] = 0  # close
            df_Trades.loc[ id , "Status" ] = 0
            df_Trades.loc[ id , "Exitprice" ] = ltp
            df_future.loc[ index , "Exit" ] = ltp
            continue

    if (bar[ mClose ] > bar[ mMA10 ]) and (bar[ mMA10 ] > bar[ mMA29 ]) and (bar[ mMA29 ] > bar[ mMA100 ]) :

        # print("Long Signal generated at " + bar[mDate])

        # if  ( bar[ mOpen ]  <= bar[ mClose ]) :
        if (True) :
            sl = bar[ mClose ]-50  # 20 points in banknify is good for scalping
            tp = bar[ mClose ]+50 *1.7
            status = 1
            exittime = -1
            df_Trades.loc[ len( df_Trades ) ] = [ bar[ mDate ] , "B" , bar[ mClose ] , bar[ mClose ] , status ,
                                                  exittime , sl , tp , 0 ]
            df_future.loc[index,"Entry"] = bar[ mClose ]

    # else :
    #     print("Square off This Trades")

df_lastOHLC = df_future.iloc[  -1  ]

fig = go.Figure(data= go.Candlestick(x=df_future[mDate],
                             open=df_future[mOpen],
                             high=df_future[mhigh],
                             low=df_future[mLow],
                             close=df_future[mClose]))


# signal = go.Scatter(x=df_future[mDate], y=df_future["Entry"], mode='lines', name='Entry',fillcolor = "#00ff00" )
# signal = go.Scatter( x=df_future[mDate], y=df_future["Entry"])

fig.add_scatter(x=df_future[mDate],
                y=df_future["Entry"],
                marker=dict(
                    color='orange',
                    size=30
                ),name= "Entry"
               )

fig.add_scatter(x=df_future[mDate],
                y=df_future["Exit"],
                marker=dict(
                    color='blue',
                    size=30
                ) ,name= "Exit"
               )

# fig.add_trace(signal)
# fig.show()
""" LAST BAR OHLC"""
"""
#  important Step : If After End of our Trading Strategies TIme , The Open Trade must be closed to LTP
#  But We assume any OHLC prices as ltp
"""
for ix , trade in df_Trades.iterrows( ) :
    if (trade[ "Status" ] == 1):

        ltp = df_lastOHLC[ mClose ] # assume close as ltp


        pnl = round( ltp-trade[ "EntryPrice" ] , 2 )
        if (trade[ "BuySell" ] == "B") :
            trade[ "PnL" ] = pnl


            # Forcefully closing Trades
            df_Trades.loc[ ix , 4 ] = 0  # close
            df_Trades.loc[ ix , 5 ] = ltp   #"Exitprice"
            df_Trades.loc[ ix , 3 ] = ltp  #"ltp"
            df_Trades.loc[ ix , 8 ] = pnl  #"PnL"

# print(df_lastOHLC)

""" APPLY STAT: Step 5 Calculate Stat """
filterGainCount = df_Trades[ "PnL" ] >= 0
filterLossCount = df_Trades[ "PnL" ] < 0
profittrade = df_Trades[ "PnL" ].where( filterGainCount ).count( )
losstrade = df_Trades[ "PnL" ].where( filterLossCount ).count( )

Gainpoints = df_Trades[ "PnL" ].where( filterGainCount ).sum( )
LossPoints = df_Trades[ "PnL" ].where( filterLossCount ).sum( )

print( "Profit Trade :"+profittrade.astype( str ) )
print( "Loss Trade :"+losstrade.astype( str ) )

print( "Profit points: "+str( Gainpoints ) )
print( """Loss  Points: """+str( LossPoints ) )

RatioOfGainByLoss = round( Gainpoints / abs( LossPoints ) , 2 )
print( "Day :Profit/Loss Points "+str( RatioOfGainByLoss ) )

Ratio_Of_Profit_Trade_By_LossTrade = round( profittrade / abs( losstrade ) , 2 )

print( "Day : No of Profit trades by Loss Trades "+str( Ratio_Of_Profit_Trade_By_LossTrade ) )
