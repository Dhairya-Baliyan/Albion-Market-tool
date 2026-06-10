from flask import Flask, render_template, request, jsonify
from api_client import search_items, fetch_prices, analyze_prices, get_top_opportunities,search_recommendations

app = Flask(__name__)

@app.route('/')
def home():
    server = request.args.get('server', 'west')
    opportunities = get_top_opportunities(server)
    return render_template('index.html', opportunities=opportunities,server=server)

@app.route('/api/autocomplete')
def autocomplete():
    query = request.args.get('q','').strip()
    if not query:
        return jsonify([])
    suggestions = search_recommendations(query)
    return jsonify(suggestions)

@app.route('/search')
def search():
    item = request.args.get('item','')
    server = request.args.get('server','west')
    if not item:
        return render_template('index.html',error="Please Enter A Valid Search Term.")
    results = search_items(item)
    return render_template('results.html',results=results,query=item,server=server)

@app.route('/prices')
def prices():
    item_id = request.args.get('id')
    item_name = request.args.get('name')
    server = request.args.get('server','west')
    location = "Caerleon,Bridgewatch,Martlock,Lymhurst,Thetford,Fort Sterling,Brecilien"
    prices_data = fetch_prices(item_id,location,server)
    analysis = analyze_prices(prices_data)
    filtered_prices = []
    for item in prices_data:
        sell_min = item.get('sell_price_min',0)
        sell_max = item.get('sell_price_max',0)
        buy_min = item.get('buy_price_min',0)
        buy_max = item.get('buy_price_max',0)
        if sell_min == 0 and sell_max == 0 and buy_min == 0 and buy_max ==0:
            continue
        filtered_prices.append(item)
    return render_template('prices.html', results=filtered_prices, query=item_name, analysis=analysis, item_id=item_id)

if __name__ == '__main__':
    app.run(debug=True)