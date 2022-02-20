import mlflow
import pandas as pd
from efficientnet.tfkeras import EfficientNetB0


MLFLOW_TRACKING_URI = "http://mlflow:5000"

class TrainingService:
    def __init__(self):
        self.root_path = "/path_to_data"

    def load_data(self, dataset_name):
        df = pd.DataFrame()
        return df

    def train(self, dataset_name: str):
        if MLFLOW_TRACKING_URI:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        data = self.load_data(dataset_name)

        with mlflow.start_run(run_name="train"):
            mlflow.log_params(
                {
                    "no_param": "this is a fake training",
                }
            )
            model = EfficientNetB0(weights='imagenet')
            mlflow.keras.log_model(
                keras_model=model,
                artifact_path="image_classification_model",
                registered_model_name="image_classification_model",
            )
    
            metrics_dict = {
                "MAE": 0,
                "MSE": 0,
                "RMSE": 0,
                "MAPE": round(
                    0.0, 2
                ),
            }
            mlflow.log_metrics(metrics_dict)
            #mlflow.log_artifact(f"{self.root_path}/{dataset_name}_data.csv")
