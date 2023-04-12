import asyncio
import discord
import yfinance as yf
import pandas as pd
import numpy as np
intents = discord.Intents.default()
intents.members = True  # This line allows the bot to receive member events (optional)
client = discord.Client(intents=intents)

rsi_level = 25
rsi_level_daily = 50

raw_watch_list = pd.read_csv("kienwl.csv")
watch_list = raw_watch_list['Symbol']
async def scan_rsi():
    await client.wait_until_ready()
    channel = client.get_channel(568639807337660416)
    while not client.is_closed():
        # sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        # sp500_list = np.array(sp500[0]['Symbol'])
        for stock in watch_list:
            # if stock == 'AMZN':
            if (stock !='FXA') and (stock != 'SPX') and (stock != 'VIX') and (stock != 'WLL') and (stock != 'M'):
            # rsi = stock.history(period='max').ta.rsi(14)[-1]
                rsi = round(get_rsi(stock),2)
                rsi_daily = round(get_rsi_daily(stock),2)
                if (rsi < rsi_level) and (rsi_daily < rsi_level_daily):
                    # print(stock)
                    await channel.send(f"5 min RSI of {stock} is {rsi}; daily RSI is {rsi_daily}. Buy now!")
        await asyncio.sleep(300) # sleep for 300 seconds

def get_rsi(stock):
    data = yf.download(stock, period='1d', interval='5m')
    close = data['Close']
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.values[-1]

def get_rsi_daily(stock):
    data = yf.download(stock, period='1mo', interval='1d')
    close = data['Close']
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.values[-1]



@client.event
async def on_ready():
    print('Bot is ready.')
    client.loop.create_task(scan_rsi())

if __name__ == '__main__':
    try:
        asyncio.run(client.start('MTA5NTA3OTM5Njk0MDk3MjAzMg.GpUjwf.gSHGW-1Ngplgsfhk4a0T73E9A263k3PWqOoiCg'))
    except KeyboardInterrupt:
        print('KeyboardInterrupt')

