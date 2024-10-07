#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 23:52:57 2023

@author: wenkangng
"""
#"Data//CL_2017_2021"
import brokerage
import datetime
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
plt.ion()

file = ['Data//XAU_USD',"Data//S&P_Futures","Data//GBP-USD","Data//S&P","BTC-USD-2"] # Gold future, stock_future,  FOREX
#file = ["Crude_Oil_2018-2015","GBP_USD_2018_2023","Gold_2018-2023","SPX_2017_2021","Bitcoin_2018-2023","Copper_2018-2023","EUR_USD_2018-2023","S&P_2018-2023"]
new = ["ETH-USD"]
instrument = file[0] # depend on which instrument to test
#instrument = new[0] # depend on which instrument to test



df = pd.read_csv(f'{instrument}.csv', parse_dates=['Date'], thousands=',')


day_test = [7,14,17,20,23,27,30,36,39,42,45,47,50,53,56]
day_ma = [7,14,30]

#fig, ax = plt.subplots(1, 1)
#fig2, ax2 = plt.subplots(1, 1, figsize=(10, 6))

fig, (ax, ax2) = plt.subplots(2, 1, figsize=(12,8))
fig3, ax3 = plt.subplots(1, 1)

data = {
    "dates": [],
    "prices": [],
    "candles": [],
    "candle_duration": 1,
    "candle_duration_unit": "day",
    "fig": fig,
    "ax": ax,
    "ax2":ax2,
    "ax3":ax3,
    "fig3" : fig3,
    "plot_range": 30,

    "typical_price": [],
    'entry_long': [],
    "exit_long": [],
    "entry_short": [],
    'exit_short':[],
    'hold': [False],
    'order':[],
    'long' : [False],
    'ma_short':[],
    "ma_mid":[],
    "ma_long":[],
    "atr":[],
    "tr":[],
    "cut_loss_long":[],
    'cut_loss_short':[],
    "fibonacci_levels_1618" :[],
    "fibonacci_levels_1236" :[],
    "fibonacci_levels_1":[],
    "fibonacci_levels_786" :[],
    "fibonacci_levels_618":[],
    "fibonacci_levels_5" :[],
    "fibonacci_levels_382" :[],
    "fibonacci_levels_236":[],
    "fibonacci_levels_0":[],
    "fibonacci_levels_n236":[],
    "x":[],
    "ticket no":[],
    "transac_price":[],
    "transaction": [],
    "transaction_entry_exit":[],
    "profit": [],
    "initial_price": [],
    "unrealised_profit": [],
    "profit_per_day": [],
    "new_profit": [],
    "cagr":[],
    "num_days":[],
    "each_cagr": [],
    "profit_after_each_transaction": [],
    "highest_values":[]




}



def connect_brokerage(instrument,s):
    username, password = "angry_bird", "0000000"
    exchange = "BDM"
    conn = brokerage.login("www.bursa.com", username, password, speed=s)
    conn.connect(exchange, instrument)
    return conn



def collect_price(d, p):
    data['dates'].append(d)
    data['prices'].append(p)


def make_candlesticks():
    if data["candle_duration_unit"] == "minute":
        make_candlesticks_minute()
    elif data["candle_duration_unit"] == "day":
        make_candlesticks_day()
    else:
        raise "Error: only minute or day is allowed"


def make_candlesticks_minute():
    d = data['dates'][-1]
    p = data['prices'][-1]
    candles = data['candles']

    ddate = d.date()
    minutes = d.minute // data['candle_duration'] * data['candle_duration']
    dtime = datetime.time(d.hour, minutes, 0)
    d0 = datetime.datetime.combine(ddate, dtime)
    

    if len(candles) == 0:
        candles.append([d0, p, p, p, p])

    d_start = candles[-1][0]
    if d - d_start < datetime.timedelta(minutes=data['candle_duration']):
        d0, o, h, l, c = candles[-1]

        c = p
        h = max(h, p)
        l = min(l, p)

        candles[-1] = [d0, o, h, l, c]

    else:
        candles.append([d0, p, p, p, p])


def make_candlesticks_day():
    is_new_candle = False
    d = data['dates'][-1]
    p = data['prices'][-1]
    candles = data['candles']

    ddate = d.date()
    dtime = datetime.time(0, 0, 0)
    d0 = datetime.datetime.combine(ddate, dtime)

    if len(candles) == 0:
        candles.append([d0, p, p, p, p])
        is_new_candle = True
        
    d_start = candles[-1][0]
    if d - d_start < datetime.timedelta(days=data['candle_duration']):
        d0, o, h, l, c = candles[-1]

        c = p
        h = max(h, p)
        l = min(l, p)

        candles[-1] = [d0, o, h, l, c]

    else:
        candles.append([d0, p, p, p, p])
        is_new_candle = True
        #print("new_candle")
    
    return is_new_candle



def visualise_candlesticks():
    #fig = data["fig"]
    ax = data["ax"]
    candles = data["candles"]
    plot_range = data["plot_range"]
    size_candles = len(data["candles"])
    xlim_start = max(size_candles - plot_range, 0)
    xlim_end = size_candles

    ax.text(3.5, 6, f"{size_candles}", fontsize=15)

    quotes = [(mdates.date2num(i[0]), *i[1:]) for i in candles]

    ax.cla()
    candlestick_ohlc(ax, quotes, width=0.5, colorup="darkgreen", colordown="red")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_facecolor("lightcyan")


    d = [row[0] for row in data["candles"]]
   


    # Plot the Fibonacci Levels
    if len(candles) > day_test[1] :
        
        ax.axhline(
                    y= data["fibonacci_levels_1"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="k",
                    linewidth=1.5,
                    label="1",)
        ax.axhline(
                    y= data["fibonacci_levels_786"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="orange",
                    linewidth=1.5,
                    label="0.786",)
        ax.axhline(
                    y= data["fibonacci_levels_618"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="hotpink",
                    linewidth=1.5,
                    label="0.618",)
        ax.axhline(
                    y= data["fibonacci_levels_5"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="dodgerblue",
                    linewidth=1.5,
                    label="0.5",)
        ax.axhline(
                    y= data["fibonacci_levels_382"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="m",
                    linewidth=1.5,
                    label="0.382",)
        ax.axhline(
                    y= data["fibonacci_levels_236"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="g",
                    linewidth=1.5,
                    label="0.236",)
        ax.axhline(
                    y= data["fibonacci_levels_0"][-1],
                    xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
                    c="k",
                    linewidth=1.5,
                    label="0",)
        

             
        # handles = [f_1,f_786,f_618,f_5,f_382,f_236,f_0]
        # legend1 = ax.legend(handles = handles, loc="upper left",bbox_to_anchor =(1,1))

        
    # Plot the entry and exit signal
    ax.scatter(d, data["entry_long"], color='green', marker='^', label='Buy',s = 200)
    ax.scatter(d, data["exit_long"], color='red', marker='x', label='Sell',s = 200)
    ax.scatter(d, data["entry_short"], color='blue', marker='v', label='Short',s = 200)
    ax.scatter(d, data["exit_short"], color='orange', marker='x', label='Buyback',s = 200)
    
    
    
   
    
    # Plot the SMA
    ma_1, = ax.plot(d, data['ma_short'], c="r",linewidth=1.5, label=f"SMA {day_ma[0]}")
    ma_2, = ax.plot(d, data['ma_mid'], c="b",linewidth=1.5, label=f"SMA {day_ma[1]}")
    ma_3, = ax.plot(d, data['ma_long'], c="orange", linewidth=1.5,label=f"SMA {day_ma[2]}")
    
    
    #Create the legend
    ax.legend(
          loc="upper center",
          bbox_to_anchor=(0.5, -0.3),
          fancybox=True,
          shadow=True,
          #facecolor='k',
          #labelcolor='w',
          ncol=5)



    ax.xaxis.set_tick_params(rotation=30)
   
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    #plt.title(f"{instrument, size_candles}")
    
    live_realised_p_l = round(data.get("live_realised_p_l", 0),6)
    live_unrealised_p_l = round(data.get("live_unrealised_p_l", 0),6)
    #plt.title(f"{instrument}, {size_candles}, Live Realised P&L: {live_realised_p_l}, Live Unrealised_P&L: {live_unrealised_p_l}")
    ax.set_title(f"{instrument}, {size_candles}, Live Realised P&L: {live_realised_p_l}, Live Unrealised_P&L: {live_unrealised_p_l}")
    
                 
    # fig.tight_layout()
    # fig.canvas.draw()
    # fig.canvas.flush_events()
   
    

def data_creation():
   
    data["entry_long"].append(None)
    data["entry_short"].append(None)
    data["exit_short"].append(None)
    data["exit_long"].append(None)
    data["cut_loss_long"].append(None)
    data["cut_loss_short"].append(None)
    data["fibonacci_levels_1618"].append(None)
    data["fibonacci_levels_1236"].append(None)
    data["fibonacci_levels_1"].append(None)
    data["fibonacci_levels_786"].append(None)
    data["fibonacci_levels_618"].append(None)
    data["fibonacci_levels_5"].append(None)
    data["fibonacci_levels_382"].append(None)
    data["fibonacci_levels_236"].append(None)
    data["fibonacci_levels_0"].append(None)
    data["fibonacci_levels_n236"].append(None)
    
def fibonacci(day):
    size_candles = len(data["candles"])
   
    for i in range(0, size_candles, day):
        quotes = data["candles"]
        subset_quotes = quotes[i - day:i]
        subset_highs =[row[2] for row in subset_quotes]
        subset_lows = [row[3] for row in subset_quotes]
        #print(subset_highs)
        
        if subset_quotes and subset_highs and subset_lows:
            p_h = max(subset_highs)
            p_l = min(subset_lows)
            #print(subset_highs)
            data["fibonacci_levels_1618"][-1] = (p_h - (abs(p_h - p_l) * (1 - 1.618)))  # Change the Fibonacci level here
            data["fibonacci_levels_1236"][-1] = (p_h - (abs(p_h - p_l) * (1 - 1.236)))
            data["fibonacci_levels_1"][-1] = (p_h - (abs(p_h - p_l) * (1 - 1)))
            data["fibonacci_levels_786"][-1] = (p_h - (abs(p_h - p_l) * (1 - 0.786)))
            data["fibonacci_levels_618"][-1] = (p_h - (abs(p_h - p_l) * (1 - 0.618)))
            data["fibonacci_levels_5"][-1] = (p_h - (abs(p_h - p_l) * (1 - 0.5)))
            data["fibonacci_levels_382"][-1] = (p_h - (abs(p_h - p_l) * (1 - 0.382)))
            data["fibonacci_levels_236"][-1] = (p_h - (abs(p_h - p_l) * (1 - 0.236)))
            data["fibonacci_levels_0"][-1] = (p_h - (abs(p_h - p_l) * (1 - 0)))
            data["fibonacci_levels_n236"][-1] = (p_h - (abs(p_h - p_l) * (1 - (-0.236))))
            
            

def strategy(day,price,conn): 
 
    hold = data["hold"]
    order = data["order"]
    long = data['long']
    size_candles = len(data["candles"])


    if size_candles > 14:
        atr = data["atr"][-1]

    if size_candles > 1:

        o = [row[1] for row in data["candles"]]
        h = [row[2] for row in data["candles"]]
        l = [row[3] for row in data["candles"]]
        c = [row[4] for row in data["candles"]]


    if size_candles > day_ma[2]+4:
        
        ma_short = data['ma_short']
        ma_mid = data['ma_mid']
        ma_long = data["ma_long"]
    
        def entry_long_order(p):
            data["entry_long"][-1]=p
            long.append(True)
            hold.append(True)
            conn.submit_order(
                price=p,
                lot_size=1,
                order_type="Limit",
                action="Buy")
            
        def entry_short_order(p):
            
            data["entry_short"][-1]=p
            long.append(False)
            hold.append(True)  
            conn.submit_order(
                price=p,
                lot_size=1,
                order_type="Limit",
                action="Sell")
            
        def exit_long_order(price):
            
            p = price
            data["exit_long"][-1] = p
            long.append(False)
            hold.append(False)
            conn.submit_order(
                price=p,
                lot_size=1,
                order_type="Limit",action="Sell")
            
        def exit_short_order(price):
            
            p = price
            data["exit_short"][-1] = p
            hold.append(False)
            long.append(False)
            conn.submit_order(
                price=p,
                lot_size=1,
                order_type="Limit",
                action="Buy")  # Buy or Sell
        
        price_above_fibo_168 = (o[-2] >  data["fibonacci_levels_1618"][-1] or c[-2] >  data["fibonacci_levels_1618"][-1])
        price_below_fibo_n236 = (o[-2] < data["fibonacci_levels_n236"][-1] or c[-2] < data["fibonacci_levels_n236"][-1])
        
                            #### __________________ Entry Condition _______________________ ####### 
        if ( hold[-1] == False and long[-1] == False and size_candles != len(df) and not  price_below_fibo_n236 and not price_above_fibo_168 ):
             ##### _____________________   Condition of Long _____________________ ####
            if (ma_short[-2] > ma_mid[-2]  and ma_short[-3] < ma_short[-2] < ma_short[-1]
                and not ma_short[-2] > o[-2] and not ma_short[-2] > c[-2]
                ):
                
                if (h[-2] >= data["fibonacci_levels_618"][-1]  >= l[-2] or l[-2] >= data["fibonacci_levels_618"][-1]  >= h[-2]
                    and not ma_short[-1] > price):
                    # Long Order
                    order.append([day, -o[-1],"price hit fibo 618"]) # manual record order
                    entry_long_order(o[-1])
           
                    
                elif (h[-2] >= data["fibonacci_levels_786"][-1] >= l[-2] or l[-2] >= data["fibonacci_levels_786"][-1] >= h[-2]
                      and not ma_short[-1] > price):
                    
                    order.append([day,  -o[-1],"price hit fibo 786"])  # manual record order
                    entry_long_order(o[-1])

                                  
                elif (h[-2] >=  data["fibonacci_levels_5"][-1] >= l[-2] or l[-2] >=  data["fibonacci_levels_5"][-1] >= h[-2]
                      and not ma_short[-1] > price):
                    
                    order.append([day, -o[-1],"price hit fibo 0.5"])  # manual record order
                    entry_long_order(o[-1])

                      
                else:
                    pass
             # ___ big uptrend because of all MA go up __#
         
            elif  ((ma_short[-1] > ma_mid[-1]  > ma_long[-1]) and ma_short[-2] > ma_mid[-2]  > ma_long[-2]
                and ma_short[-3] > ma_mid[-3]  > ma_long[-3] and  o[-2] > ma_short[-2] and c[-2] > ma_short[-2]):
                
                     entry_long_order(o[-1])
                     order.append([day,  -o[-1],"uptrend determined"])  # manual record order

                
                 
             ##### _____________________   Condition of Entry short _____________________ ####
          
            elif (ma_short[-2] < ma_mid[-2] and ma_short[-3] < ma_mid[-3]  and  ma_short[-3] > ma_short[-2] > ma_short[-1]
                 and not c[-2] > ma_short[-2] and not o[-2] > ma_short[-2] ):

                if (h[-2] >= data["fibonacci_levels_618"][-1]  >= l[-2] or l[-2] >= data["fibonacci_levels_618"][-1]  >= h[-2]
                    and not ma_short[-1] < price):
                    
                    order.append([day, o[-1],"price hit fibo 0.618"])  # manual record order
                    entry_short_order(o[-1])


 
                elif (h[-2] >= data["fibonacci_levels_5"][-1] >= l[-2] or l[-2] >= data["fibonacci_levels_5"][-1] >= h[-2]
                      and not ma_short[-1] < price):

                    
                    order.append([day, o[-1],"price hit fibo 0.5"])  # manual record order
                    entry_short_order(o[-1])
                    
                   
                elif (h[-2] >= data["fibonacci_levels_382"][-1]>= l[-2] or l[-2] >= data["fibonacci_levels_382"][-1] >= h[-2]
                    and not ma_short[-1] < price):
                
                    
                    order.append([day, o[-1],"price hit fibo 0.382"])  # manual record order
                    entry_short_order(o[-1])

                    
                    
                else:
                    pass
                     
               # ___ big downtrend because of all MA go down __#
            # elif (ma_short[-1] < ma_mid[-1]  < ma_long[-1] and ma_short[-2] < ma_mid[-2]  < ma_long[-2]
            #      and ma_short[-3] < ma_mid[-3]  < ma_long[-3] and  o[-2] < ma_short[-1] and c[-2] < ma_short[-1]
            #     and not ma_short[-1] < price):
                
            elif ((ma_short[-1] < ma_mid[-1] < ma_long[-1]) and (ma_short[-2] < ma_mid[-2]  < ma_long[-2])
                 and ma_short[-3] < ma_mid[-3]  < ma_long[-3] and o[-2] < ma_short[-2] and c[-2]< ma_short[-2]):
                

                    order.append([day, o[-1],"downtrend determined "])  # manual record order
                    entry_short_order(o[-1])
                       

            else:
                 pass

    a = conn.get_transactions(True)[0] # pending order

        #### ____________________ Exit Long  ____________________####
    if hold[-1] == True and long[-1] == True and len(a)==0:
        data["cut_loss_long"][-1] = abs(order[-1][-2]) - 2 * atr
        cut_loss_long = data["cut_loss_long"][-1]

        #_____ MA short < MA mid continuous 2 days _______#
        if ma_short[-2] < ma_mid[-2] and ma_short[-3] < ma_mid[-3]:
    
            exit_long_order(o[-1])
            order.append([day, o[-1],'sell with MA cross'])  # manual record order
                 
           
    
        #_____ candlestick above MA shorts _______#
        elif ma_short[-2] > o[-2] and ma_short[-2] > c[-2]:
    
            exit_long_order(o[-1])
            order.append([day, o[-1],'sell with candle below MA']) # manual record order
                 
                 

        #_____ candlestick above fibonacci(day, 1.618) _______#
        elif o[-2] >  data["fibonacci_levels_1618"][-1] or c[-2] >  data["fibonacci_levels_1618"][-1]: 
    
             exit_long_order(o[-1])
             order.append([day, o[-1],'sell with candle > Fibo'])# manual record order
                  
             
        elif price < cut_loss_long:
             exit_long_order(price)
             order.append([day, price,'cut loss long'])# manual record order
                  
             
    
        else:
            pass

             
    
     #### ____________________ Exit Short  ____________________####
    elif hold[-1] == True and long[-1] == False and len(a)==0 :
        data["cut_loss_short"][-1] = order[-1][-2] + 2 * atr
        cut_loss_short = data["cut_loss_short"][-1]
        ma_mid_bigger_ma_short = (ma_short[-1] < ma_mid[-1] and  ma_short[-2] < ma_mid[-2] and ma_short[-3] > ma_short[-2] > ma_short[-1])

        
        #_____ MA short > MA mid continuous 2 days _______#
        if ma_short[-2] > ma_mid[-2] and ma_short[-3] > ma_mid[-3]:
    
            exit_short_order(o[-1])
            order.append([day, -o[-1],'buyback with MA cross'])
    
                 
             
        #_____ candlestick below MA shorts _______#
        elif c[-2] > ma_short[-2] and  o[-2] > ma_short[-2] :
    
            exit_short_order(o[-1])
            order.append([day, -o[-1],'buyback with candle below MA'])
                
    
        #_____ candlestick below ibonacci(day, 0)_______#
        elif o[-2] < data["fibonacci_levels_n236"][-1] or c[-2] < data["fibonacci_levels_n236"][-1]:
    
            exit_short_order(o[-1])
            order.append([day, -o[-1],'buyback with candle below fibo -0.236'])
             
        elif price > cut_loss_short:
    
             exit_short_order(price)
             order.append([day, -price,'cut loss short'])
             
       
        else:
             pass
    else:
             pass


     #________  Last day to cut off  ______________#
    if hold[-1] == True  and long[-1] == False and size_candles+1 == len(df) and len(conn.get_transactions(True)[0])==0:
        
        p= o[-1]
        data["exit_short"][-1]=p
        order.append([day,-p,"cut off short position"])
        hold.append(False)
        long.append(False)
        conn.submit_order(
            price= o[-1],
            lot_size=1,
            order_type="Market",
            action="Buy"  # Buy or Sell
            )
 
    if hold[-1] == True  and long[-1] == True and size_candles+1 == len(df) and len(conn.get_transactions(True)[0])==0:
        
        p= o[-1]
        data["exit_long"][-1]=p
        order.append([day,p,"cut off long position"])
        hold.append(False)
        long.append(False)
        conn.submit_order(
                        price= o[-1],
                        lot_size=1,
                         order_type="Market",
                        action="Sell"  # Buy or Sell
                        )

def calculate_ma(day_1,day_2,day_3):
    c = [row[4] for row in data["candles"]][:-1]
    #print(c)
    data["ma_mid"].append(None)
    data["ma_long"].append(None)
    data["ma_short"].append(None)

    if len(c)> day_1:
        ma_1= sum(c[-day_1-1:-1])/day_1
        data["ma_short"][-1]=ma_1
        
    if len(c) > day_2 :
        ma_1= sum(c[-day_1-1:-1])/day_1
        ma_2= sum(c[-day_2-1:-1])/day_2
        data["ma_short"][-1]=ma_1
        data["ma_mid"][-1]=ma_2

        
    if len(c)> day_3:
        ma_1= sum(c[-day_1-1:-1])/day_1
        ma_2= sum(c[-day_2-1:-1])/day_2
        ma_3= sum(c[-day_3-1:-1])/day_3
        data["ma_short"][-1]=ma_1
        data["ma_mid"][-1]=ma_2
        data["ma_long"][-1]=ma_3


def atr(n):
    h = [row[2] for row in data["candles"]][:-1]
    l = [row[3] for row in data["candles"]][:-1]
    c = [row[4] for row in data["candles"]][:-1]
    data["tr"].append(None)
    data["atr"].append(None)
    size_candles = len(data["candles"])

    if size_candles >2:
 
        tr = max(h[-1]-l[-1],abs(h[-1]-c[-2]),abs(l[-1]-c[-2]))
        data["tr"][-1]=tr
        
        
        if len(data["tr"]) == n+2:
            
            atr = sum(data["tr"][-n:])/n
            data["atr"][-1]=atr
            
            
        if len(data["tr"]) > n+2:
            atr = (data["atr"][-2]*(n-1)+data["tr"][-1])/n
            data["atr"][-1] = atr
        
def calculate_win_rate():
    print()
    record =[]
    x = data['x']
    if len(data['x'])>=2:
        for i in range(0,len(data["x"]),2):
            if x[i]+x[i+1]>0:
                record.append(1)
        
    win_rate = round(len(record)/(len(data["x"])/2),4)*100
    print(f"Win Rate :{win_rate}%")
    

def calculate_profit(conn):

    o = [row[1] for row in data["candles"]]
    # order = [row[1] for row in data["order"]]
    
    record = data["x"] 
    p_l = sum(record)      
    p_l_percentage = round(sum(record)/abs(record[0])*100,6)
    monkey_profit_percentage = round((o[-1]-o[0])/o[0] *100,5)
    monkey_profit = o[-1]-o[0]    
    n_pending = len(conn.get_transactions(True)[0])
    n_transcated = len(conn.get_transactions(True)[1])
    n_canceled = len(conn.get_transactions(True)[2])
    
    print(f"Total profit after stimulation :{p_l}")
    print(f"Total profit margin after stimulation :{p_l_percentage}%")
    print()
    print(f"Monkey profit :{monkey_profit}") 
    print(f"Monkey profit percentage :{monkey_profit_percentage}%") # Assume trader not trading ,just buy and let it go   
    print()
    print(f"Number of order pending:{n_pending}")
    print(f"Number of order transcated:{n_transcated}")
    print(f"Number of order cancelled:{n_canceled}")
    
def record_order(conn):
    
    ### _____ transacted order ________##
    a = conn.get_transactions(True)[1]
    record = data["x"]
    data['transaction'] = a
    
   
    if  len(record) !=  len(a) :
        data['transac_price'].append(a[-1]['transac_price'])
        transac_price = a[-1]['transac_price']
        
        if a[-1]['action'] == 'Sell':
           record.append(transac_price)
        elif a[-1]['action'] == 'Buy':
           record.append(-transac_price)
           
           

            
# Done by Risk Controller - Lim Sheng Hong
def calculate_live_realised_profit_and_cagr():
    
    
    if len(data['transaction_entry_exit']) == 0:
        
        data["cagr"].append(0)
        data['profit'].append(0)
        data['unrealised_profit'].append(0)
        data['transaction_entry_exit'].append([0, None, data['profit'][-1]])
        data["live_realised_p_l"] = data['profit'][-1]
        data["profit_per_day"].append(0)
    
    else:
        
        if len(data['transaction']) == 0:
            
            data["cagr"].append(0)
            data['profit'].append(0)
            data['unrealised_profit'].append(0)
            data['transaction_entry_exit'].append([0, None, data['profit'][-1]])
            data["live_realised_p_l"] = data['profit'][-1]
            data["profit_per_day"].append(0)
            
            
            
        
        if len(data['transaction']) > 0:
        
            if len(data['transaction']) % 2 == 1:
                
                
                if sum(sublist[0] for sublist in data['transaction_entry_exit']) == 0:
                    
                    if data['transaction'][-1]['action'] == 'Buy':
                        
                        data["cagr"].append(0)
                        data['initial_price'] = data['transaction'][-1]['transac_price']
                        unrealised_profit = sum(data['profit']) -data['initial_price'] + data['prices'][-1]
                        profit_per_day = unrealised_profit - sum(data['profit'])
                        data['profit'].append(0)
                        data['unrealised_profit'].append(unrealised_profit)
                        data['transaction_entry_exit'].append([-1, data['transaction'][-1]['action'], data['unrealised_profit'][-1]])
                        data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                        data["profit_per_day"].append(profit_per_day)
                        
                        
                        
                    if data['transaction'][-1]['action'] == 'Sell':
                        
                        data["cagr"].append(0)
                        data['initial_price'] = data['transaction'][-1]['transac_price']
                        unrealised_profit = sum(data['profit']) + data['initial_price'] - data['prices'][-1]
                        profit_per_day = unrealised_profit - sum(data['profit'])
                        data['profit'].append(0)
                        data['unrealised_profit'].append(unrealised_profit)
                        data['transaction_entry_exit'].append([1, data['transaction'][-1]['action'], data['unrealised_profit'][-1]])
                        data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                        data["profit_per_day"].append(profit_per_day)
                        
                        
                else:        
                
                    # for buy
                    if sum(sublist[0] for sublist in data['transaction_entry_exit']) == -1:
                    
                        data["cagr"].append(0)
                        data['profit'].append(0)
                        unrealised_profit = sum(data['profit']) -data['initial_price'] + data['prices'][-1]
                        profit_per_day = unrealised_profit - sum(data['profit'])
                        data['unrealised_profit'].append(unrealised_profit)
                        data['transaction_entry_exit'].append([0, None, data['unrealised_profit'][-1]])
                        data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                        data["profit_per_day"].append(profit_per_day)
                    
                
                    # for sell
                    else:
                    
                        data["cagr"].append(0)
                        data['profit'].append(0)
                        unrealised_profit = sum(data['profit']) + data['initial_price'] - data['prices'][-1]
                        profit_per_day = unrealised_profit - sum(data['profit'])
                        data['unrealised_profit'].append(unrealised_profit)
                        data['transaction_entry_exit'].append([0, None, data['unrealised_profit'][-1]])
                        data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                        data["profit_per_day"].append(profit_per_day)
                
                
                
            
            if len(data['transaction']) % 2 == 0:
                
                # for buy
                if sum(sublist[0] for sublist in data['transaction_entry_exit']) == -1:
                    
                    data["cagr"].append(0)
                    unrealised_profit = sum(data['profit']) -data['initial_price'] + data['transaction'][-1]['transac_price']
                    profit_per_day = unrealised_profit - sum(data['profit'])
                    data['unrealised_profit'].append(unrealised_profit)
                    data['transaction_entry_exit'].append([1, data['transaction'][-1]['action'], data['unrealised_profit'][-1]])
                    data['profit'].append(unrealised_profit - sum(data['profit']))
                    data["live_realised_p_l"] = sum(data['profit'])
                    data['profit_after_each_transaction'].append(data["live_realised_p_l"])
                    data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                    data["profit_per_day"].append(profit_per_day)
                    
                    
                    num_days = (data['transaction'][-1]['transac_timestamp'] - data['transaction'][-2]['transac_timestamp']).days
                    
                    if num_days ==0:
                        
                        num_days = 1
                    
                    
                    data['num_days'].append(num_days)
                    N = data['num_days'][-1]/252
                    cagr = ((data['x'][-1]+data['x'][-2])/abs(data['x'][-2]) + 1)**(1/N) -1
                    
                    data['cagr'][-1] =cagr
                    data['each_cagr'].append(cagr)
                
                
                else:
                    if sum(sublist[0] for sublist in data['transaction_entry_exit']) == 1:
                    
                        data["cagr"].append(0)
                        unrealised_profit = sum(data['profit']) + data['initial_price'] - data['transaction'][-1]['transac_price']
                        profit_per_day = unrealised_profit - sum(data['profit'])
                        data['unrealised_profit'].append(unrealised_profit)
                        data['transaction_entry_exit'].append([-1, data['transaction'][-1]['action'], data['unrealised_profit'][-1]])
                        data['profit'].append(unrealised_profit - sum(data['profit']))
                        data["live_realised_p_l"] = sum(data['profit'])
                        data['profit_after_each_transaction'].append(data["live_realised_p_l"])
                        data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                        data["profit_per_day"].append(profit_per_day)
                        
                        num_days = (data['transaction'][-1]['transac_timestamp'] - data['transaction'][-2]['transac_timestamp']).days
                        
                        if num_days ==0:
                            
                            num_days = 1
                        
                        data['num_days'].append(num_days)
                        
                        N = data['num_days'][-1]/252
                        cagr = ((data['x'][-1]+data['x'][-2])/abs(data['x'][-2]) + 1)**(1/N) -1
                        
                        data['cagr'][-1] = cagr
                        data['each_cagr'].append(cagr)
                
                
                    else:
                        data["cagr"].append(0)
                        unrealised_profit = sum(data['profit'])
                        profit_per_day = unrealised_profit - sum(data['profit'])
                        data['unrealised_profit'].append(unrealised_profit)
                        data['transaction_entry_exit'].append([0, None, data['unrealised_profit'][-1]])
                        data['profit'].append(unrealised_profit - sum(data['profit']))
                        data["live_realised_p_l"] = sum(data['profit'])
                        data["live_unrealised_p_l"] = data['unrealised_profit'][-1]
                        data["profit_per_day"].append(profit_per_day)
                

                    
# Done by Risk Controller - Lim Sheng Hong    
def calculate_each_transcation():
    # Create a dataframe with your data
    data2 = [i[1] for i in data['new_profit'][:-1]]
    df2 = pd.DataFrame({'values': data2})
    
    
    # Initialize variables
    
    first_values = [i[0] for i in data['transaction_entry_exit'][:-1]]
    intervals = []
    start_idx = None
    current_sum = 0
    
    # Iterate through 'first_values' to find the intervals
    for idx, value in enumerate(first_values):
        current_sum += value
        
        if start_idx is None:
            if value != 0:
                start_idx = idx
        else:
            if current_sum == 0:
                intervals.append((start_idx, idx))
                start_idx = None
        
    
    # Find the highest value in each non-zero interval
    for start, end in intervals:
        interval_values = df2.iloc[start:end+1]['values']
        highest_value = interval_values.max()
        data["highest_values"].append(round(highest_value,2))
            

# Done by Risk Controller - Lim Sheng Hong        
def print_each_transcation(): 
    
    highest_values = data["highest_values"]
    # Create a dictionary to assign names to the values
    transaction_names = {f'Transaction {i+1}': value for i, value in enumerate(highest_values)}
    bold_and_underline = "\033[1;4m"
    reset_format = "\033[0m" 
    text = "Maximum Profit & Loss of each transaction"
    
    formatted_text = f"{bold_and_underline}{text}{reset_format}" 
    print() # print space
    print(formatted_text)
    print()
    # Print out the values with their corresponding names
    for name, value in transaction_names.items():
        print(f'{name}: {value}')
        
    
# Done by Risk Controller - Lim Sheng Hong
def calculate_profit_per_day():
    
    p = data['profit_per_day'][-1]
    new_profit = [data['dates'][-1], p]
    data['new_profit'].append(new_profit)
    
    
    
# Done by Risk Controller - Lim Sheng Hong
def visualise_profit_loss():
    
    dates = data["dates"]
    dates = [int(mdates.date2num(date)) for date in dates]
    profit_per_day = data['profit_per_day']
    #realised_pnl = data['realised_PnL']
    #accumulate_pnl = data['accumulate_PnL']
    #fig2 = data["fig2"]
    ax2 = data["ax2"]
    
    x = [(idx) for idx, i in enumerate(dates)]
    plot_range = data['plot_range']
    
    #plot_range = data['plot_range']
    #x = dates[-plot_range:]  # Use the last `plot_range` dates for x-axis
    
    ax2.cla() #clear current axis\
    ax2.grid(True)
    ax2.set_xlabel('Number of Price Collected')
    ax2.set_ylabel('Price')
    ax2.set_title('Profit & Loss')
    colors = ['green' if profit > 0 else 'red' for profit in profit_per_day[-plot_range:]]
    # Plot the bars with conditional colors
    ax2.bar(x[-plot_range:], profit_per_day[-plot_range:], color=colors, width = 0.5 )
    ax2.axhline(y=0, color='black', linewidth=1.0, linestyle='-')  # Add black line at y=0
    #ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    #ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax2.set_facecolor("lightcyan")
    ax2.xaxis.set_tick_params(rotation=30)
    #ax2.legend(loc="upper left")
    

    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events() #display to the screen immediately


# Done by Risk Controller - Lim Sheng Hong
def visualise_cagr():
    
    dates = data["dates"]
    dates = [int(mdates.date2num(date)) for date in dates]
    cagr = data['cagr']
    #realised_pnl = data['realised_PnL']
    #accumulate_pnl = data['accumulate_PnL']
    fig3 = data["fig3"]
    ax3 = data["ax3"]
    
    x = [(idx) for idx, i in enumerate(dates)]
    plot_range = data['plot_range']
    
    #plot_range = data['plot_range']
    #x = dates[-plot_range:]  # Use the last `plot_range` dates for x-axis
    
    ax3.cla() #clear current axis\
    ax3.grid(True)
    ax3.set_xlabel('CAGR')
    ax3.set_ylabel('Percentage,%')
    ax3.set_title('Compound Annual Growth Rate')
    colors = ['green' if cagr > 0 else 'red' for cagr in cagr[-plot_range:]]
    # Plot the bars with conditional colors
    ax3.bar(x[-plot_range:], cagr[-plot_range:], color=colors, width = 1.5 )
    ax3.axhline(y=0, color='black', linewidth=1.0, linestyle='-')  # Add black line at y=0
    #ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    #ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax3.set_facecolor("lightcyan")
    ax3.xaxis.set_tick_params(rotation=30)
    
    #ax2.legend(loc="upper left")
    

    fig3.tight_layout()
    fig3.canvas.draw()
    fig3.canvas.flush_events() #display to the screen immediately


# Done by Risk Controller - Lim Sheng Hong
def realised_profit_transaction():
    profits = data['profit']
    
    filtered_profits = [profit for profit in profits if profit != 0] # Filter greater than 0
    
    
    
    colors = ['g' if profit > 0 else 'r' for profit in filtered_profits]
    # Create x-values starting from 1
    x_values = range(1, len(filtered_profits) + 1)
    
    plt.figure(figsize=(10, 6)) 
    plt.bar(x_values, filtered_profits, color=colors)
    plt.title('Realised Profit of Each Transaction (Fibonacci Retracement and TMA)')
    plt.xlabel('Transaction')
    plt.ylabel('Profit')
    plt.xticks(x_values)
    
    plt.show()           
                

# Done by Risk Controller - Lim Sheng Hong
def maximun_p_l_transaction():
    highest_values = data["highest_values"]
    profits = data['profit']
    
    filtered_profits = [profit for profit in profits if profit != 0] # Filter greater than 0
    filtered_profits2 = [highest_value for highest_value in highest_values if highest_value != 0]
    
    # Create a bar graph for filtered profits
    plt.figure(figsize=(10, 6))  # Optional: Set the figure size
    
    # Define colors for positive (green) and negative (red) profits
    colors2 = ['g' if highest_value > 0 else 'r' for highest_value in filtered_profits2]
    
    # Create x-values starting from 1
    x_values = range(1, len(filtered_profits) + 1)
    
    plt.bar(x_values, filtered_profits2, color=colors2)
    plt.title('Maximum Profit & Loss of Each Transaction (Fibonacci Retracement and TMA)')
    plt.xlabel('Transaction')
    plt.ylabel('Profit')
    plt.xticks(x_values)
    
    plt.show()         


# Done by Risk Controller - Lim Sheng Hong
def profit_after_each_transaction():               
    # Assuming data['profit_after_each_transaction'] is a list or array containing your profit data
    profits = data['profit_after_each_transaction']
    
    # Create a line graph
    plt.figure(figsize=(10, 6))  # Optional: Set the figure size
    
    # Assuming you want to use the index as the x-axis values
    x_values = range(1, len(profits) + 1)
    
    plt.plot(x_values, profits, marker='o', linestyle='-', color='b')
    plt.title('Profit After Each Transaction ( Fibonacci Retracement and TMA)')
    plt.xlabel('Transaction')
    plt.ylabel('Profit')
    plt.xticks(x_values)
    
    plt.grid(True)  # Optional: Add a grid to the plot
    
    plt.show()                
                
                
                



def main():
    conn = connect_brokerage(instrument,0.01)
    for d, p in conn.data_stream():
        collect_price(d, p)
        visualise_candlesticks()
        is_new_candle = make_candlesticks_day()
        strategy(d,p,conn)
        #print(d, p)
        record_order(conn)
        calculate_live_realised_profit_and_cagr()
        calculate_profit_per_day()
        # visualise_profit_loss()
        # visualise_cagr()

        

        if is_new_candle:
            data_creation() # Append None in data
            atr(14)
            calculate_ma(day_ma[0], day_ma[1], day_ma[2])
            fibonacci(day_test[1])
             

    conn.logout()
    calculate_win_rate()
    calculate_profit(conn)
    calculate_win_rate()
    calculate_each_transcation()
    print_each_transcation()
    realised_profit_transaction()  
    maximun_p_l_transaction()     
    profit_after_each_transaction()



main()



                
                
                
                
                
                
                
                
                
                
                



            

