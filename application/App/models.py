import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = sa.Column(sa.Integer,primary_key=True)
    email = sa.Column(sa.String(100), nullable=False, unique=True)
    _hashed_password = sa.Column(sa.String(500))
    predictions = db.relationship('Prediction', backref='user')

    @hybrid_property
    def hashed_password(self):
        raise AttributeError("password is not a readable property!")
    
    @hashed_password.setter
    def hashed_password(self, password):
        self.hashed_password =  generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self._hashed_password, password)

    def __repr__(self):
        return f"<User {self.email}>"
    
class Prediction(db.Model):
    __tablename__ = "prediction"
    id = sa.Column(sa.Integer,primary_key=True)
    user_id = sa.Column(sa.Integer,sa.ForeignKey('user.id'))
    VolumeBasement = sa.Column(sa.Integer)
    OverallQual = sa.Column(sa.Integer)
    AllBathGrd = sa.Column(sa.Float)
    MSSubClass = sa.Column(sa.Integer)
    Neighborhood = sa.Column(sa.String)
    GarageArea = sa.Column(sa.Integer)
    BsmtFinSF1 = sa.Column(sa.Integer)
    YearRemod__Add = sa.Column(sa.Integer)
    KitchenQual = sa.Column(sa.Integer)
    SaleCondition = sa.Column(sa.String)
    prediction = sa.Column(sa.Float)
