from flask import render_template
from . import farming_bp

@farming_bp.route('/techniques')
def techniques():
    return render_template('modern_farming.html')

@farming_bp.route('/modern_farming/drip_irrigation')
def drip_irrigation():
    return render_template('drip.html')

@farming_bp.route('/modern_farming/soil_health')
def soil_health():
    return render_template('soil.html')

@farming_bp.route('/modern_farming/vertical_farming')
def vertical_farming():
    return render_template('vertical.html')

@farming_bp.route('/modern_farming/drones_agriculture')
def drones_agriculture():
    return render_template('drones.html')

@farming_bp.route('/modern_farming/hydroponics')
def hydroponics():
    return render_template('hydroponics.html')

@farming_bp.route('/modern_farming/ai_data_analytics')
def ai_data_analytics():
    return render_template('ai_data.html')
