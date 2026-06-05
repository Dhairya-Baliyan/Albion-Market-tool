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
    words_to_filter = ["NONTRADABLE", "NONTRADEABLE", "NON_TRADABLE", "ARENA", 
                       "LOOTBAG", "SKIN", "UNIQUE", "VANITY", "GUILD", "QUEST", 
                       "TROPHY", "FOUNDER", "MYSTERY", "XMAX", "HALLOWEEN", 
                       "EASTER", "EVENT"]
    matches = []
    for item in list_of_items:
        parts = item.split(": ")
        if len(parts) <3:
            continue
        item_id = parts[1].strip()
        item_name = parts[2].strip()

        if any(word in item_id.upper() for word in words_to_filter):
            continue

        if "@" in item_id:
                enchant_level = item_id.split("@")[1]
                display_name = item_name + "(Enchantment " + enchant_level + ")"
                if user_input.lower() in display_name.lower():
                    matches.append({"id": item_id, "name": display_name})
        else:
            if user_input.lower() in item_name.lower():
                display_name = item_name
                matches.append({"id": item_id, "name": display_name})
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
    by_quality = {}

    for item in prices:
        quality = item.get('quality', 'Unknown')
        if quality not in by_quality:
            by_quality[quality] = []
        by_quality[quality].append(item)
    
    print("-----Price Analysis-----")

    for quality in by_quality:
        sell_order = None
        sell_city = None
        buy_order = 0
        buy_city = None
        for item in by_quality[quality]:
            city = item.get('city', 'Unknown')
            sell = item.get('sell_price_min', 0)
            buy = item.get('buy_price_max', 0)
            if sell > 0:
                if sell_order is None or sell < sell_order:
                    sell_order = sell
                    sell_city = city
            if buy > buy_order:
                buy_order = buy
                buy_city = city
        
        if sell_city and buy_city:
            profit = sell_order - buy_order
            if profit > 0:
                print(f"Quality {quality}")
                print(f"Buy in: {buy_city} for {buy_order} Silver")
                print(f"Sell in: {sell_city} for {sell_order} Silver")
                print(f"Profit: {profit} Silver")
                print("--------------------------------------")  