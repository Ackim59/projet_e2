from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, EmailField, SelectField, SubmitField)
from wtforms.validators import InputRequired, Length, Email, NumberRange
import joblib

class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[InputRequired(), Length(max=100), Email()])
    password = PasswordField('Mot de passe',validators=[InputRequired(),Length(min=8,max=500)])
    submit = SubmitField("Login")

class SignUpForm(FlaskForm):
    email = EmailField('E-mail', validators=[InputRequired(), Length(max=100), Email()])
    password = PasswordField('Mot de passe',validators=[InputRequired(),Length(min=8,max=500)])
    confirm_password = PasswordField('Confirmer le mot de passe',validators=[InputRequired(),Length(min=8,max=500)])

class PredictionForm(FlaskForm):
    X_train = joblib.load(open('X_train.joblib', 'rb'))

    VolumeBasement = IntegerField('VolumeBasement',
                                       validators=[InputRequired(),
                                                   NumberRange(min=X_train["VolumeBasement"].min(),
                                                               max=X_train["VolumeBasement"].max())],
                                       default=0)
    OverallQual = SelectField('OverallQual',
                               choices=[(name, name) for name in sorted(X_train["OverallQual"].unique())],
                               validators=[InputRequired()])
    AllBathGrd = SelectField('AllBathGrd',
                              choices=[(name, name) for name in sorted(X_train["AllBathGrd"].unique())],
                              validators=[InputRequired()])
    MSSubClass = IntegerField('MSSubClass', validators=[InputRequired(),NumberRange(min=0)])
    Neighborhood = SelectField('Neighborhood',
                               choices=[(name, name) for name in sorted(X_train["Neighborhood"].unique())],
                               validators=[InputRequired()])
    GarageArea = IntegerField('GarageArea',
                                   validators=[InputRequired(),
                                               NumberRange(min=X_train["GarageArea"].min(),
                                                           max=X_train["GarageArea"].max())],
                                   default=0)
    BsmtFinSF1 = IntegerField('BsmtFinSF1',
                                   validators=[InputRequired(),
                                               NumberRange(min=X_train["BsmtFinSF1"].min(),
                                                           max=X_train["BsmtFinSF1"].max())],
                                   default=0)
    YearRemod__Add = IntegerField('YearRemodAdd',
                                       validators=[InputRequired(),
                                                   NumberRange(min=X_train["YearRemod__Add"].min(),
                                                               max=X_train["YearRemod__Add"].max())],
                                       default=1970)
    KitchenQual = SelectField('KitchenQual',
                               choices=[(name, name) for name in sorted(X_train["KitchenQual"].unique())],
                               validators=[InputRequired()])
    SaleCondition = SelectField('SaleCondition',
                                 choices=[(name, name) for name in sorted(X_train["SaleCondition"].unique())],
                                 validators=[InputRequired()])
    submit = SubmitField("Predict")