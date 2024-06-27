from flask import Flask, request, send_from_directory, jsonify
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xls', 'xlsx', 'doc', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # Needed for flashing messages

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>

    <head>
        <title>Upload File</title>
    </head>

    <body>
        <h2>Upload File</h2>
        <div id="upload-status"></div>
        <form id="upload-form" action="/upload" method="post" enctype="multipart/form-data">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br><br>
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>

        <script>
            document.getElementById('upload-form').addEventListener('submit', function(event) {
                event.preventDefault(); // Prevent default form submission

                var form = this;
                var formData = new FormData(form); // Create FormData object

                // Make fetch request to upload endpoint
                fetch(form.action, {
                        method: form.method,
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Display upload status message
                        document.getElementById('upload-status').innerHTML = `<p>${data.message}</p>`;
                        form.reset(); // Reset the form
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            });
        </script>
    </body>

    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    username = request.form['username']
    password = request.form['password']
    print(f"Username: {username}, Password: {password}")
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']
    print(f"File: {file}")
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = file.filename
        print(f"Filename: {filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': f'File {filename} uploaded successfully by {username}.'}), 200
    else:
        return jsonify({'message': 'File not allowed'}), 400

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'message': 'File not found'}), 404

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
