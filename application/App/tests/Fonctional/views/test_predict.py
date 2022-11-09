from werkzeug.datastructures import MultiDict
import pandas as pd

def test_index_route_correct_template(test_client, captured_templates):
    response = test_client.get("/")
    assert response.status_code == 200
    title = "<title>Prédiction du prix de la maison</title>"
    assert title.encode() in response.data

    template, context = captured_templates[0]

    assert template.name == "index.html"
    assert "metadata" in context
    assert isinstance(context["metadata"],pd.DataFrame)


def test_index_route_param_insertion(test_client):
    response = test_client.get("/")
    df_metadata = pd.read_csv("features_e2.csv")
    columns = [*set(df_metadata["Column"])]
    descriptions = [*set(df_metadata["Description"])]
    for col, desc in zip(columns,descriptions):
        if col in df_metadata["Column"]:
            assert col.encode() in response.data
            assert desc.encode() in response.data

def test_post_index_route(test_client):
    response = test_client.post("/")
    assert response.status_code == 405

# def test_predict_route(test_client):

#     data = MultiDict([('totalarea',2100), ('OverallQual',7), ('TotalBsmtSF',60000), ('Neighborhood',"OldTown"),
#        ('YearRemod__Add',1900), ('BsmtFinSF1',622), ('BsmtExposure',"Gd"), ('GarageArea',550),
#        ('Fireplaces',1), ('MasVnrArea',120)])
#     metadata = pd.read_csv("features_e2.csv")
#     response = test_client.post("/predict",data=data)
#     assert response.status_code == 200
#     title = "<title>Prédiction du prix de la maison</title>"
#     assert title.encode() in response.data


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