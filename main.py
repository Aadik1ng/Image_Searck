# main.py
from flask import Flask
from api.routes import routes
from setup.initializer import initialize

app = Flask(__name__)
app.register_blueprint(routes)

# Initialize the app state explicitly before starting the server
embeddings, image_paths = initialize()
app.config['embeddings'] = embeddings
app.config['image_paths'] = image_paths

if __name__ == '__main__':
    app.run(debug=True)
