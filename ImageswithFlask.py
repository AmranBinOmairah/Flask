#!/usr/bin/env python
# coding: utf-8

# # Images with Flask

# ### Importing the libraries

# In[1]:


import os
import uuid
import numpy as np 
import pandas as pd
from io import BytesIO
from flask import Flask, request, jsonify, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image, ImageFile
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input, decode_predictions


# In[2]:


ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_HEIGHT = 224
IMAGE_WIDTH = 224
IMAGE_CHANNELS = 3
#os.chdir(r'D:\Courses\Udemy\Deploying Machine Learning Models with Flask\flaskdata\flaskdata')
#os.getcwd()


# In[3]:


def allowed_file(filename):
    return '.' in filename and     filename.rsplit('.', 1)[1] in ALLOWED_EXTENSION


# In[4]:


app = Flask(__name__)
model = MobileNet(weights='imagenet', include_top=True)

@app.route('/')
def index():
    return render_template('ImageML.html')

@app.route('/api/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return render_template('ImageML.html', prediction='No posted image. Should be attribute named image')
    file = request.files['image']
    
    if file.filename == '':
        return render_template('ImageML.html', prediction= 'You did not select an image')
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("****"+filename)
        x = []
        ImageFile.LOAD_TRUNCATED_IMAGES = False
        img = Image.open(BytesIO(file.read()))
        img.load()
        img = img.resize((IMAGE_HEIGHT, IMAGE_WIDTH), Image.ANTIALIAS)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        pred = model.predict(x)
        lst = decode_predictions(pred, top=3)
        
        items = []
        for item in lst[0]:
            items. append({'name': item[1], 'prob': float(item[2])})
            
        response = {'pred': items}
        return render_template('ImageML.html', prediction= 'I would say the image is most likely {}'.format(response))
    else:
        return render_template('ImageML.html', prediction= 'Invalid File Extension!')
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


# In[ ]:




