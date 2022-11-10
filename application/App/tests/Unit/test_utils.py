import joblib
import pandas as pd
from App.utils import get_metadata


def test_get_metadata():
    X_train = joblib.load(open('X_train.joblib', 'rb'))
    metadata = get_metadata(X_train, csvpath="features_e2.csv")
    assert isinstance(metadata, pd.DataFrame)
    assert len(metadata.columns) == 4
    for col in metadata.columns:
        assert col in ["Column", "Description", "Column_type", "Values"]
    for i in metadata.index:
        col = metadata["Column"][i]
        if metadata["Column_type"][i] == "categorical":
            assert type(metadata.loc[metadata["Column"]
                        == col, :]["Values"][i]) == list
        elif metadata["Column_type"][i] == "numerical":
            assert type(metadata.loc[metadata["Column"]
                        == col, :]["Values"][i][0]) == str
