import os
import json
from flask import Flask, request, jsonify, flash, redirect, url_for,session
import base64
from flask_cors import CORS
from table_example import convertImageToText, getPathToGCPBucket


#UPLOAD_DIRECTORY = os.path.join(os.getcwd(),"sample")
UPLOAD_DIRECTORY = os.path.join(os.getcwd(),"/tmp")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app=Flask(__name__)

CORS(app)

app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY


@app.route('/image/getText', methods=['POST'])
def get_text_from_image():
    image = request.files['image']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)

@app.route('/upload/parseImage', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return convertImageToText(os.path.join(UPLOAD_DIRECTORY,filename))
    return ""



@app.route('/image/ocr', methods=['GET'])
def process_ocr():
    filename = request.args.get('filename')
    getPathToGCPBucket(filename)
    return convertImageToText(os.path.join(UPLOAD_DIRECTORY,filename))

@app.route('/', methods=['GET'])
def hello():
    return "hello world"

if __name__ == '__main__':
    port2 = int(os.getenv('VCAP_APP_PORT', 8080))
    app.run(host='0.0.0.0',port=8080)
