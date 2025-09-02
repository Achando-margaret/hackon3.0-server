from app import create_app, db
from flask_cors import CORS

# create app from factory
app = create_app()

# enable CORS
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
