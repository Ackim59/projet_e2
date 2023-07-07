from flask import render_template, request, Blueprint, flash
from flask_login import login_required,current_user
import pandas as pd
import joblib
import os
from App.forms import PredictionForm
from App.models import db, Prediction
# from App import load_user

pred = Blueprint("predict", __name__,
                 template_folder="templates", static_folder="static")

apikey = os.getenv("apikey")

def save_pred(X_pred: pd.DataFrame):
    prediction = Prediction(user_id=current_user.id,
                            VolumeBasement=X_pred["VolumeBasement"],
                            OverallQual=X_pred["OverallQual"],
                            AllBathGrd=X_pred["AllBathGrd"],
                            MSSubClass=X_pred["MSSubClass"],
                            Neighborhood=X_pred["Neighborhood"],
                            GarageArea=X_pred["GarageArea"],
                            BsmtFinSF1=X_pred["BsmtFinSF1"],
                            YearRemod__Add=X_pred["YearRemod__Add"],
                            KitchenQual=X_pred["KitchenQual"],
                            SaleCondition=X_pred["SaleCondition"],
                            prediction=X_pred["prediction"])
    db.session.add(prediction)
    db.session.commit()
    flash(f"Prediction added successfully!")

@pred.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictionForm()
    print(type(form))
    model = joblib.load(open('model.joblib', 'rb'))
    X_train = joblib.load(open('X_train.joblib', 'rb'))
    if form.validate_on_submit():
        X_pred = {}
        for col in X_train.columns:
            # if X_train[col].dtype == "O":
            X_pred[col] = form[col].data
            # else:
                # X_pred[col] = int(form[col].data)

        print("-------------------------------------------------------------")
        print(model.predict(pd.DataFrame(X_pred, index=[0])))
        pred = model.predict(pd.DataFrame(X_pred, index=[0]))
        X_pred["prediction"] = pred
        save_pred(X_pred)
        return render_template('predict.html', form=form, data=int(pred))

    return render_template('predict.html', form=form)


# @pred.route('/predict', methods=['GET', 'POST'])
# def predict():

#     model = joblib.load(open('model.joblib', 'rb'))
#     X_predict = {}
#     for var in ['Year_Built', 'Total_Bsmt_SF', '1st_Flr_SF', 'Gr_Liv_Area', 'Garage_Area', 'Overall_Qual', 'Full_Bath', 'Exter_Qual',
#                 'Kitchen_Qual', 'Neighborhood']:

#         if var in ['Exter_Qual', 'Kitchen_Qual', 'Neighborhood']:
#             X_predict[var] = request.form[var]
#         else:
#             X_predict[var] = int(request.form[var])

#     pred = model.predict(pd.DataFrame(X_predict, index=[0]))

#     return render_template('index.html', data=int(pred))
