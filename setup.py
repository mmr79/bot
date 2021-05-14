# -*- coding: utf-8 -*-
"""
Created on Sat May  8 22:43:15 2021

@author: mraslan
"""

import ccxt
import pandas as pd
import numpy as np
ex=ccxt.binance()
ex.load_markets()
f=pd.DataFrame(ex.fetch_markets())
symbols=f[f['active']==True].symbol.unique()
#symbols=ex.symbols
def comp_prev(a,shift=1):
    return (a.High-a.Close.shift(shift))*100/a.Close.shift(shift)#a.High

s=[]
u=[]

for symbol in symbols:
    if symbol.split('/')[1]=='BTC':
        s.append(symbol)
    if symbol.split('/')[1]=='USDT':
        u.append(symbol)
symbols=[]        
for i in u:
    t=i.find('DOWN/' or 'UP/' or 'BULL/' or 'BEAR/')
    if(t==-1):
        symbols.append(i)

def trades(ex,symbol,since):
        #since = ex.parse8601(since)
        all_orders =pd.DataFrame()
        s=[]
        g=0
        while since < ex.milliseconds ():#-(1000*60*5):
            symbol = symbol  # change for your symbol
            #limit = 20  # change for your limit
        
            orders =  pd.DataFrame(ex.fetch_trades(symbol, since,limit=1000))
   
            s.append(len(all_orders))
            print(pd.to_datetime(since, unit='ms'))
            if len(orders):
                since =  orders['timestamp'].max()#orders[len(orders) - 1]['timestamp']
             
                if(g>0):
                    if since==(all_orders['timestamp'].max()):
                        since=ex.milliseconds()
                        break
                g+=1
                all_orders=pd.concat([orders,all_orders])
             
                if len(all_orders)==s[-1]:
                    break
                #print(all_orders[-1])
            else:
                    break
        #orders=pd.DataFrame(all_orders)
        all_orders['symbol']=symbol
        return all_orders

def ohlcv(since,symbol,data):
        data=pd.DataFrame()
        
        all_orders = []
        s=[]
        while since < ex.milliseconds ()-(1000*60*15):
            symbol = symbol  # change for your symbol
            #limit = 20  # change for your limit
        
            #orders =  ex.fetch_ohlcv(symbol,'1m',since=since,limit=10000)
            price=pd.DataFrame(ex.fetch_ohlcv(symbol,'1m',since=since),columns=['Time','Open','High','Low','Close','Volume'])
            
            s.append(len(data))
            print(pd.to_datetime(since, unit='ms'))
            if len(price):
                since =  price['Time'].max()
                #all_orders += orders
                data=pd.concat([price,data])
                if len(data)==s[-1]:
                    break
                #print(all_orders[-1])
            elif(s==since):
                
                break
        data['symbol']=symbol
        data['change']=comp_prev(data,1)
        data['Date']=pd.to_datetime(data['Time']*1000000)
        
        return data,price

def comp_prev_spread(a,shift=1):
        return (a.spread-a.spread.shift(shift))*100/a.spread

for i in range(0,len(u)):
    u[i]=u[i]+'/USDT'

from datetime import datetime
start=now = datetime.now()

#for bot
def scan_breakout(symbol,tf='5m',filters=2):
            all_df=pd.DataFrame()
            suspect=[]
            symbols=s+u
            message=[]
            sus={}

            df=pd.DataFrame(ex.fetch_ohlcv(symbol,tf,limit=1),columns=['Time','Open','High','Low','Close','Volume'])
            #df['Date']=pd.to_datetime(df['Time']*1000000)
            df['change']=(df['Close']-df['Open'])*100/df['Open']
            df['symbol']=symbol
            df['Date']=pd.to_datetime(df['Time']*1000000)
            suspects=df[df['change']>filters]
            all_df=pd.concat([df,all_df])
            if(len(suspects)):
                suspect.append(symbol)
                sus[symbol]=df['change']
                print(symbol)
                date=df['Date'].max()
                print(str(date))
                message=(symbol + '    ' +str(round(df['change'].max()))+'   '+str(date))
                
            #end=datetime.now()
            #elapsed=end-start
            #print(elapsed)
            return message



from rocketgram import Bot, Dispatcher, UpdatesExecutor
from rocketgram import context, commonfilters
from rocketgram import SendMessage
import time
import nest_asyncio
def main():
    
        nest_asyncio.apply()
        token = '1756164387:AAHWjHOz5rVjzfu-uqgaaRkzsiB5mjMDFHY'
        symbols=u
        router = Dispatcher()
        bot = Bot(token, router=router)
        
        @router.handler
        @commonfilters.command('/start')
        async def start_command():
            await SendMessage(-1001455990819, 'Hello there!').send()
        
        @router.handler
        @commonfilters.command('/help')
        async def start_command():
            await SendMessage(-1001455990819, 'Some userful help!').send()
        @router.handler
        @commonfilters.command('/input')
        async def start_command():
            SendMessage(context.user.user_id, 'input the filter').send()
            variant = context.callback.message
            await SendMessage(context.user.user_id, variant).send()
        
        @router.handler
        @commonfilters.command('/scan_5m')
        async def start_command():
            
        
            for symbol in symbols:
                message=scan_breakout(symbol,tf='5m',filters=2)
                if(len(message)):
                    await SendMessage(-1001455990819, message).send()
        
        @router.handler
        @commonfilters.command('/scan_1m')
        async def start_command():
            start=now = datetime.now()
        
            for symbol in symbols:
                message=scan_breakout(symbol,tf='1m',filters=2)
                if(len(message)):
                    await SendMessage(-1001455990819, message).send()
        
        @router.handler
        @commonfilters.command('/scan_1m_')
        async def start_command():
            start=now = datetime.now()
            while True:
              for symbol in symbols:
                message=scan_breakout(symbol,tf='1m',filters=2)
                if(len(message)):
                    await SendMessage(-1001455990819, message).send()
              await SendMessage(-1001455990819, '-----------------').send()
            time.sleep(10)
        
                
        @router.handler
        @commonfilters.command('/scan_15m')
        async def start_command():
            start=now = datetime.now()
          
            for symbol in symbols:
                message=scan_breakout(symbol,tf='15m',filters=2)
                if(len(message)):
                    await SendMessage(context.user.user_id, message).send()
        
        
        UpdatesExecutor.run(bot)



if __name__ == "__main__":
    main()