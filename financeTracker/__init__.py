from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from financeTracker.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from financeTracker.main.routes import main
    from financeTracker.assets.routes import assets
    from financeTracker.debts.routes import debts
    from financeTracker.spending.routes import spending
    app.register_blueprint(main)
    app.register_blueprint(assets)
    app.register_blueprint(debts)
    app.register_blueprint(spending)

    return app
