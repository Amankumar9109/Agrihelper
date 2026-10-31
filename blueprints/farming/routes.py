import os
import json
from flask import render_template, request, jsonify, current_app, abort
from . import farming_bp
from services.technique_service import (
    get_all_techniques,
    get_technique_by_slug,
    get_technique_by_id,
    get_categories,
    calculate_technique_roi,
    TECHNIQUES_CATALOG
)
from services.scheme_service import get_scheme_by_code

def _load_store_products():
    """Loads store products from products.json"""
    try:
        path = os.path.join(current_app.root_path, 'static', 'data', 'products.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        current_app.logger.error(f"Error loading products in farming routes: {e}")
    return []

@farming_bp.route('/techniques')
def techniques():
    category = request.args.get('category', 'All')
    search_query = request.args.get('q', '').strip()

    techniques_list = get_all_techniques(category=category, search=search_query)
    categories = get_categories()

    return render_template(
        'modern_farming.html',
        techniques=techniques_list,
        categories=categories,
        selected_category=category,
        search_query=search_query,
        total_techniques=len(techniques_list)
    )

@farming_bp.route('/techniques/<slug>')
def technique_detail(slug):
    technique = get_technique_by_slug(slug)
    if not technique:
        abort(404)

    all_products = _load_store_products()
    related_products = [
        p for p in all_products
        if p.get('id') in technique.get('related_products', [])
    ]

    related_schemes = []
    for code in technique.get('related_schemes', []):
        scheme = get_scheme_by_code(code)
        if scheme:
            related_schemes.append(scheme)

    roi_summary = calculate_technique_roi(technique['slug'], farm_acres=1.0)

    return render_template(
        'technique_detail.html',
        technique=technique,
        related_products=related_products,
        related_schemes=related_schemes,
        roi_summary=roi_summary
    )

# Backward compatibility routes
@farming_bp.route('/modern_farming/drip_irrigation')
def drip_irrigation():
    technique = get_technique_by_slug('drip-irrigation')
    all_products = _load_store_products()
    related_products = [p for p in all_products if p.get('id') in technique.get('related_products', [])]
    related_schemes = [get_scheme_by_code(c) for c in technique.get('related_schemes', []) if get_scheme_by_code(c)]
    roi_summary = calculate_technique_roi('drip-irrigation', farm_acres=1.0)
    return render_template('drip.html', technique=technique, related_products=related_products, related_schemes=related_schemes, roi_summary=roi_summary)

@farming_bp.route('/modern_farming/soil_health')
def soil_health():
    technique = get_technique_by_slug('soil-health')
    all_products = _load_store_products()
    related_products = [p for p in all_products if p.get('id') in technique.get('related_products', [])]
    related_schemes = [get_scheme_by_code(c) for c in technique.get('related_schemes', []) if get_scheme_by_code(c)]
    roi_summary = calculate_technique_roi('soil-health', farm_acres=1.0)
    return render_template('soil.html', technique=technique, related_products=related_products, related_schemes=related_schemes, roi_summary=roi_summary)

@farming_bp.route('/modern_farming/vertical_farming')
def vertical_farming():
    technique = get_technique_by_slug('vertical-farming')
    all_products = _load_store_products()
    related_products = [p for p in all_products if p.get('id') in technique.get('related_products', [])]
    related_schemes = [get_scheme_by_code(c) for c in technique.get('related_schemes', []) if get_scheme_by_code(c)]
    roi_summary = calculate_technique_roi('vertical-farming', farm_acres=1.0)
    return render_template('vertical.html', technique=technique, related_products=related_products, related_schemes=related_schemes, roi_summary=roi_summary)

@farming_bp.route('/modern_farming/drones_agriculture')
def drones_agriculture():
    technique = get_technique_by_slug('drones-agriculture')
    all_products = _load_store_products()
    related_products = [p for p in all_products if p.get('id') in technique.get('related_products', [])]
    related_schemes = [get_scheme_by_code(c) for c in technique.get('related_schemes', []) if get_scheme_by_code(c)]
    roi_summary = calculate_technique_roi('drones-agriculture', farm_acres=1.0)
    return render_template('drones.html', technique=technique, related_products=related_products, related_schemes=related_schemes, roi_summary=roi_summary)

@farming_bp.route('/modern_farming/hydroponics')
def hydroponics():
    technique = get_technique_by_slug('hydroponics')
    all_products = _load_store_products()
    related_products = [p for p in all_products if p.get('id') in technique.get('related_products', [])]
    related_schemes = [get_scheme_by_code(c) for c in technique.get('related_schemes', []) if get_scheme_by_code(c)]
    roi_summary = calculate_technique_roi('hydroponics', farm_acres=1.0)
    return render_template('hydroponics.html', technique=technique, related_products=related_products, related_schemes=related_schemes, roi_summary=roi_summary)

@farming_bp.route('/modern_farming/ai_data_analytics')
def ai_data_analytics():
    technique = get_technique_by_slug('ai-data-analytics')
    all_products = _load_store_products()
    related_products = [p for p in all_products if p.get('id') in technique.get('related_products', [])]
    related_schemes = [get_scheme_by_code(c) for c in technique.get('related_schemes', []) if get_scheme_by_code(c)]
    roi_summary = calculate_technique_roi('ai-data-analytics', farm_acres=1.0)
    return render_template('ai_data.html', technique=technique, related_products=related_products, related_schemes=related_schemes, roi_summary=roi_summary)

# API Endpoints
@farming_bp.route('/api/techniques')
def api_techniques():
    category = request.args.get('category', 'All')
    search = request.args.get('search', request.args.get('q', ''))
    techniques_list = get_all_techniques(category=category, search=search)
    return jsonify({
        'success': True,
        'count': len(techniques_list),
        'techniques': techniques_list
    })

@farming_bp.route('/api/techniques/<slug>')
def api_technique_detail(slug):
    technique = get_technique_by_slug(slug)
    if not technique:
        return jsonify({'error': 'Technique not found'}), 404
    return jsonify({
        'success': True,
        'technique': technique
    })

@farming_bp.route('/api/techniques/calculate-roi', methods=['POST'])
def api_calculate_roi():
    data = request.get_json() or {}
    slug = data.get('technique', 'drip-irrigation')
    try:
        acres = float(data.get('acres', 1.0))
    except (ValueError, TypeError):
        acres = 1.0
    crop = data.get('crop', 'General')

    calc_result = calculate_technique_roi(slug, farm_acres=acres, crop_type=crop)
    return jsonify({
        'success': True,
        'data': calc_result
    })
