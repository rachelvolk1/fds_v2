from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.decision_tree import train_decision_tree_model
from models.random_forest import train_random_forest_model
from models.svm import train_svm_model
import os
import pandas as pd
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'  # Necessary for flash messages
app.config['STATIC_FOLDER'] = 'static'

# Dummy in-memory database for example purposes
users = {
    "user@example.com": "password"
}

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_missing_values(df, method):
    if method == 'remove':
        return df.dropna()
    elif method == 'mean':
        return df.fillna(df.mean())
    elif method == 'median':
        return df.fillna(df.median())
    elif method == 'mode':
        return df.fillna(df.mode().iloc[0])
    else:
        return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

#login, register and forgot password
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        else:
            users[username] = generate_password_hash(password)
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Implement logic to handle forgot password functionality (e.g., sending a reset link via email)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html') 

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'fileUpload' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['fileUpload']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = f"{int(time.time())}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)

                # Process CSV or Excel based on extension
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)

                # Handle missing values if needed
                df = handle_missing_values(df, request.form.get('missingValue'))

                # Handle date formatting if needed
                if 'dateFormat' in request.form and 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], format=request.form['dateFormat'])

                # Instead of saving back, send data to preview
                return redirect(url_for('preview_file', filename=filename))

            except Exception as e:
                flash(f'Error processing file: {str(e)}')
                return redirect(request.url)
        else:
            flash('Unsupported file type')
            return redirect(request.url)
    
    # If GET request, render the file upload form
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        # Load the dataset depending on the file extension
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        # Get the first 10 rows for preview
        preview_df = df.head(10)

        # Convert to HTML for frontend preview
        preview_html = preview_df.to_html(classes='data', table_id='data-table', index=False)

        # Render preview page with the HTML table
        return render_template('preview.html', data_preview=preview_html, filename=filename)
    else:
        flash('File not found')
        return redirect(url_for('upload_file'))

@app.route('/api/preview/<filename>', methods=['GET'])
def upload_dataset(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        # Load the dataset based on the file extension
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        # Convert DataFrame to JSON for DataTables
        data = df.to_dict(orient='records')

        return jsonify(data)
    else:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/load_dataset', methods=['POST'])
def load_dataset():
    filename = request.form.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath) if filename.endswith('.csv') else pd.read_excel(filepath)
            # Code to load data into your database goes here
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    else:
        return jsonify({'success': False, 'error': 'File not found'})

@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        model_type = request.form.get('model-type')
        filename = request.form.get('filename')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            if model_type == 'decision_tree':
                train_decision_tree_model(filepath)
            elif model_type == 'random_forest':
                train_random_forest_model(filepath)
            elif model_type == 'svm':
                train_svm_model(filepath)
            
            return jsonify({'message': 'Training started successfully.', 'progress': 0})
        else:
            return jsonify({'error': 'File not found'})
    
    return render_template('train.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        feature_1 = request.form.get('individualFeature_1')
        feature_2 = request.form.get('individualFeature_2')
        
        response = {
            'feature_1': feature_1,
            'feature_2': feature_2
        }
        return jsonify(response)

    return render_template('test.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        response = {
            'status': 'Results complete'
        }
        return jsonify(response)

    return render_template('results.html')

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        response = {
            'status': 'Analysis data received'
        }
        return jsonify(response)

    return render_template('analysis.html')

# Inbox Routes
@app.route('/upload_inbox', methods=['GET', 'POST'])
def upload_inbox():
    if request.method == 'POST':
        # Handle the uploaded file for inbox processing
        flash('Inbox upload successful!', 'success')
    return render_template('upload_inbox.html')

@app.route('/train_inbox', methods=['GET', 'POST'])
def train_inbox():
    if request.method == 'POST':
        # Handle the training process for inbox data
        flash('Inbox training started!', 'success')
    return render_template('train_inbox.html')

@app.route('/test_inbox', methods=['GET', 'POST'])
def test_inbox():
    if request.method == 'POST':
        # Handle the testing process for inbox data
        flash('Inbox testing started!', 'success')
    return render_template('test_inbox.html')

@app.route('/analysis_inbox', methods=['GET', 'POST'])
def analysis_inbox():
    if request.method == 'POST':
        # Handle the analysis process for inbox data
        flash('Inbox analysis started!', 'success')
    return render_template('analysis_inbox.html')

@app.route('/results_inbox', methods=['GET', 'POST'])
def results_inbox():
    if request.method == 'POST':
        # Handle the results process for inbox data
        flash('results!', 'success')
    return render_template('results_inbox.html')


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)


@app.route('/create_user')
def create_user():
    # Logic for creating a new user
    return render_template('create_user.html')

@app.route('/list_users')
def list_users():
    # Logic for listing existing users
    return render_template('list_users.html', users=users)