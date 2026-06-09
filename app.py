from flask import Flask, render_template, request
from api_client import search_items, fetch_prices, analyze_prices

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    item = request.args.get('item', '')
    if not item:
        return render_template('index.html', error="Please Enter A Valid Search Term.")
    results = search_items(item)
    return render_template('results.html', results=results, query=item)

@app.route('/prices')
def prices():
    item_id = request.args.get('id')
    item_name = request.args.get('name')
    location = "Caerleon,Bridgewatch,Martlock,Lymhurst,Thetford,Fort Sterling,Brecilien"
    prices_data = fetch_prices(item_id,location)
    analysis = analyze_prices(prices_data)
    print(f"Analysis results count: {len(analysis)}")
    filtered_prices = []
    for item in prices_data:
        sell_min = item.get('sell_price_min',0)
        sell_max = item.get('sell_price_max',0)
        buy_min = item.get('buy_price_min',0)
        buy_max = item.get('buy_price_max',0)
        if sell_min == 0 and sell_max == 0 and buy_min == 0 and buy_max ==0:
            continue
        filtered_prices.append(item)
    return render_template('prices.html', results=filtered_prices, query=item_name, analysis=analysis)

if __name__ == '__main__':
    app.run(debug=True)