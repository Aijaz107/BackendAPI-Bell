from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import urllib

app = Flask(__name__)
CORS(app)

# Connection string
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS01;"
    "DATABASE=Bell;"
    "Trusted_Connection=yes;"
)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    image = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "image": self.image
        }

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    print(jsonify([user.to_dict() for user in users]))  # Debugging statement to check if users are retrieved
    return jsonify([user.to_dict() for user in users])