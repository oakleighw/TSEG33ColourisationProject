from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

app.config["IMAGE_UPLOADS"] = "C:/Users/olive/Documents/GitHub/Team Software Development Project/WebDevelopment/static/img/uploads"
app.config["IMAGE_FILETYPES"] = ["PNG", "JPG", "JPEG"]
app.config["MAX_FILESIZE"] = 20971520 #20mb

def imageExtensionCheck(filename):
    if not "." in filename:
        return False
    extension = filename.rsplit(".", 1)[1]

    if extension.upper() in app.config["IMAGE_FILETYPES"]:
        return True
    
    else:
        return False

def imageFileSize(filesize):
    if int(str(filesize)) <= app.config["MAX_FILESIZE"]:
        return True
    else:
        return False

@app.route('/upload-image', methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        
        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("Image must have a filename.")
                return redirect(request.url)
            
            if not imageFileSize(request.cookies.get("filesize")):
                print("File exceeded "+ (str(int(app.config["MAX_FILESIZE"])/1024**2)+"mb."))
                return redirect(request.url)

            if not imageExtensionCheck(image.filename):
                print("Image must be of the filetype: .jpg, .jpeg or .png")
                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            
            print("Image saved")

            return redirect(request.url)

    return render_template('upload_image.html')




if __name__ == "__main__":
    app.run(debug=True)