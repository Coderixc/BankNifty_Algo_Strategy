# print( "Analysis" )

import pandas as pd


# MINCLOSE = 100
# MINVOLUME =  50000
class OHLCHeader :
    mOpen = "OPEN"
    mHigh = "HIGH"
    mLOW = "LOW"
    mCLOSE = "CLOSE"
    mVolume = "TOTTRDQTY"
    mTradingSymbol = "SYMBOL"
    mSeries = "SERIES"


#  Read INTRADY OHLC + Volume + PerChange Data from NSE Bhav Copy

class SingleChartPattern :

    # path = ".//Data//cm17AUG2023bhav.csv"
    # df_BhavCopy = pd.read_csv( path )

    def initilize_global_varibles( self ) :
        print( "Initializing" )
        self.MINCLOSE = 30
        self.MINVOLUME = 50000
        self.SERIESALLOWED = [ "EQ" ]  # ["EQ","BE"]

        filename = "cm30AUG2023bhav"
        path = ".//Data//"+filename+".csv"
        self.df_BhavCopy = pd.read_csv( path )

        count = self.df_BhavCopy.shape[ 0 ]
        print( " Trading Symbol Quote Contain Rows :"+str( count ) )

        self.List_Bullish_Marubuzo = [ ]
        self.List_Bearish_Marubuzo = [ ]
        print( "BHAV COPY Loaded: " , filename )

    # Loop & Iterate

    def Analyse_Quote_OHLC_Data_of_Stocks( self ) :

        for idx , record in self.df_BhavCopy.iterrows( ) :

            if (record[ OHLCHeader.mSeries ] not in self.SERIESALLOWED) :
                continue

            tradingSymbol = record[ OHLCHeader.mTradingSymbol ]
            o = record[ OHLCHeader.mOpen ]
            h = record[ OHLCHeader.mHigh ]
            l = record[ OHLCHeader.mLOW ]
            c = record[ OHLCHeader.mCLOSE ]
            v = record[ OHLCHeader.mVolume ]

            if (c <= self.MINCLOSE) :
                continue  # pass to next iteration

            if (v <= self.MINVOLUME) :
                continue  # pass to next iteration

            """ GREEN COLOR CANDLE """
            # cond1 = "Analysing Bullish MaruBuzo CP"
            # print("********",cond1)
            if (c > o) :
                if (l == o and h == c) :
                    # print( "BULLISH MURUBUZO CANDLESTICKS :" , tradingSymbol   )
                    self.List_Bullish_Marubuzo.append( tradingSymbol )

            """ RED COLOR CANDLE """
            # cond2 = "Analysing BEARISH MaruBuzo CP"
            # print( "********" ,cond2)
            if (c < o) :
                if (h == o and l == c) :
                    # print( "BEARISH MURUBUZO CANDLESTICKS :" , tradingSymbol )
                    self.List_Bearish_Marubuzo.append( tradingSymbol )

        print( "Analysis Completed,Please Check Analysis." )

    def Result_Of_Analysis( self ) :

        # self.initilize_global_varibles()
        print( "Preparing Report......" )
        print( " ********* BULLISH MARUBUZO CANDLESTICKS PATTERN *******" )
        for item in self.List_Bullish_Marubuzo :
            print( item )

        print( " ********* BEARISH MARUBUZO CANDLESTICKS PATTERN *******" )
        for item in self.List_Bearish_Marubuzo :
            print( item )


# Using the special variable
# __name__
if __name__ == "__main__" :
    """ Load indicator object """
    ind = SingleChartPattern( )

    """ Read or Load Bhav Copy Equity Data , contain O H L C """
    ind.initilize_global_varibles( )

    """ Apply Logic in Data  """
    ind.Analyse_Quote_OHLC_Data_of_Stocks( )

    """Result Of Analysis """
    ind.Result_Of_Analysis( )
