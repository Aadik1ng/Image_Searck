# main.py
from flask import Flask
from routes.routes import api_bp
from dotenv import load_dotenv

# Load environment variables from .env file (if used)
load_dotenv()

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
