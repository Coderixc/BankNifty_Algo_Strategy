print("Analysis")

import pandas as pd

# MINCLOSE = 100
# MINVOLUME =  50000
class ColumnName :
    mOpen  = "OPEN"
    mHigh = "HIGH"
    mLOW = "LOW"
    mCLOSE = "CLOSE"
    mVolume ="TOTTRDQTY"
    mTradingSymbol = "SYMBOL"


#  Read INTRADY OHLC + Volume + PerChange Data from NSE Bhav Copy

class Indicator( ColumnName):

# path = ".//Data//cm17AUG2023bhav.csv"
# df_BhavCopy = pd.read_csv( path )


    def initilize_global_varibles(self):
        self.MINCLOSE = 100
        self.MINVOLUME =50000
        path = ".//Data//cm17AUG2023bhav.csv"
        self.df_BhavCopy = pd.read_csv( path )

        count = self.df_BhavCopy.shape[0]
        print( "Quote Contain Rows :" + str(count) )

        self.List_Bullish_Marubuzo =[]
        self.List_Bearish_Marubuzo = [ ]


# Loop & Iterate

    def Analyse_Quote_OHLC_Data_of_Stocks( self):


        for idx , record in self.df_BhavCopy.iterrows( ):



            tradingSymbol = record[ColumnName.mTradingSymbol]
            o = record[ColumnName.mOpen]
            h = record[ColumnName.mHigh]
            l = record[ ColumnName.mLOW ]
            c = record[ ColumnName.mCLOSE ]
            v = record[ ColumnName.mVolume ]

            if(c <= self.MINCLOSE):
                continue #pass to next iteration

            if (v <= self.MINCLOSE) :
                continue  # pass to next iteration



            """ GREEN COLOR CANDLE """
            # cond1 = "Analysing Bullish MaruBuzo CP"
            # print("********",cond1)
            if(c > o) :
                if(l== o and h== c):
                    # print( "BULLISH MURUBUZO CANDLESTICKS :" , tradingSymbol   )
                    self.List_Bullish_Marubuzo.append(tradingSymbol)

            """ RED COLOR CANDLE """
            # cond2 = "Analysing BEARISH MaruBuzo CP"
            # print( "********" ,cond2)
            if (c < o) :
                if (h == o and l == c) :
                    # print( "BEARISH MURUBUZO CANDLESTICKS :" , tradingSymbol )
                    self.List_Bearish_Marubuzo.append( tradingSymbol )

        print("Analysis Completed,Please Check Analysis.")










    def Result_Of_Analysis(self):

        # self.initilize_global_varibles()
        print("Preparing Report")
        print( " ********* BULLISH MARUBUZO CANDLESTICKS PATTERN *******")
        for item in self.List_Bullish_Marubuzo:
            print(item)

        print( " ********* BEARISH MARUBUZO CANDLESTICKS PATTERN *******")
        for item in self.List_Bearish_Marubuzo:
            print(item)






# Using the special variable
# __name__
if __name__=="__main__":
    """ Load indicator object """
    ind = Indicator()

    """ Read or Load Bhav Copy Equity Data , contain O H L C """
    ind.initilize_global_varibles()

    """ Apply Logic in Data  """
    ind.Analyse_Quote_OHLC_Data_of_Stocks()

    """Result Of Analysis """
    ind.Result_Of_Analysis()
