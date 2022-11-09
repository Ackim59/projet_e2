import joblib
import pandas as pd
import numpy as np

def get_metadata(X,csvpath):
    df_metadata = pd.read_csv(csvpath)
    df_values = pd.DataFrame(data={"Column":"","Values":[]})
    df_values['Values'] = df_values['Values'].astype('object')
    for i, col in enumerate(X.columns):
        if col in df_metadata["Column"].values:
            if (X[col].dtype == "O") | (X[col].dtype == np.int64):
                df_values.at[i, 'Column'] = col
                try:
                    test = pd.to_datetime(X[col],format='%Y')
                    df_values.at[i, 'Values'] = df_metadata.loc[df_metadata["Column"] == col,"Description"]
                    df_values.at[i, 'Column_type'] = "numerical"
                except ValueError:
                    df_values.at[i, 'Values'] = [*set(X[col])]
                    df_values.at[i, 'Column_type'] = "categorical"
            else:
                df_values.at[i, 'Column'] = col
                df_values.at[i, 'Values'] = df_metadata.loc[df_metadata["Column"] == col,"Description"]
                df_values.at[i, 'Column_type'] = "numerical"
    return df_metadata.merge(df_values,on=["Column"])