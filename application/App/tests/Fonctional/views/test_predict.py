from werkzeug.datastructures import MultiDict
import pandas as pd
import joblib
from App.utils import get_metadata
from os.path import exists


def test_metadata_file_exists():
    assert exists("features_e2.csv")


def test_metadata_file_format():
    df_metadata = pd.read_csv("features_e2.csv")
    for col in df_metadata.columns:
        assert col in ["Column", "Description"]
        assert df_metadata[col].dtype == "O"


def test_model_file_exists():
    assert exists("model_v1.joblib")


def test_X_train_file_exists():
    assert exists("X_train.joblib")


def test_columns_metadata_X_train_match():
    X_train = joblib.load(open('X_train.joblib', 'rb'))
    metadata = get_metadata(X_train, csvpath="features_e2.csv")
    for i in metadata.index:
        col_metadata = metadata["Column"][i]
        assert col_metadata in X_train.columns
    for col in X_train.columns:
        assert col in list(metadata["Column"])


def test_index_route_correct_template(test_client, captured_templates):
    response = test_client.get("/")
    assert response.status_code == 200
    title = "<title>Prédiction du prix de la maison</title>"
    assert title.encode() in response.data

    template, context = captured_templates[0]

    assert template.name == "index.html"
    assert "metadata" in context
    assert isinstance(context["metadata"], pd.DataFrame)


def test_index_route_param_insertion(test_client):
    response = test_client.get("/")
    df_metadata = pd.read_csv("features_e2.csv")
    columns = [*set(df_metadata["Column"])]
    descriptions = [*set(df_metadata["Description"])]
    for col, desc in zip(columns, descriptions):
        # Il faudra retirer cette ligne quand le modèle sera implémenté
        if col in df_metadata["Column"]:
            assert col.encode() in response.data
            assert desc.encode() in response.data


def test_post_index_route(test_client):
    response = test_client.post("/")
    assert response.status_code == 405


# def test_predict_route_correct_template(test_client, captured_templates):
#     response = test_client.get("/predict")
#     assert response.status_code == 200
#     title = "<title>Prédiction du prix de la maison</title>"
#     assert title.encode() in response.data

#     template, context = captured_templates[0]

#     assert template.name == "index.html"
#     assert "metadata" in context
#     assert isinstance(context["metadata"], pd.DataFrame)
#     assert "data" in context
#     assert isinstance(context["data"], int)


def test_predict_route_param_insertion(test_client):

    data = MultiDict([('totalarea', 2100), ('OverallQual', 7), ('TotalBsmtSF', 60000), ('Neighborhood', "OldTown"),
                      ('YearRemod__Add', 1900), ('BsmtFinSF1', 622), ('BsmtExposure', "Gd"), ('GarageArea', 550),
                      ('Fireplaces', 1), ('MasVnrArea', 120)])
    X_train = joblib.load(open('X_train.joblib', 'rb'))
    metadata = get_metadata(X_train, csvpath="features_e2.csv")
    response = test_client.post("/predict", metadata=metadata, data=data)
    assert response.status_code == 200
    title = "<title>Prédiction du prix de la maison</title>"
    assert title.encode() in response.data


# def test_index_template(test_client):
#     response = test_client.get("/")
#     df_metadata = pd.read_csv("features_e2.csv")
#     columns = [*set(df_metadata["Column"])]
#     descriptions = [*set(df_metadata["Description"])]
#     for col, desc in zip(columns,descriptions):
#         assert col.encode() in response.data
#         assert desc.encode() in response.data


# def test_predict_route(test_client):

#     data = MultiDict([('Year_Built', '1960'), ('Total_Bsmt_SF', '200'), ('1st_Flr_SF', '500'),
#                       ('Gr_Liv_Area', '1100'), ('Garage_Area', '100'), ('Overall_Qual', '6'),
#                       ('Full_Bath', '2'), ('Exter_Qual', 'TA'), ('Kitchen_Qual', 'Gd'), ('Neighborhood', 'NWAmes')])

#     response = test_client.post("/predict",data=data)
#     assert response.status_code == 200
#     title = "<title>Prédiction du prix de la maison</title>"
#     assert title.encode() in response.data
