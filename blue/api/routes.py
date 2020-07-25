from flask import Blueprint,jsonify, request
from flask_restful import Api,Resource
import pandas as pd
from werkzeug.utils import secure_filename
import sys 
import os
import json
import h5py
from tensorflow.keras.models import load_model
import requests
from PIL import Image
import urllib
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import bcrypt


dirname = os.path.dirname(os.path.abspath(__file__))
dirname_list = dirname.split("/")[:-1]
dirname = "/".join(dirname_list)
print(dirname)
path = dirname + "/api"
print(path)
sys.path.append(path)



path02 = dirname + "/api/Models"

sys.path.append(path02)

mod = Blueprint('api',__name__)
api = Api(mod)

from data_upload import Upload_Data
from TrainingModel import Model_Train
from model_prediction import Prediction_Func


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///record.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)



class Users (db.Model) :
    id = db.Column(db.Integer , primary_key=True)
    user_name = db.Column(db.String(40))
    password = db.Column(db.String(20))
    user_email=db.Column(db.String(40))






class Create_Project(Resource):
    def post(self):
        try:
            proj_path = dirname + "/Projects"

            postedData=request.get_json()
        
            proj_name=postedData['project_name']
            first_category=postedData['category_one']
            second_category=postedData['category_two']

            name_and_path = proj_path + "/" + proj_name
            path01 = name_and_path + "/" + first_category
            path02 = name_and_path + "/" + second_category
        
            if not os.path.exists(name_and_path):
            
                
                if not os.path.exists(path01):
                    
                    if not os.path.exists(path02):
                        os.mkdir(name_and_path)
                        print("created project : ", proj_name)
                        os.mkdir(path01)
                        os.mkdir(path02)
                        print("created categories : ", first_category,second_category)
                
                        ret={"status":200,"msg":"Successfully created project"}         
                        return jsonify(ret)

                else:
                    print(proj_name, " folder already exists.")
                    ret={"status":401,"msg":"category with this name already exist"}         
                    
                    return jsonify(ret)
        
                ret={"status":200,"msg":"Successfully created project"}         
                return jsonify(ret)

            else:
                print(proj_name, " folder already exists.")
                ret={"status":401,"msg":"Project with this name already exist"}         
                
                return jsonify(ret)
  
        except Exception as e:
            ret={"status":401,"msg":"Cannot create this project","Problem":e}         
            return jsonify(ret)


class Uploading_Data(Resource):
    def post(self):
        try:
            proj_path = dirname + "/Projects"

            postedData=request.get_json()
        
            proj_name=postedData['project_name']
            category=postedData['category']
            urls=postedData['urls']
        

            project_path = proj_path + "/" + proj_name
            cat_path = project_path + "/" + category

            if os.path.exists(project_path):
                if os.path.exists(cat_path):

                    for url in urls:
                        retJson = Upload_Data(cat_path,url)
                    return jsonify({"status":200,"msg":retJson})

                else:
                    retJson = {"status":404,"msg":"Category with this name doesn't exist"}
                    return jsonify(retJson)

            else:
                retJson = {"status":404,"msg":"Project with this name doesn't exist"}
                return jsonify(retJson)

        except Exception as e:
            ret={"status":401,"msg":"Cannot Upload","Problem":e}         
            return jsonify(ret)
        


class Train_Models(Resource):
    def post(self):
        try:

            proj_path = dirname + "/Projects"
            postedData=request.get_json()
        
            proj_name=postedData['project_name']
            cat1 =postedData['category1']
            cat2 =postedData['category2']

            categories=[cat1,cat2]

            DIR_NAME = proj_path + "/" + proj_name

            retJson = Model_Train(DIR_NAME,categories)


            return jsonify(retJson)
    
        except Exception as e:
            ret={"status":401,"msg":"Error in training model","Problem":e}         
            return jsonify(ret)


class Prediction(Resource):
    def post(self):
        try:

            postedData=request.get_json()
            url=postedData['url']
            proj_name=postedData['project_name']
            cat1 =postedData['category1']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
            cat2 =postedData['category2']

            proj_path = dirname + "/Projects"
            DIR_NAME = proj_path + "/" + proj_name

            model_path = DIR_NAME + "/" + "model.h5"

            model = load_model(model_path,compile=False)

            

            categories=[cat1,cat2]

            retJson = Prediction_Func(url,categories,model)
            
            return jsonify(retJson)
        
        except Exception as e:
            ret={"status":401,"msg":"Cannot use this image for prediction","Problem":e}         
            return jsonify(ret)


api.add_resource(Create_Project, "/create_project")
api.add_resource(Uploading_Data, "/upload_data")
api.add_resource(Train_Models, "/train")
api.add_resource(Prediction, "/predict")
