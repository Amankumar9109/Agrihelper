from datetime import datetime
from flask import render_template, request, jsonify
from flask_login import current_user
from extensions import db
from services.scheme_service import (
    get_all_schemes,
    get_scheme_by_id,
    get_scheme_by_code,
    sync_schemes_cache,
    evaluate_eligibility
)
from . import policy_bp

@policy_bp.route('/policy')
@policy_bp.route('/schemes')
def policy():
    selected_category = request.args.get('category', 'All')
    search_query = request.args.get('q', '').strip()

    # Calculate new schemes for logged-in user
    new_schemes_count = 0
    if current_user.is_authenticated:
        if current_user.last_scheme_check:
            from models.scheme import GovernmentScheme
            new_schemes_count = GovernmentScheme.query.filter(
                GovernmentScheme.last_updated > current_user.last_scheme_check
            ).count()
        # Update user's last_scheme_check timestamp
        current_user.last_scheme_check = datetime.utcnow()
        db.session.commit()

    schemes = get_all_schemes(category=selected_category, search=search_query)

    # Categories list for filter pills
    categories = [
        'All',
        'Financial Aid',
        'Crop Insurance',
        'Market Access',
        'Credit & Loans',
        'Irrigation & Solar',
        'Organic Farming',
        'Inputs & Testing'
    ]

    return render_template(
        'policy.html',
        schemes=schemes,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        new_schemes_count=new_schemes_count,
        total_schemes=len(schemes)
    )

@policy_bp.route('/api/schemes')
def api_schemes():
    category = request.args.get('category', 'All')
    search = request.args.get('search', request.args.get('q', ''))
    schemes = get_all_schemes(category=category, search=search)
    return jsonify({
        'success': True,
        'count': len(schemes),
        'schemes': [s.to_dict() for s in schemes]
    })

@policy_bp.route('/api/schemes/<int:scheme_id>')
def api_scheme_detail(scheme_id):
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        return jsonify({'error': 'Scheme not found'}), 404
    return jsonify({'success': True, 'scheme': scheme.to_dict()})

@policy_bp.route('/api/schemes/refresh', methods=['POST'])
def api_refresh_schemes():
    count = sync_schemes_cache(force=True)
    return jsonify({
        'success': True,
        'message': f'Successfully synchronized {count} government schemes.',
        'count': count,
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    })

@policy_bp.route('/api/schemes/check-eligibility', methods=['POST'])
def api_check_eligibility():
    data = request.get_json() or {}
    land_size = data.get('land_size', 'small')
    farm_type = data.get('farm_type', 'crops')
    primary_need = data.get('primary_need', 'cash')

    matches = evaluate_eligibility(land_size, farm_type, primary_need)
    return jsonify({
        'success': True,
        'total_matches': len(matches),
        'matches': matches
    })

# Backward compatibility routes for p1–p5 detailed pages
@policy_bp.route('/policy/p1')
def p1():
    return render_template('p1.html')

@policy_bp.route('/policy/p2')
def p2():
    return render_template('p2.html')

@policy_bp.route('/policy/p3')
def p3():
    return render_template('p3.html')

@policy_bp.route('/policy/p4')
def p4():
    return render_template('p4.html')

@policy_bp.route('/policy/p5')
def p5():
    return render_template('p5.html')
