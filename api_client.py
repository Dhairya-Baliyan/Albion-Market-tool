import requests
import time

BASE_URL = "https://west.albion-online-data.com/api/v2/stats/prices"

def fetch_prices(item_id, location):
    full_url = f"{BASE_URL}/{item_id}.json?locations={location}"
    print(f"Calling Url: {full_url}")

    response = requests.get(full_url)
    print(f"Response Status: {response}")
    
    if response.status_code == 200:
        print("Item found successfully.")
        return response.json()
    else:
        print(f"None: {response.status_code}")
    
    time.sleep(0.5)


def search_items(user_input):
    search_url = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.txt"
    response = requests.get(search_url)
    list_of_items = response.text.splitlines()
    matches = []
    for item in list_of_items:
        if user_input.lower() in item.lower():
            matches.append(item)
    return matches


def print_prices(prices):
    if not prices:
        print("No price data available for the specified item and location.")
        return

    print("----- Detailed Price Information -----")

    for item in prices:
        city = item.get('city', 'Unknown')
        quality = item.get('quality', 'Unknown')
        sell = item.get('sell_price_min', 0)
        buy = item.get('buy_price_max', 0)
        if sell == 0 or buy == 0:
            continue

        print(f"City    : {city}, Quality: {quality}")
        print(f"Sell Min: {sell}, Buy Max: {buy}:")
        print("--------------------------------------")

def analyze_prices(prices):
    if not prices:
        print("No price data available for the specified item and location.")
        return
    cheapest_buy = {}
    best_sell = {}

    for item in prices:
        city = item.get('city', 'Unknown')
        quality = item.get('quality', 'Unknown')
        sell_min = item.get('sell_price_min', 0)
        buy_max = item.get('buy_price_max', 0)

        if city not in cheapest_buy or sell_min < cheapest_buy[city]:
            cheapest_buy[city] = sell_min

        if city not in best_sell or buy_max > best_sell[city]:
            best_sell[city] = buy_max     

    best_sell_city = max(best_sell, key=best_sell.get)

    cheapest_buy_city = min(cheapest_buy, key=cheapest_buy.get)

    if best_sell[best_sell_city] == 0 or cheapest_buy[cheapest_buy_city] == 0:
        print("Insufficient data to analyze prices.")
        return
    print("----- Price Analysis -----")

    profit = best_sell[best_sell_city] - cheapest_buy[cheapest_buy_city]

    print(f"Best Buy city: {cheapest_buy_city} at {cheapest_buy[cheapest_buy_city]}")
    print(f"Best Sell City: {best_sell_city} at {best_sell[best_sell_city]}")
    print(f"Potential Profit: {profit}")