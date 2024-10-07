#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 15:25:48 2023

@author: wenkangng
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:39:01 2023

@author: wenkangng
"""


import brokerage
import datetime
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
plt.ion()

file = ["/Users/wenkangng/Documents/research/CIMB"]

instrument = file[0] # depend on which instrument to test

df = pd.read_csv(f'{instrument}.csv', parse_dates=['Date'], thousands=',')


day_test = [14,17,20,23,27,30,36,39,42,45,47,50,53,56]
day_ma = [15,30,60]
day = [7,14,30,35,60]
fig, ax = plt.subplots(1, 1)

data = {
    "dates": [],
    "prices": [],
    "candles": [],
    "candle_duration": 1,
    "candle_duration_unit": "day",
    "fig": fig,
    "ax": ax,
    "plot_range": 30,
    "day":day[2], # Duration of measure highest and lowest price

    "typical_price": [],
    'entry_long': [],
    "exit_long": [],
    "entry_short": [],
    'exit_short':[],
    'hold': [False],
    'order':[],
    'long' : [False],
    'ma_1':[],
    "ma_2":[],
    "ma_3":[]



}


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
    day =data["day"]
    fig = data["fig"]
    ax = data["ax"]
    candles = data["candles"]
    plot_range = data["plot_range"]
    size_candles = len(data["candles"])
    xlim_start = max(size_candles - plot_range, 0)
    xlim_end = size_candles

    ax.text(3.5, 6, f"{size_candles}", fontsize=15)

    quotes = [(mdates.date2num(i[0]), *i[1:]) for i in candles]

    ax.cla()
    candlestick_ohlc(ax, quotes[-plot_range:], width=0.5, colorup="darkgreen", colordown="red")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.set_facecolor("lightcyan")


    
    # if size_candles >= day:
    #     fibonacci_levels_1 = fibonacci(day,1)
    #     fibonacci_levels_2 = fibonacci(day,0.786)
    #     fibonacci_levels_3 = fibonacci(day,0.618)
    #     fibonacci_levels_4 = fibonacci(day,0.5)
    #     fibonacci_levels_5 = fibonacci(day,0.382)
    #     fibonacci_levels_6 = fibonacci(day,0.236)
    #     fibonacci_levels_7 = fibonacci(day,0)
    
        
    #     latest_fibonacci_level_1 = fibonacci_levels_1[-1] if fibonacci_levels_1 else None
    #     latest_fibonacci_level_2 = fibonacci_levels_2[-1] if fibonacci_levels_2 else None
    #     latest_fibonacci_level_3 = fibonacci_levels_3[-1] if fibonacci_levels_3 else None
    #     latest_fibonacci_level_4 = fibonacci_levels_4[-1] if fibonacci_levels_4 else None
    #     latest_fibonacci_level_5 = fibonacci_levels_5[-1] if fibonacci_levels_5 else None
    #     latest_fibonacci_level_6 = fibonacci_levels_6[-1] if fibonacci_levels_6 else None
    #     latest_fibonacci_level_7 = fibonacci_levels_7[-1] if fibonacci_levels_7 else None



    #     if latest_fibonacci_level_1 is not None:
    #         ax.axhline(
    #             y=latest_fibonacci_level_1,
    #             xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #             c="r",
    #             linewidth=1.5,
    #             label="1",
    #         )
            
    #     if latest_fibonacci_level_2 is not None:
    #          ax.axhline(
    #              y=latest_fibonacci_level_2,
    #              xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #              c="orange",
    #              linewidth=1.5,
    #              label="0.786",
    #          )
             
    #     if latest_fibonacci_level_3 is not None:
    #          ax.axhline(
    #              y=latest_fibonacci_level_3,
    #              xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #              c="hotpink",
    #              linewidth=1.5,
    #              label="0.618",
    #          )
    #     if latest_fibonacci_level_4 is not None:
    #          ax.axhline(
    #              y=latest_fibonacci_level_4,
    #              xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #              c="dodgerblue",
    #              linewidth=2,linestyle = '--',
    #              label="0.5")
                 
    #     if latest_fibonacci_level_5 is not None:
    #          ax.axhline(
    #              y=latest_fibonacci_level_5,
    #              xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #              c="g",
    #              linewidth=1.5,
    #              label="0.382")
             
    #     if latest_fibonacci_level_6 is not None:
    #          ax.axhline(
    #              y=latest_fibonacci_level_6,
    #              xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #              c="m",
    #              linewidth=1.5,
    #              label="0.236")
             
    #     if latest_fibonacci_level_7 is not None:
    #          ax.axhline(
    #              y=latest_fibonacci_level_7,
    #              xmax=min(quotes[-1][0], plot_range - 1) / (xlim_end - xlim_start),
    #              c="k",
    #              linewidth=1.5,
    #              label="0")
             
        
             
    d = [row[0] for row in data["candles"]]    
    ax.scatter(d, data["entry_long"], color='green', marker='^', label='Buy',s = 200)
    ax.scatter(d, data["exit_long"], color='red', marker='x', label='Sell',s = 200)
    ax.scatter(d, data["entry_short"], color='blue', marker='v', label='Short',s = 200)
    ax.scatter(d, data["exit_short"], color='orange', marker='x', label='Buyback',s = 200)
    
    
    # # plot simple moving average
    # ax.plot(d[-plot_range:],data['ma_1'][-plot_range:])
    # ax.plot(d[-plot_range:],data['ma_2'][-plot_range:])
    # ax.plot(d[-plot_range:],data['ma_3'][-plot_range:])


    ax.legend(
         loc="upper center",
         bbox_to_anchor=(0.5, -0.25),
         fancybox=True,
         shadow=True,
         ncol=4)

    ax.xaxis.set_tick_params(rotation=30)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{instrument, size_candles}")
    fig.tight_layout()
    fig.canvas.draw()
    fig.canvas.flush_events()
   
    

def fibonacci(day,level):
    candles = data["candles"]
    quotes = [(mdates.date2num(i[0]), *i[1:]) for i in candles]
    fibonacci_levels = []

    for i in range(0, len(quotes), day):
        subset_quotes = quotes[i - day:i]
        subset_highs =[row[2] for row in subset_quotes] 
        subset_lows = [row[3] for row in subset_quotes]

        if subset_quotes and subset_highs and subset_lows:
            p_h = max(subset_highs)
            p_l = min(subset_lows)
            retracement_level = (p_h - (abs(p_h - p_l) * (1 - level)))  # Change the Fibonacci level here
            fibonacci_levels.append(retracement_level)

    return fibonacci_levels




def strategy():

    # Trading plan for buying and selling   
    size_candles = len(data["candles"])
    day =data["day"]
    hold = data["hold"]
    order = data["order"]
    long = data['long']


   
    if size_candles > day:
        
        buy_price = fibonacci(day,0.618)[-1]  # fibonacci() is dynamic 
        sell_price = fibonacci(day,0.786)[-1] or fibonacci(day,1.236)[-1]
        loss_cut_price = fibonacci(day,0.5)[-1]
        
        short_price =fibonacci(day,0.382)[-1] or fibonacci(day,0.236)[-1]
        buyback_price = fibonacci(day,0.236)[-1]
        short_loss_cut_price =  fibonacci(day,0.5)[-1]
        
    else:
          buy_price = fibonacci(day,0.618)  # fibonacci() is dynamic 
          sell_price = fibonacci(day,0.786)
          loss_cut_price = fibonacci(day,0.5)
         
          short_price =fibonacci(day,0.382)
          buyback_price = fibonacci(day,0.236)
          short_loss_cut_price =  fibonacci(day,0.5)
                
             
    o = [row[1] for row in data["candles"]]
    h = [row[2] for row in data["candles"]]
    l = [row[3] for row in data["candles"]]
    c = [row[4] for row in data["candles"]]
  
    
    # if size_candles <= 1:        
    #     entry_long_signal_appear = (o[-1] >= buy_price >= c[-1] or c[-1] >= buy_price >= o[-1] ) 
    #     entry_short_signal_appear = (o[-1] >= short_price >= c[-1]or c[-1] >= short_price >= o[-1]) 
    #     exit_long_signal_take_profit = (o[-1] >= sell_price >= c[-1] or c[-1] >= sell_price >= o[-1])
    #     exit_short_signal_take_profit = ( c[-1] >= buyback_price >= o[-1] or o[-1] >= buyback_price >= c[-1]) 
    #     exit_long_signal_cut_loss = (c[-1] >= loss_cut_price >= o[-1] or o[-1] >= loss_cut_price >= c[-1]) 
    #     exit_short_signal_cut_loss = (o[-1] >= short_loss_cut_price >= c[-1] or c[-1] >= short_loss_cut_price >= o[-1])
    # else:
    #     entry_long_signal_appear = (o[-2] >= buy_price >= c[-2] or c[-2] >= buy_price >= o[-2] ) 
    #     entry_short_signal_appear = (o[-2] >= short_price >= c[-2]or c[-2] >= short_price >= o[-2]) 
    #     exit_long_signal_take_profit = (o[-2] >= sell_price >= c[-2] or c[-2] >= sell_price >= o[-2])
    #     exit_short_signal_take_profit = ( c[-2] >= buyback_price >= o[-2] or o[-2] >= buyback_price >= c[-2]) 
    #     exit_long_signal_cut_loss = (c[-2] >= loss_cut_price >= o[-2] or o[-2] >= loss_cut_price >= c[-2]) 
    #     exit_short_signal_cut_loss = (o[-2] >= short_loss_cut_price >= c[-2] or c[-2] >= short_loss_cut_price >= o[-2])

    if size_candles <= 1:        
        entry_long_signal_appear = (h[-1] >= buy_price >= l[-1] or l[-1] >= buy_price >= h[-1] ) 
        entry_short_signal_appear = (h[-1] >= short_price >= l[-1]or l[-1] >= short_price >= h[-1]) 
        exit_long_signal_take_profit = (h[-1] >= sell_price >= l[-1] or l[-1] >= sell_price >= h[-1])
        exit_short_signal_take_profit = ( l[-1] >= buyback_price >= h[-1] or h[-1] >= buyback_price >= l[-1]) 
        exit_long_signal_cut_loss = (l[-1] >= loss_cut_price >= h[-1] or h[-1] >= loss_cut_price >= l[-1]) 
        exit_short_signal_cut_loss = (h[-1] >= short_loss_cut_price >= l[-1] or l[-1] >= short_loss_cut_price >= h[-1])
    else:
      entry_long_signal_appear = (h[-2] >= buy_price >= l[-2] or l[-2] >= buy_price >= h[-2] ) 
      entry_short_signal_appear = (h[-2] >= short_price >= l[-2]or l[-2] >= short_price >= h[-2]) 
      exit_long_signal_take_profit = (h[-2] >= sell_price >= l[-2] or l[-2] >= sell_price >= h[-2])
      exit_short_signal_take_profit = ( l[-2] >= buyback_price >= h[-1] or h[-2] >= buyback_price >= l[-2]) 
      exit_long_signal_cut_loss = (l[-2] >= loss_cut_price >= h[-2] or h[-2] >= loss_cut_price >= l[-2]) 
      exit_short_signal_cut_loss = (h[-2] >= short_loss_cut_price >= l[-2] or l[-2] >= short_loss_cut_price >= h[-2])


    data["entry_long"].append(None)
    data["entry_short"].append(None)
    data["exit_short"].append(None)
    data["exit_long"].append(None)
   

        
    if hold[-1] == False and long[-1] == False and not exit_short_signal_cut_loss and not exit_long_signal_cut_loss and not size_candles+1 == len(df) :
        if entry_long_signal_appear:
            
            p = o[-1]
            data["entry_long"][-1]=p
            long.append(True)
            hold.append(True)
            order.append(-p)

            print(size_candles, p, 'buy')
                 
        elif entry_short_signal_appear:
            
            p = o[-1]
            data["entry_short"][-1]=p
            order.append(p)
            hold.append(True)
            long.append(False)

            print(size_candles, p, 'short')
        else:
         print(size_candles,None)
            

            
            
    elif hold[-1] == True and long[-1] == True:
        if exit_long_signal_take_profit:
                 
                  p = o[-1]
                  data["exit_long"][-1]=p
                  order.append(p)
                  long.append(False)
                  hold.append(False)

                  print(size_candles, p,  'sell')
                 
                 
     
        elif exit_long_signal_cut_loss:
                  hold.append(False)
                  p = o[-1]
                  data["exit_long"][-1]=p
                  order.append(p)
                  long.append(False)
                  print(size_candles, p, 'cut loss ', f"Cut Loss Fibo price :{loss_cut_price}")
                 
                 
                  # if o[-2]<= abs(data['order'][-1]*0.96)or c[-2]<= abs(data['order'][-1]*0.96) == True:
                  #     print(size_candles, p, 'cut loss ', f"Cut Loss VaR :{abs(data['order'][-1]*0.96)}")
        else:
            print(size_candles,None)
    
    elif hold[-1] == True and long[-1] == False:              
        if exit_short_signal_take_profit:
                  hold.append(False)
                  long.append(False)
                  p = o[-1]
                  order.append(-p)
                  data['exit_short'][-1]=p
                 
                  print(size_candles, p,  'buyback')
                 
        
        elif exit_short_signal_cut_loss:
                hold.append(False)
                long.append(False)
                p = o[-1]
                data["exit_short"][-1]=p
                order.append(-p)
                print(size_candles, p, 'cut loss ', f"Cut Loss Fibo price :{short_loss_cut_price}")

               
        else:
              print(size_candles,None)        
                
                # if o[-2]>=data['order'][-1]*1.04 or c[-2]>=data['order'][-1]*1.04 == True :
                #     print(size_candles, p, 'cut loss ', f"Cut Loss VaR :{abs(data['order'][-1]*1.04)}")

        
 
        
    else:
         print(size_candles,None)
    
                 
            
    # Last day to cut off
    if hold[-1] == True  and long[-1] == False and size_candles+1 == len(df):
            p= o[-1]
            data["exit_short"][-1]=p
            order.append(-p)
            print(size_candles, p, 'buyback')
            
    if hold[-1] == True  and long[-1] == True and size_candles+1 == len(df):
            p= o[-1]
            data["exit_long"][-1]=p
            order.append(p)
            print(size_candles, p, 'sell')
        

def calculate_win_rate():
    record =[]
    if len(data['order'])>=2:
        for i in range(0,len(data["order"]),2):
            if data["order"][i]+data["order"][i+1]>0:
                record.append(1)
        
    win_rate = round(len(record)/(len(data["order"])/2),4)*100
    print(f"Win Rate :{win_rate}%")
            
             
    
   
def calculate_profit():
    order = data["order"]
    o = [row[1] for row in data["candles"]]
    p_l = round(sum(order)/abs(order[0]),6)*100
    monkey_profit = round((o[-1]-o[0])/o[0]*100,3)   
    n = len(order)/2
    print(f"Total profit after stimulation :{p_l}%")
    print(f"Monkey profit :{monkey_profit}") 
    print(F"Number of transcation:{n}")
    
    
def calculate_ma(day_1,day_2,day_3):
    c = [row[4] for row in data["candles"]]
    data["ma_1"].append(None)
    data["ma_2"].append(None)
    data["ma_3"].append(None)

    if len(c)> day_1:
        ma_1= sum(c[-day_1:])/day_1
        data["ma_1"][-1]=ma_1
        
    if len(c) > day_2 :
        ma_1= sum(c[-day_1:])/day_1
        ma_2= sum(c[-day_2:])/day_2
        data["ma_1"][-1]=ma_1
        data["ma_2"][-1]=ma_2
        
    if len(c)> day_3:
        ma_1= sum(c[-day_1:])/day_1
        ma_2= sum(c[-day_2:])/day_2
        ma_3= sum(c[-day_3:])/day_3
        data["ma_1"][-1]=ma_1
        data["ma_2"][-1]=ma_2
        data["ma_3"][-1]=ma_3
    else :
        pass


def main():
    conn = brokerage.login(url="url", username="wen", password="pikachu", speed=1)
    conn.connect(exchange="BDM", instrument=instrument)
    for d, p in conn.data_stream():
        
        collect_price(d, p)
        visualise_candlesticks()
        is_new_candle = make_candlesticks_day()
        #print(d, p)
        if is_new_candle:
            strategy()
            calculate_ma(day_ma[0], day_ma[1], day_ma[2])
            pass
            
           
            
    conn.logout()
    calculate_profit()
    calculate_win_rate()

main()
