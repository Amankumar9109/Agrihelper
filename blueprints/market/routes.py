from flask import render_template, request, jsonify
from . import market_bp
from .data_loader import get_market_dataframe

@market_bp.route('/market')
def market():
    df = get_market_dataframe()
    if 'State' in df.columns:
        states = sorted(df['State'].dropna().unique().tolist())
    else:
        states = []
    return render_template('market.html', states=states)

@market_bp.route('/get_options', methods=['POST'])
@market_bp.route('/market/get_options', methods=['POST'])
def get_options():
    df = get_market_dataframe()
    data = request.get_json() or {}
    level = data.get('level')
    selection = data.get('selection')

    if df.empty:
        return jsonify([])

    if level == "district" and 'State' in df.columns and 'District' in df.columns:
        options = df[df['State'] == selection]['District'].dropna().unique()
    elif level == "market" and 'District' in df.columns and 'Market' in df.columns:
        options = df[df['District'] == selection]['Market'].dropna().unique()
    elif level == "commodity" and 'Market' in df.columns and 'Commodity' in df.columns:
        options = df[df['Market'] == selection]['Commodity'].dropna().unique()
    else:
        options = []

    return jsonify(sorted(options.tolist()))

@market_bp.route('/get_prices', methods=['POST'])
@market_bp.route('/market/get_prices', methods=['POST'])
def get_prices():
    df = get_market_dataframe()
    data = request.get_json() or {}
    state = data.get('state')
    district = data.get('district')
    market_name = data.get('market')
    commodity = data.get('commodity')

    if df.empty:
        return jsonify({'error': 'Market dataset not loaded.'})

    # Filter for selected combination
    selected = df[
        (df['State'] == state) &
        (df['District'] == district) &
        (df['Market'] == market_name) &
        (df['Commodity'] == commodity)
    ]

    if selected.empty:
        return jsonify({'error': 'No data found for selection.'})

    # Average price computation
    prices = {
        'Min Price': round(float(selected['Min Price'].mean()), 2),
        'Max Price': round(float(selected['Max Price'].mean()), 2),
        'Modal Price': round(float(selected['Modal Price'].mean()), 2)
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
