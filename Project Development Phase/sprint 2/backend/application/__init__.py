import ibm_db_sa
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import APP_SETTINGS
from flask_cors import CORS
db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(APP_SETTINGS)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    with app.app_context():
        from application.auth.routes import auth_blueprint
        from application.location.routes import locations_blueprint
        from application.product.routes import products_blueprint

        app.register_blueprint(auth_blueprint, url_prefix='/v1/auth')
        app.register_blueprint(products_blueprint, url_prefix='/v1/products')
        app.register_blueprint(locations_blueprint, url_prefix='/v1/locations')

        @jwt.user_identity_loader
        def user_identity_loader(user):
            return user.id

        from application.auth.models import Retailer

        @jwt.user_lookup_loader
        def user_lookup_loader(_jwt_header, jwt_data):
            identity = jwt_data['sub']
            return Retailer.query.filter_by(id=identity).one_or_none()

        import lib.error_handlers.error_handlers

        db.create_all()

    return app
