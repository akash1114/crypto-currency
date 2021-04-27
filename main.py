
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# -*- coding: utf-8 -*-

from pycoingecko import CoinGeckoAPI
import pandas as pd
import sys
import datetime
import time

cg = CoinGeckoAPI()


# collecting data of 2500 coins
def market_price():
    m_p = []
    for i in range(1, 11):
        m_p.extend(cg.get_coins_markets('usd', page=i, per_page=250))
    return m_p


# collecting useful data
def collect_data(market_details):
    data = {}
    name = []
    symbol = []
    market_cap = []
    current_price = []
    percentage_change = []
    ids = []

    for coin in market_details:
        symbol.append(coin['symbol'])
        market_cap.append(round(coin['market_cap'] / 1000000, 2))

        try:
            current_price.append(round(coin['current_price'], 2))
        except:
            current_price.append(0)
        name.append(url(coin['name']))
        percentage_change.append(round(percentage_diff(coin['ath'], current_price=coin['current_price']), 2))
        ids.append(coin['id'])

    data['Name'] = name
    data['Coin Symbol(ticker)'] = symbol
    data['Market Cap(In Millions)'] = market_cap
    data['Current Price'] = current_price
    data['Percentage Change on ATH'] = percentage_change
    data['ids'] = ids

    return data


#total exchange count of one coin
# def total_count(id):
#     binance_count = count('binance', id)
#     hitbtc_count = count('hitbtc', id)
#     binance_us = count('binance_us', id)
#     kucoin = count('kucoin', id)
#     uniswap = count('uniswap', id)
#     gemini = count('gemini', id)
#     return binance_count + hitbtc_count + binance_us + kucoin + uniswap + gemini


#exchange count of one coinfor a exchange
# def count(id, coin):
#     coin_exchange = cg.get_exchanges_tickers_by_id(id=id, coin_ids=coin)
#     if len(coin_exchange['tickers']) == 100:
#         return 0
#     return len(coin_exchange['tickers'])


#exchange count
# def e_count(df):
#     count = 1
#     exchange_count = []
#     for i in list(df['ids']):
#         exchange_count.append(total_count(i))
#         if count % 7 == 0:
#             print(count)
#             time.sleep(60)
#         count += 1
#     return exchange_count


#collecting all listed exchange details for 6 exchanges

def exchange_deta():
    exchanges = ['binance', 'hitbtc', 'binance_us', 'kucoin', 'uniswap', 'gemini']
    exchange_details = []
    for exchange in exchanges:
        for page_no in range(1, 20):
            exchange_data = cg.get_exchanges_tickers_by_id(exchange, page=page_no)
            if (len(exchange_data['tickers']) == 0):
                break
            exchange_details.extend(exchange_data['tickers'])
        print(exchange, len(exchange_details))
    return exchange_details


#counting exchange for selected coins
def exchange_count(df):
    exchange_count = {}
    ids = list(df['ids'])
    exchange_details = exchange_deta()
    for exchange in exchange_details:
        if exchange['coin_id'] in ids:
            if exchange['coin_id'] in exchange_count.keys():
                exchange_count[exchange['coin_id']] += 1
            else:
                exchange_count[exchange['coin_id']] = 1
    exchange_list = []
    for id in list(df['ids']):
        if id in exchange_count.keys():
            exchange_list.append(exchange_count[id])
        else:
            exchange_list.append(0)
    return exchange_list


def percentage_diff(ath, current_price):
    try:
        return 100 * (ath - current_price) / ath
    except:
        return 0


# hyperlink of coin
def url(name):
    coin = name.lower()
    QM = '"'

    if len(str.split(coin)) > 1:

        link = "https://www.coingecko.com/en/coins/" + "-".join([str(num) for num in str.split(coin)])

    else:
        link = "https://www.coingecko.com/en/coins/" + coin

    output = "=HYPERLINK(" + QM + link + QM + "," + QM + name + QM + ")"

    return output


# main function to maintain execution flow
def main():
    # User Input

    print("Do you want to add custome values ? yes/no")
    choice = input()

    if choice == 'Yes' or choice == 'yes':

        # Values entered by user
        print("Enter Number of coins to download...")
        number = int(input())

        print("What is the lower limit of market cap (in Millions)?")
        lower_limit = float(input())
        print("What is the Upper limit of market cap (in Millions)?")
        upper_limit = float(input())

        if lower_limit >= upper_limit:
            sys.exit("Please provide correct limits...")

        print("What is the lower limit of percenntage change in Current price of all time high")
        pr_lower_limit = float(input())
        print("What is the Upper limit of percenntage change in Current price of all time high")
        pr_upper_limit = float(input())

        if pr_lower_limit >= pr_upper_limit:
            sys.exit("Please provide correct limits...")

    else:
        # default Values
        number = 50
        lower_limit = 1
        upper_limit = 100
        pr_lower_limit = 10
        pr_upper_limit = 20

    # Collecting Data
    m_p = market_price()

    # Selecting Usefull Data
    data = collect_data(m_p)

    # Converting to dataframe
    df = pd.DataFrame.from_dict(data)

    # Querying lower and upper limit
    df_market_cap = df[(df['Market Cap(In Millions)'] > lower_limit) & (df['Market Cap(In Millions)'] < upper_limit)]
    df_query = df_market_cap[(df_market_cap['Percentage Change on ATH'] > pr_lower_limit) & (
            df_market_cap['Percentage Change on ATH'] <= pr_upper_limit)]

    # Selecting numbers of coins
    df_final = df_query.head(number)

    #counting exchanges
    df_final['No. of Exchanges'] = exchange_count(df_final)

    # Sorting

    print("Your data is ready...")

    print("Press 1 to sort it by Name")

    print("Press 2 to sort it by Coin Symbol")

    print("Press 3 to sort it by Market Cap")

    print("Press 4 to sort it by Current Price")

    print("Press 5 to sort it by Percentage Change on ATH")

    print("Press 6 for defualt sorting....")

    sort = int(input())

    columns = ['index', 'Name', 'Coin Symbol(ticker)', 'Market Cap(In Millions)', 'Current Price',
               'Percentage Change on ATH']

    if 0 < sort < 6:
        df_sorted = df_final.sort_values(by=[columns[sort]])

    else:
        df_sorted = df_final

    # Sorting end

    df_sorted.drop('ids',inplace=True, axis=1)

    # Saving file
    df_sorted.to_csv('Data-' + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + '.csv', index=False)


main()
