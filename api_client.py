import requests
import time
import os
import threading

cached_opportunities = []
_cache = {"west":None,"east":None,"europe":None}
_cache_time = {"west":0,"east":0,"europe":0}
CACHE_DURATION = 1800

SERVERS = {
    "west": "https://west.albion-online-data.com/api/v2/stats/prices",
    "east": "https://east.albion-online-data.com/api/v2/stats/prices",
    "europe": "https://europe.albion-online-data.com/api/v2/stats/prices"
}

def fetch_prices(item_id, location, server):
    base_url = SERVERS.get(server, SERVERS["west"])
    full_url = f"{base_url}/{item_id}.json?locations={location}"
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

def get_top_opportunities(server):
    global _cache, _cache_time
    current_time = time.time()
    if _cache[server] and (current_time - _cache_time[server]) < CACHE_DURATION:
        return _cache[server] 
    popular_items = [
        # Bags & Capes
        {"id": "T4_BAG", "name": "Adept's Bag"},
        {"id": "T5_BAG", "name": "Expert's Bag"},
        {"id": "T6_BAG", "name": "Master's Bag"},
        {"id": "T4_CAPE", "name": "Adept's Cape"},
        {"id": "T5_CAPE", "name": "Expert's Cape"},
        {"id": "T6_CAPE", "name": "Master's Cape"},
        
        # Faction Capes
        {"id": "T4_CAPEITEM_FW_THETFORD", "name": "Adept's Thetford Cape"},
        {"id": "T4_CAPEITEM_FW_LYMHURST", "name": "Adept's Lymhurst Cape"},
        {"id": "T4_CAPEITEM_FW_FORTSTERLING", "name": "Adept's Fort Sterling Cape"},
        
        # Mounts
        {"id": "T4_MOUNT_HORSE", "name": "Adept's Riding Horse"},
        {"id": "T5_MOUNT_HORSE", "name": "Expert's Riding Horse"},
        {"id": "T4_MOUNT_OX", "name": "Adept's Transport Ox"},
        {"id": "T5_MOUNT_OX", "name": "Expert's Transport Ox"},
        
        # Consumables
        {"id": "T7_MEAL_OMELETTE", "name": "Pork Omelette"},
        {"id": "T8_MEAL_STEW", "name": "Beef Stew"},
        {"id": "T7_MEAL_PORKPIE", "name": "Pork Pie"},
        
        # Materials
        {"id": "RUNE", "name": "Rune"},
        {"id": "SOUL", "name": "Soul"}
    ]

    results = []
    location = "Caerleon,Bridgewatch,Martlock,Lymhurst,Thetford,Fort Sterling,Brecilien"
    for item in popular_items:
        prices = fetch_prices(item["id"], location, server)
        if not prices:
            continue
        analysis = analyze_prices(prices)
        if analysis:
            best = analysis[0]
            results.append({
                "name": item["name"],
                "id": item["id"],
                "profit": best["profit"],
                "buy_city": best["buy_city"],
                "sell_city": best["sell_city"],
                "quality": best["quality"]
            })
    
    results.sort(key=lambda x: x["profit"], reverse=True)
    results = results[:6]
    _cache[server]=results
    _cache_time[server] = current_time
    return results  

def search_recommendations(user_input):
    raw_matches = search_items(user_input)
    query = user_input.lower().strip()
    scored_items = []
    for item in raw_matches:
        item_id = item["id"]
        if "@" in item_id:
            continue
        name = item["name"].lower()
        if name == query:
            tier = 0
        elif name.startswith(query):
            tier = 1
        elif f"{query}" in name:
            tier = 3
        else:
            tier = 3
        filter_words = ["_GROWN","_BABY","ARTEFACT","_SEED","_CROP",",MEAL","_FURNITUREITEM"]
        penalty = 1 if any(kw in item_id for kw in filter_words) else 0

        match_index = name.find(query)
        name_length = len(name)
        scored_items.append({
            "tier": tier,
            "penalty": penalty,
            "match_index": match_index,
            "length": name_length,
            "item_data": item
        })
    scored_items.sort(key=lambda x: (x["tier"], x["penalty"], x["match_index"], x["length"]))
    suggestions = []
    seen_names = set()
    for entry in scored_items:
        item = entry["item_data"]
        item_name = item.get('name') 
        if item_name not in seen_names:
            seen_names.add(item_name)
            suggestions.append(item)
        if len(suggestions) >= 6:
            break
    return suggestions
