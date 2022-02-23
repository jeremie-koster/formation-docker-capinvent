
import os
import logging

import numpy as np
import pandas as pd
import mlflow
import json
from pydantic import BaseModel

MLFLOW_TRACKING_URI="http://mlflow:5000"
MODEL_NAME="iris_classification_model"
STAGE="Production"

logger = logging.getLogger(__name__)


class PredictionReturned(BaseModel):
    prediction: str
    score: float

class InputName(BaseModel):
    name: str

class ModelHandler:
    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model = mlflow.sklearn.load_model(model_uri=f"models:/{MODEL_NAME}/{STAGE}")
        return model
    
    def load_iris(self, name):
        path = os.path.join('/data/iris_examples', name)
        df_iris = pd.read_json(path)
        return df_iris

    def predict(self, iris_name):
        df_iris = self.load_iris(iris_name)
        predictions = self.model.predict(df_iris)
        return predictions
