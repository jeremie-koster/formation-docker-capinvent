
import os
import logging

import numpy as np
import mlflow
from skimage.io import imread
from pydantic import BaseModel
from efficientnet.tfkeras import EfficientNetB0
from efficientnet.tfkeras import center_crop_and_resize, preprocess_input
from tensorflow.keras.applications.imagenet_utils import decode_predictions

MLFLOW_TRACKING_URI="http://mlflow:5000"
MODEL_NAME="image_classification_model"
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
        self.target_size = 224

    def load_model(self):
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        model = mlflow.pyfunc.load_model(model_uri=f"models:/{MODEL_NAME}/{STAGE}")
        return model
    
    def load_img(self, name):
        path = os.path.join('/image_examples', name)
        if os.path.isfile(path):
            array_img = imread(path)
            if len(array_img.shape) == 3 and array_img.shape[2]==4:
                array_img= array_img[:,:,:3]
        else :
            logger.error("file not found")
            array_img = np.zeros((100,100, 3))
        return array_img

    def _preprocess(self, img):
        x = center_crop_and_resize(img, image_size=self.target_size)
        x = preprocess_input(x)
        x = np.expand_dims(x, 0)
        return x

    def _postProcess(self, predictions):
        predictions = decode_predictions(predictions)
        return {"prediction": predictions[0][0][1], "score": predictions[0][0][2]}

    def predict(self, img_name):
        img = self.load_img(img_name)
        resized_img = self._preprocess(img)
        predictions = self.model.predict(resized_img)
        prediction = self._postProcess(predictions)
        return prediction
