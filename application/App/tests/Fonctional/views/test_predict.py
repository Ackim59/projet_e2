from werkzeug.datastructures import MultiDict
from os.path import exists

def test_model_file_exists():
    assert exists("model.joblib")

def test_X_train_file_exists():
    assert exists("X_train.joblib")

def test_login_route_correct_template(test_client, captured_templates):
    response = test_client.get("/")
    assert response.status_code == 200
    title = "<title>Login</title>"
    assert title.encode() in response.data

    template, context = captured_templates[0]

    assert template.name == "login.html"
    assert "form" in context

    response = test_client.get("/login")
    title = "<title>Login</title>"
    assert title.encode() in response.data

    template, context = captured_templates[0]

    assert template.name == "login.html"
    assert "form" in context

def test_post_login_route(test_client):
    response = test_client.post("/")
    assert response.status_code == 200
    response = test_client.post("/login")
    assert response.status_code == 200

def test_signup_route_correct_template(test_client, captured_templates):
    response = test_client.get("/signup")
    assert response.status_code == 200
    title = "<title>SignUp</title>"
    assert title.encode() in response.data

    template, context = captured_templates[0]

    assert template.name == "signup.html"
    assert "form" in context

def test_post_signup_route(test_client):
    response = test_client.post("/signup")
    assert response.status_code == 200


def test_predict_route_correct_template(test_client, captured_templates,app):
    app.config["LOGIN_DISABLED"] = True
    response = test_client.get("/predict")
    assert response.status_code == 200
    title = "<title>Prédiction du prix d'une maison</title>"
    assert title.encode() in response.data

    template, context = captured_templates[0]

    assert template.name == "predict.html"
    assert "form" in context


def test_predict_route_param_insertion(test_client, app):
    app.config["LOGIN_DISABLED"] = True
    data = MultiDict([('VolumeBasement', 80000),
                      ('OverallQual', 7),
                      ('AllBathGrd', 2.5),
                      ('MSSubClass', 1000),
                      ('Neighborhood', "OldTown"),
                      ('GarageArea', 800),
                      ('BsmtFinSF1', 622),
                      ('YearRemod__Add', 1970),
                      ('KitchenQual', "Ex"),
                      ('SaleCondition', 'Normal')]
                      )
    response = test_client.post("/predict", data=data)
    assert response.status_code == 200
    title = "<title>Prédiction du prix d'une maison</title>"
    assert title.encode() in response.data
