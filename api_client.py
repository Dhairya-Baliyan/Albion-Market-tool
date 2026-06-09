import requests
import time
import os

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
    if os.path.exists("items.txt"):
        with open("items.txt", "r", encoding="utf-8") as f:
            content = f.read()
    else:
        search_url = "https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.txt"
        response = requests.get(search_url)
        content = response.text
        with open("items.txt", "w", encoding="utf-8") as f:
            f.write(content)

    list_of_items = content.splitlines()
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
    print(f"{'City':<15} {'Quality':<10} {'Sell Order':<12} {'Buy Order':<12}")

    by_quality = {}
    for item in prices:
        quality = item.get('quality', 'Unknown')
        if quality not in by_quality:
            by_quality[quality] = []
        by_quality[quality].append(item)

    for quality in by_quality:
        for item in by_quality[quality]:

            city = item.get('city', 'Unknown')
            sell_order = item.get('sell_price_min', 0)
            buy_order = item.get('buy_price_max', 0)

            if sell_order == 0 and buy_order == 0:
                continue

            print(f"{city:<15} {quality:<10} {sell_order:<12} {buy_order:<12}")

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
    results= []

    for quality, items in by_quality.items():
        for city_1 in items:
            buy_price = city_1.get('sell_price_min',0)
            buy_city = city_1.get('city', 'Unknown')
            if buy_price == 0:
                continue
            for city_2 in items:
                sell_price = city_2.get('sell_price_min',0)
                sell_city = city_2.get('city','Unknown')
                if buy_city == sell_city or sell_price == 0:
                    continue
                if sell_price < 1000:
                    continue
                profit = int((sell_price * 0.96) - buy_price)
                if profit <= 0 or profit > 50000:
                    continue
                if profit > 0:
                    results.append({
                    "quality": quality,
                    "buy_city": buy_city,
                    "buy_price": buy_price,
                    "sell_city": sell_city,
                    "sell_price": sell_price,
                    "profit": profit
                    })
    
    results.sort(key=lambda x: x['profit'], reverse=True)
    results = results[:15]
    return results
