# App.py file for the api
from flask import Flask

# Find upload folder
UPLOAD_FOLDER = 'C:/uploads'

app = Flask(__name__)

# Cookie handler ;;
app.secret_key = "secret key"
# Folder config file ;;
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Content limitations ;; I cannot remember the file dimensions
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
