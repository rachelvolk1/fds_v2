from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'csv'}

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
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(filepath)
                df = pd.read_csv(filepath, delimiter=request.form.get('delimiter', ','))
                df = handle_missing_values(df, request.form.get('missingValue'))
                if request.form.get('dateFormat'):
                    df['Date'] = pd.to_datetime(df['Date'], format=request.form['dateFormat'])
                df.to_csv(filepath, index=False)  # Save processed data
                preview_html = df.head(10).to_html(classes='data')
                return redirect(url_for('preview_file', filename=filename))
            except FileNotFoundError:
                flash('Error saving file')
                return redirect(request.url)

    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        preview_html = df.head(10).to_html(classes='data')  # You can customize preview here
        return render_template('preview.html', data_preview=preview_html, filename=filename)
    else:
        flash('File not found')
        return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
