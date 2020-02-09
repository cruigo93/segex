from app import *
from flask import render_template
from segmodule import *
import os
import glob
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    session['file_urls'] == []
    file_urls = []
    # print(session['file_urls'])
    files = glob.glob(os.getcwd() + '/uploads/*.jpg')
    for f in files:
        os.remove(f)
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            
            filename = photos.save(
                file,
                name=file.filename    
            )
            # append image urls
            file_urls.append(photos.url(filename))
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request    
    return render_template('index.html')
@app.route('/results')
def results():
    
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    if len(file_urls) > 0:
        img_file = file_urls[-1]
    else:
        img_file = file_urls

    print("ggggg", file_urls)
    img_file = os.path.basename(img_file)
    predict_mask(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], img_file))
    session.pop('file_urls', None)
    file_url = file_urls[0]
    file_url = file_url[:-4] + '_mask.png'
    file_urls.append(file_url)
    return render_template('results.html', file_urls=file_urls)