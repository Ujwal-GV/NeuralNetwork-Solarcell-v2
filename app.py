from flask import Flask, render_template, request, jsonify, redirect, url_for
import train_model
import test
import matplotlib
import os
from flask_cors import CORS

# Configure Matplotlib to work in a server environment
matplotlib.use('Agg')

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to save uploaded images
def save_image(image_file):
    # Define the directory where images will be saved
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    # Save the image to the uploads directory
    image_path = os.path.join(upload_dir, image_file.filename)
    image_file.save(image_path)
    
    return image_path

# Validate allowed file extensions for image uploads
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define routes
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'UG' and password == 'UG2002':
            return redirect(url_for('index'))
        else:
            error_message = "Incorrect username or password. Please try again."
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/train')
def train_func():
    return render_template('train.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/train_model', methods=['POST'])
def train():
    try:
        train_model.process()
        return jsonify({'message': 'Training completed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['POST'])
def predict_image():
    try:
        # Get the uploaded image file
        image_file = request.files.get('image')
        if not image_file:
            return jsonify({'error': 'No file provided'}), 400
        if not allowed_file(image_file.filename):
            return jsonify({'error': 'Unsupported file type'}), 400

        # Save the image and get its path
        image_path = save_image(image_file)
        
        # Get prediction result
        prediction = test.predict_process(image_path)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Use the port defined in environment variables or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True, threaded=False)
