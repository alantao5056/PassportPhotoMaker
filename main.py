from flask import Flask, request, jsonify, json
from flask_restful import Api, Resource, reqparse
import werkzeug
import os
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)
 
UPLOAD_FOLDER = 'files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class HelloWorld(Resource):
  def post(self):
    # check if the post request has the file part
    if 'files[]' not in request.files:
      resp = jsonify({'message' : 'No file part in the request'})
      resp.status_code = 400
      return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
     
    for file in files:      
      if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        success = True
      else:
        errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
      errors['message'] = 'File(s) successfully uploaded'
      resp = jsonify(errors)
      resp.status_code = 500
      return resp
    if success:
      resp = jsonify({'message' : 'Files successfully uploaded'})
      resp.status_code = 201
      return resp
    else:
      resp = jsonify(errors)
      resp.status_code = 500
      return resp

api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
  app.run(debug=True)