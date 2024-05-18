import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from backend.routes.events import events_bp
from backend.routes.livefeed import livefeed_bp
from backend.routes.stats import stats_bp

# Initialize the Flask application
app = Flask(__name__)

# Initialize the SQLite database
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "smartcam.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(events_bp)
app.register_blueprint(livefeed_bp)
app.register_blueprint(stats_bp)


# Create all tables in the database and start the application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, threaded=True)
