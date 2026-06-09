# Arbitrage.ao — Albion Online Market Price Tracker

A web-based market price checker for Albion Online that helps 
players find the best arbitrage opportunities across all royal 
cities without having to travel in-game.

## Live Demo
[Coming soon after deployment]

## Features

- **Item Search** — Search any tradeable item by name with 
  live dropdown suggestions as you type
- **Multi-City Comparison** — Instantly compare prices across 
  all 7 cities: Caerleon, Bridgewatch, Martlock, Lymhurst, 
  Thetford, Fort Sterling and Brecilien
- **Arbitrage Calculator** — Automatically finds the most 
  profitable buy/sell city combinations per quality tier
- **Market Tax Applied** — All profit calculations include 
  the 4% Albion market tax so results are accurate
- **Enchantment Support** — Supports all enchantment levels 
  (@1, @2, @3, @4) for every item
- **Top Opportunities Panel** — Homepage shows the best 
  current flipping opportunities updated every 30 minutes
- **Item Images** — Every item displays its in-game icon 
  from the official Albion render API
- **Troll Listing Filter** — Automatically filters out 
  unrealistic price listings that would skew profit calculations

## Tech Stack

- **Backend** — Python 3, Flask
- **Frontend** — HTML, CSS, JavaScript
- **Data Source** — Albion Online Data Project API
- **Item Images** — Albion Online Render API

## How It Works

1. User searches for an item by name
2. Backend searches a local cache of 9500+ item names
3. User selects the exact item and enchantment level
4. Flask fetches live prices from the Albion Online Data 
   Project API across all cities
5. Profit analysis compares same-quality items across cities
6. Results displayed with best opportunities highlighted

## Project Structure
arbitrage-ao/
├── app.py              # Flask routes and server
├── api_client.py       # API calls, search, profit analysis
├── main.py             # CLI version (development only)
├── items.txt           # Cached item database
├── templates/
│   ├── index.html      # Homepage with search
│   ├── results.html    # Search results page
│   └── prices.html     # Price table and arbitrage page
└── README.md

## Planned Features

- Price history charts using the Albion history API
- Black Market buy order tracker
- Price alerts for specific items
- Mobile responsive design
- Sort prices table by any column

## About

- Built by Dhairya Baliyan — 1st year CSE student at DIT 
  University. Started as a personal tool to check Albion 
  market prices without opening the game repeatedly.
- I am looking forward to add more useful features as 
  part of my coding journey, I want to learn as I build
  something useful.
- The next project will require me to have a deep understanding 
  of everything as it is concerned with real life issues, So I
  am really looking forward to clear my basic concepts and build IT.

Data sourced from the 
[Albion Online Data Project](https://www.albion-online-data.com) 
— a community project that collects market data through a 
client-side plugin.