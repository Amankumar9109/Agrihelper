from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
import os

app = Flask(__name__)

# Load JSON data from correct file path
DATA_PATH = os.path.join(app.root_path, 'static', 'data', 'market_data.json')
with open(DATA_PATH, 'r') as f:
    market_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(market_data)
print("DataFrame columns:", df.columns)
print(df.head())  # Debugging: Confirm structure

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/community')
def community():
    return render_template('community.html')
    
@app.route('/community/post')
def post():
    return render_template('post.html')
    
@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/weather')
def weather():
    return render_template('weather.html')
    
@app.route('/login')
def login():
    print("Reached /login route")
    return render_template('login.html')

@app.route('/techniques')
def techniques():
    return render_template('modern_farming.html')
    
@app.route('/modern_farming/drip_irrigation')
def drip_irrigation():
    return render_template('drip.html')

@app.route('/modern_farming/soil_health')
def soil_health():
    return render_template('soil.html')

@app.route('/modern_farming/vertical_farming')
def vertical_farming():
    return render_template('vertical.html')

@app.route('/modern_farming/drones_agriculture')
def drones_agriculture():
    return render_template('drones.html')

@app.route('/modern_farming/hydroponics')
def hydroponics():
    return render_template('hydroponics.html')

@app.route('/modern_farming/ai_data_analytics')
def ai_data_analytics():
    return render_template('ai_data.html')

@app.route('/market')
def market():
    states = sorted(df['State'].dropna().unique())
    print("Available states:", states)  # Debugging output
    return render_template('market.html', states=states)

@app.route('/get_options', methods=['POST'])
def get_options():
    data = request.get_json()
    level = data.get('level')
    selection = data.get('selection')

    if level == "district":
        options = df[df['State'] == selection]['District'].dropna().unique()
    elif level == "market":
        options = df[df['District'] == selection]['Market'].dropna().unique()
    elif level == "commodity":
        options = df[df['Market'] == selection]['Commodity'].dropna().unique()
    else:
        options = []

    return jsonify(sorted(options.tolist()))

@app.route('/get_prices', methods=['POST'])
def get_prices():
    data = request.get_json()
    state = data.get('state')
    district = data.get('district')
    market = data.get('market')
    commodity = data.get('commodity')

    # Filter for selected combination
    selected = df[
        (df['State'] == state) &
        (df['District'] == district) &
        (df['Market'] == market) &
        (df['Commodity'] == commodity)
    ]

    if selected.empty:
        return jsonify({'error': 'No data found for selection.'})

    # Average price computation
    prices = {
        'Min Price': round(selected['Min Price'].mean(), 2),
        'Max Price': round(selected['Max Price'].mean(), 2),
        'Modal Price': round(selected['Modal Price'].mean(), 2)
    }

    # Market-wise comparison within state
    state_filtered = df[(df['State'] == state) & (df['Commodity'] == commodity)]
    market_prices = state_filtered.groupby('Market')['Modal Price'].mean().round(2).to_dict()

    # National-level comparison across states
    national_filtered = df[df['Commodity'] == commodity]
    national_prices = national_filtered.groupby('State')['Modal Price'].mean().round(2).to_dict()

    return jsonify({
        'prices': prices,
        'state_comparison': market_prices,
        'national_comparison': national_prices
    })

# Optional: routes for policy pages (if needed)
@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/policy/p1')
def p1():
    return render_template('p1.html')

@app.route('/policy/p2')
def p2():
    return render_template('p2.html')

@app.route('/policy/p3')
def p3():
    return render_template('p3.html')

@app.route('/policy/p4')
def p4():
    return render_template('p4.html')

@app.route('/policy/p5')
def p5():
    return render_template('p5.html')

if __name__ == '__main__':
    app.run(debug=True)

