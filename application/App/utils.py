import joblib
import pandas as pd
import numpy as np
import requests


def get_metadata(X, csvpath):
    df_metadata = pd.read_csv(csvpath)
    df_values = pd.DataFrame(data={"Column": "", "Values": []})
    df_values['Values'] = df_values['Values'].astype('object')
    for i, col in enumerate(X.columns):
        if (X[col].dtype == "O") | (X[col].dtype == np.int64):
            df_values.at[i, 'Column'] = col
            try:
                test = pd.to_datetime(X[col], format='%Y')
                df_values.at[i, 'Values'] = df_metadata.loc[df_metadata["Column"]
                                                            == col, "Description"]
                df_values.at[i, 'Column_type'] = "numerical"
            except ValueError:
                df_values.at[i, 'Values'] = [*set(X[col])]
                df_values.at[i, 'Column_type'] = "categorical"
        else:
            df_values.at[i, 'Column'] = col
            df_values.at[i, 'Values'] = df_metadata.loc[df_metadata["Column"]
                                                        == col, "Description"]
            df_values.at[i, 'Column_type'] = "numerical"
    return df_metadata.merge(df_values, on=["Column"])


def query_property_ids_api(params, apikey):
    # &page=1&pagesize=100
    url_ids_filter = 'https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/id'
    headers = {'apikey': apikey}
    # params = {"postalcode":50010,"minBeds":1,"maxBeds":2,"pagesize":100}
    response_ids = requests.request(
        "GET", url_ids_filter, headers=headers, params=params)


def query_property_detail_from_ids_api(params, apikey):
    # &page=1&pagesize=100
    url_detail_filter = 'https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/detail'
    headers = {'apikey': apikey}
    # params = {"attomid":184713191,"pagesize":100}
    response_ids = requests.request(
        "GET", url_detail_filter, headers=headers, params=params)
