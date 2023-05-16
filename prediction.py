# -*- coding: utf-8 -*-
"""
Created on Mon May  1 18:07:51 2023

@author: Zied
"""
### import library 
from detoxify import Detoxify
import json
import pandas as pd
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import requests
from wtforms.validators import InputRequired

#set directory 
project_directory="./"
output_directory=project_directory+"output_data/"
input_directory=project_directory+"input_data/"

#import model that will be used for prediction
model = Detoxify('unbiased', device='cpu')

#this function for download json fil from url and saved it on input_directory
def import_json():  
    url = "https://dummyjson.com/comments" 
    r = requests.get(url)
    with open(input_directory+"data.json",'wb') as f:
        f.write(r.content)

import_json()

# flask configuration
app = Flask(__name__, template_folder=project_directory+"templates/")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = input_directory

# this function is for prediction, it only need data from a json file 
# prediction results and data (comment, id, user, ...) are saved on csv file on output_directory 
# no preproccessing for comment are need because it is done by tekonizer in prediction function proposed by Detoxify
def predict (data) :
    #extract comments from json
    comment= [data["comments"][i]["body"] for i in range (0, len(data["comments"]))]
    
    prediction=model.predict(comment)
    pred=pd.DataFrame.from_dict(prediction)
     
    comment_id = [data["comments"][i]["id"] for i in range (0, len(data["comments"]))]
    post_id    = [data["comments"][i]["postId"] for i in range (0, len(data["comments"]))]
    user_id    = [data["comments"][i]["user"]["id"] for i in range (0, len(data["comments"]))]
    comment    = [data["comments"][i]["body"] for i in range (0, len(data["comments"]))]
    
    df=pd.DataFrame(list(zip(comment_id, post_id  ,user_id ,comment)),  
                    columns=["comment_id", "post_id", "user_id", "comment" ])
    
    result=pd.concat([df,pred], axis=1)
    result.to_csv(output_directory+"résultat.csv", index=False)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload file and predict")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename("temp_"+file.filename))) # Then save the file
        with open(os.path.join(input_directory,"temp_"+file.filename), "r") as f:
             data = json.load(f)
        predict(data)
        return "result has been uploaded in "+output_directory
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
    
