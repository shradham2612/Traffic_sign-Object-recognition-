from flask import Flask, render_template, request, session
import os
import shutil
from werkzeug.utils import secure_filename
import subprocess
#*** Backend operation
 
# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'
 
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)#x.jpg
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
       
        # print(img_filename)
       
        
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

        
        cmd2=r"python yolov5/detect.py --weights best.pt --source "+"staticFiles/uploads/"+img_filename#x.jpg
        print(cmd2)
        
        subprocess.call(cmd2,shell=True)
        #change image directory
        origin = 'yolov5/runs/detect/exp/'
        target = 'staticFiles/output/'

        # Fetching the list of all the files
        files = os.listdir(origin)

        # Fetching all the files to directory
        for file_name in files:
            shutil.copy(origin+file_name, target+file_name)
            print("Files are copied successfully")
        
        # code to delete directory
        shutil.rmtree('yolov5/runs/detect/exp')
        #rename
        source = 'staticFiles/output/'+img_filename
  
        # destination file path
        dest = 'staticFiles/output/'+'output.jpg'
        os.rename(source,dest)
        return render_template('index1.html')
 
@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    # img_file_path = session.get('staticFiles/output/output.jpg', None)
    
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = 'staticFiles/output/output.jpg')

@app.route('/reset')
def reset():
    myfile = "staticFiles/output/output.jpg"
    # If file exists, delete it.
    if os.path.isfile(myfile):
        os.remove(myfile)
    return render_template('index.html')
 
if __name__=='__main__':
    app.run(debug = True)