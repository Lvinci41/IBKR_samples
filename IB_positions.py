from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from threading import Thread
import pandas as pd
import time
from ibapi import wrapper
from ibapi.utils import iswrapper 
from ibapi.common import *
from ibapi.contract import Contract
from datetime import datetime, timedelta, timezone

class ib_class(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        self.data = [] #Initialize variable to store candle        
        self.all_positions = pd.DataFrame([], columns = ['Account','Symbol', 'Quantity', 'Average Cost', 'Sec Type'])
        self.all_accounts = pd.DataFrame([], columns = ['reqId','Account', 'Tag', 'Value' , 'Currency'])

    def error(self, reqId:TickerId, errorCode:int, errorString:str, advancedOrderRejectJson = ""):
        if reqId > -1:
            print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    def position(self, account, contract, pos, avgCost):
        index = str(account)+str(contract.symbol)
        self.all_positions.loc[index]= account, contract.symbol, pos, avgCost, contract.secType
        
    def accountSummary(self, reqId, account, tag, value, currency):
        index = str(account)
        self.all_accounts.loc[index]=reqId, account, tag, value, currency

def connect_to_server(app):

    def run_loop():
        app.run()
    app.connect('127.0.0.1', 7497, 0)
    #Start the socket in a thread
    api_thread = Thread(target=run_loop, daemon=True)
    api_thread.start()
    time.sleep(0.5) #Sleep interval to allow time for connection to server


def read_positions(): #read all accounts positions and return DataFrame with information

    app = ib_class()    
    connect_to_server(app)

    app.reqPositions() # associated callback: position
    print("Waiting for IB's API response for accounts positions requests...\n")
    time.sleep(1)
    current_positions = app.all_positions # associated callback: position
    current_positions.set_index('Account',inplace=True,drop=True) #set all_positions DataFrame index to "Account"
    
    app.disconnect()

    return(current_positions)


def read_navs(): #read all accounts NAVs
    
    app = ib_class()  
    connect_to_server(app)

    app.reqAccountSummary(0,"All", "$LEDGER:ALL") #NetLiquidation
    #app.reqAccountSummary(0,"All", "TotalCashBalance") #NetLiquidation
    print("Waiting for IB's API response for NAVs requests...\n")
    time.sleep(1)
    current_nav = app.all_accounts
    current_nav.set_index('Tag',inplace=True,drop=True) #set all_positions DataFrame index 
    
    app.disconnect()

    return(current_nav)




print("Testing IB's API as an imported library:")

all_positions = read_positions()
print(all_positions, '\n')
all_positions.to_csv('positions.csv')  
#all_navs = read_navs()
#print(all_navs)



#https://stackoverflow.com/questions/57618971/how-do-i-get-my-accounts-positions-at-interactive-brokers-using-python-api


