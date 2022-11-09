from flask import Flask


def create_app():
    app = Flask(__name__)
    
    # app.config.from_pyfile(config_filename)
    with app.app_context():
        from App.views.predict import pred as predict_blueprint
        app.register_blueprint(predict_blueprint)

    return app