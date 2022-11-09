from flask import Flask, render_template, request, Blueprint
import numpy as np
import pandas as pd
import joblib
from App.utils import get_metadata
pred = Blueprint("predict", __name__, template_folder="templates", static_folder="static")


@pred.route('/')
def index():
    X_train = joblib.load(open('X_train.joblib', 'rb'))
    metadata = get_metadata(X_train,csvpath="features_e2.csv")
    # for val in df_metadata.index:
    #     print(df_metadata.loc[val,:]["Values"])
    return render_template('index.html',metadata=metadata)


@pred.route('/predict', methods=['GET', 'POST'])
def predict():
    
    model = joblib.load(open('model_v1.joblib', 'rb'))
    X_train = joblib.load(open('X_train.joblib', 'rb'))
    metadata = get_metadata(X_train,csvpath="features_e2.csv")
    X_predict = {}

    for col in X_train.columns:
        if X_train[col].dtype == "O":
            X_predict[col]= request.form[col]
        else:
            X_predict[col]= int(request.form[col])

    pred = model.predict(pd.DataFrame(X_predict, index=[0]))
    return render_template('index.html', metadate=metadata, data=int(pred))

# @pred.route('/predict', methods=['GET', 'POST'])
# def predict():
    
#     model = joblib.load(open('model.joblib', 'rb'))
#     X_predict = {}
#     for var in ['Year_Built', 'Total_Bsmt_SF', '1st_Flr_SF', 'Gr_Liv_Area','Garage_Area', 'Overall_Qual', 'Full_Bath', 'Exter_Qual',
#               'Kitchen_Qual', 'Neighborhood']:

#         if var in ['Exter_Qual','Kitchen_Qual', 'Neighborhood']:
#             X_predict[var]= request.form[var]
#         else:
#             X_predict[var]= int(request.form[var])

#     pred = model.predict(pd.DataFrame(X_predict, index=[0]))

#     return render_template('index.html', data=int(pred))