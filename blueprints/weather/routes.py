from flask import render_template
from . import weather_bp

@weather_bp.route('/weather')
def weather():
    return render_template('weather.html')
