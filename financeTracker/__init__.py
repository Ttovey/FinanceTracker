from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from financeTracker.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'a temporary secret key'

    db.init_app(app)
    migrate.init_app(app, db)

    from financeTracker.main.routes import main
    from financeTracker.assets.routes import assets
    from financeTracker.debts.routes import debts
    from financeTracker.spending.routes import spending
    from financeTracker.plaid.routes import plaidapi
    from financeTracker.polygon.routes import poly
    app.register_blueprint(main)
    app.register_blueprint(assets)
    app.register_blueprint(debts)
    app.register_blueprint(spending)
    app.register_blueprint(plaidapi)
    app.register_blueprint(poly)

    return app
