import os

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

import db_models.base
from backend.routes.events import events_bp
from backend.routes.livefeed import livefeed_bp
from backend.routes.login import login_bp
from backend.routes.stats import stats_bp

if os.environ.get("DEBUG", 0):
    # Define the base directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Initialize the Flask application with static folder pointing to the React build files
    app = Flask(
        __name__, static_folder=os.path.join(base_dir, "frontend/build"), static_url_path=""
    )
else:
    app = Flask(__name__)

# Initialize the SQLite database
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "smartcam.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
db = SQLAlchemy(app, model_class=db_models.base.Base)
db_models.base.create_tables()


# Register blueprints
app.register_blueprint(events_bp)
app.register_blueprint(livefeed_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(login_bp)


# Serve React build files
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>", methods=["GET"])
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


# Create all tables in the database and start the application
if __name__ == "__main__":
    app.run(debug=bool(os.environ.get("DEBUG", 1)), threaded=True)
