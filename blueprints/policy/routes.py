from flask import render_template
from . import policy_bp

@policy_bp.route('/policy')
def policy():
    return render_template('policy.html')

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
