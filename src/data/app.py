from flask import Flask
from routes.consultant_sessions_routes import consultant_sessions_bp
from routes.consultants_routes import consultants_bp
from routes.customers_routes import customers_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(consultant_sessions_bp)
app.register_blueprint(consultants_bp)
app.register_blueprint(customers_bp)

if __name__ == "__main__":
    app.run()