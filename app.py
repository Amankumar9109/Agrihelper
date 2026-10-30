import os
from flask import Flask, request, render_template, jsonify, url_for as flask_url_for
from config import config
from extensions import db, migrate, login_manager

# Ensure models are loaded for SQLAlchemy & Alembic
import models

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # Ensure instance directory exists for SQLite
    instance_dir = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_dir, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    from blueprints.main import main_bp
    from blueprints.auth import auth_bp
    from blueprints.market import market_bp
    from blueprints.store import store_bp
    from blueprints.community import community_bp
    from blueprints.policy import policy_bp
    from blueprints.weather import weather_bp
    from blueprints.farming import farming_bp
    from blueprints.chatbot import chatbot_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(store_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(farming_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(chatbot_bp)

    # Backward compatibility context processor for templates
    @app.context_processor
    def inject_helpers():
        endpoint_aliases = {
            'techniques': 'farming.techniques',
            'drip_irrigation': 'farming.drip_irrigation',
            'soil_health': 'farming.soil_health',
            'vertical_farming': 'farming.vertical_farming',
            'drones_agriculture': 'farming.drones_agriculture',
            'hydroponics': 'farming.hydroponics',
            'ai_data_analytics': 'farming.ai_data_analytics',
            'weather': 'weather.weather',
            'market': 'market.market',
            'policy': 'policy.policy',
            'community': 'community.community',
            'store': 'store.store',
            'login': 'auth.login',
            'post': 'community.post',
            'p1': 'policy.p1',
            'p2': 'policy.p2',
            'p3': 'policy.p3',
            'p4': 'policy.p4',
            'p5': 'policy.p5',
            'home': 'main.home'
        }

        def smart_url_for(endpoint, **values):
            target = endpoint_aliases.get(endpoint, endpoint)
            try:
                return flask_url_for(target, **values)
            except Exception:
                return flask_url_for(endpoint, **values)

        return dict(url_for=smart_url_for)

    # Auto-create tables on startup and apply lightweight migrations if needed
    with app.app_context():
        db.create_all()
        try:
            from sqlalchemy import text
            with db.engine.connect() as conn:
                # Check users columns
                result = conn.execute(text("PRAGMA table_info(users)"))
                columns = [row[1] for row in result.fetchall()]
                if 'last_scheme_check' not in columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN last_scheme_check DATETIME"))
                    conn.commit()

                # Check posts columns
                p_result = conn.execute(text("PRAGMA table_info(posts)"))
                p_columns = [row[1] for row in p_result.fetchall()]
                if 'image_url' not in p_columns:
                    conn.execute(text("ALTER TABLE posts ADD COLUMN image_url VARCHAR(300)"))
                    conn.commit()
                if 'updated_at' not in p_columns:
                    conn.execute(text("ALTER TABLE posts ADD COLUMN updated_at DATETIME"))
                    conn.commit()
        except Exception as e:
            app.logger.warning(f"Schema migration warning: {e}")

    # Register Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Resource not found', 'status_code': 404}), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error', 'status_code': 500}), 500
        return render_template('errors/500.html'), 500

    return app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(debug=True)
