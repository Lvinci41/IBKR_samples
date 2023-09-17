from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper 
from ibapi.common import *
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper
import pandas as pd

class TestApp(wrapper.EWrapper, EClient):
    posns = []
    fname = 'fname.txt'
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId:int):
        #self.nextValidOrderId = orderId
        self.reqAccountSummary(9002, "All", "$LEDGER:ALL")
        #self.reqAccountSummary(9002, "All", "CashBalance")  
        #self.reqAccountSummary(9002, "All", AccountSummaryTags.AllTags)  

    def accountSummary(self, reqId:int, account:str, tag:str, value:str, currency:str):
        self.reqAccountSummary(9002, "All", "$LEDGER:ALL")        
        with open('Balance.txt', 'a+') as file: #append, create if doesn't exist
            file.write("%s, %s, %s, %s\n" % (account, tag, value, currency))

    def accountSummaryEnd(self, reqId:int):
        self.disconnect()

    def start(self):
        self.reqAccountSummary(9001, "All", AccountSummaryTags.AllTags)

    def stop(self):
        self.done = True
        self.disconnect()


app = TestApp()
app.connect("127.0.0.1", 7497, 123)
app.run()

#original: https://stackoverflow.com/questions/62985585/interactive-brokers-tws-api-python-get-account-balance
#try: https://stackoverflow.com/questions/57618971/how-do-i-get-my-accounts-positions-at-interactive-brokers-using-python-api
#   https://stackoverflow.com/questions/70869327/how-to-return-positions-from-ibkr-api-interactive-brokers-consistently