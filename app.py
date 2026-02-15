from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_url_path='/uploads', static_folder='uploads')


# Allow CORS for all origins
CORS(app)

# MySQL Configuration using Flapp = Flask(__name__, static_url_path='/uploads', static_folder='uploads')ask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://myadmin:123456@localhost:3306/flask_crud'  # Update with your credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Secret key for CSRF protection
app.config['SECRET_KEY'] = 'yofdgusdfsdffdsfdsdfddsfsdfrsecretkey'

# Create a folder to store uploaded images
app.config['UPLOAD_FOLDER'] = 'uploads/photos'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Allowed file extensions for the images
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


# User Model for the database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))  # Only store the filename, not the full path

    def __repr__(self):
        return f''

# Function to check allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/api/users', methods=['POST'])
def create_user():
    # Check if the image file is in the form data
    if 'image' not in request.files:
        return jsonify({'message': 'No image file found'}), 400

    image = request.files['image']

    # Validate the image file extension
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
    else:
        return jsonify({'message': 'Invalid image format. Only jpg, jpeg, and png allowed.'}), 400

    # Get other form data (text fields)
    data = request.form

    # Print the data to inspect which field is missing
    print("Received data:", data)

    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        print(f"Missing fields: {missing_fields}")  # This will show the missing fields
        return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    # Retrieve form data
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    # Create a new user in the database
    new_user = Users(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        image=filename  # Store only the filename here
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created'}), 201

# Route for viewing all users
@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    users_list = []
    for user in users:
        users_list.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'image': user.image  # Only send the filename, not the full path
        })
    return jsonify(users_list), 200


# Route for viewing a single user
@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'image': user.image
    }), 200


@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.form

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)

    # Handle image if provided
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            user.image = filename
        else:
            return jsonify({'message': 'Invalid image format'}), 400

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Delete image file if exists
    if user.image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], user.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)