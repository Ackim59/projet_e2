from werkzeug.security import generate_password_hash
from App.models import User, Prediction, db

def test_user_model(app):
    with app.app_context():
        password = "essaienmodetest"
        email = "essai@gmail.com"
        hashed_password = generate_password_hash(password)
        user = User(email=email, _hashed_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        assert user.email == email

def test_prediction_model(app):
    with app.app_context():
        user_id = 1
        VolumeBasement = 80000
        OverallQual = 7
        AllBathGrd = 2.5
        MSSubClass = 1000
        Neighborhood = 'OldTown'
        GarageArea = 800
        BsmtFinSF1 = 622
        YearRemod__Add = 1970
        KitchenQual = 'Ex'
        SaleCondition = 'Normal'
        prediction = 120000
        pred = Prediction(
                user_id = user_id,
                VolumeBasement = VolumeBasement,
                OverallQual = OverallQual,
                AllBathGrd = AllBathGrd,
                MSSubClass = MSSubClass,
                Neighborhood = Neighborhood,
                GarageArea = GarageArea,
                BsmtFinSF1 = BsmtFinSF1,
                YearRemod__Add = YearRemod__Add,
                KitchenQual = KitchenQual,
                SaleCondition = SaleCondition,
                prediction = prediction
        )
        

        db.session.add(pred)
        db.session.commit()
        pred = Prediction.query.filter_by(     
                            user_id = user_id,
                            VolumeBasement = VolumeBasement,
                            OverallQual = OverallQual,
                            AllBathGrd = AllBathGrd,
                            Neighborhood = Neighborhood,
                            MSSubClass = MSSubClass,
                            GarageArea = GarageArea,
                            BsmtFinSF1 = BsmtFinSF1,
                            YearRemod__Add = YearRemod__Add,
                            KitchenQual = KitchenQual,
                            SaleCondition = SaleCondition,
                            prediction = prediction
                            ).first()
        assert pred.user_id == user_id
        assert pred.VolumeBasement == VolumeBasement
        assert pred.OverallQual == OverallQual
        assert pred.AllBathGrd == AllBathGrd
        assert pred.Neighborhood == Neighborhood
        assert pred.MSSubClass == MSSubClass
        assert pred.GarageArea == GarageArea
        assert pred.BsmtFinSF1 == BsmtFinSF1
        assert pred.YearRemod__Add == YearRemod__Add
        assert pred.KitchenQual == KitchenQual
        assert pred.SaleCondition == SaleCondition
        assert pred.prediction == prediction
