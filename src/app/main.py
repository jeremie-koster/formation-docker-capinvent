import logging

from fastapi import FastAPI, Response
from .model import ModelHandler, PredictionReturned, InputName

logger = logging.getLogger(__name__)
app = FastAPI()

@app.on_event("startup")
async def init_worker():
    global model
    model = ModelHandler()
    return

@app.get("/")
def read_root():
    return "Model API"

@app.post("/prediction", response_model=PredictionReturned)
async def predict(data: InputName, response: Response):
    model = ModelHandler()
    try :
        prediction = model.predict(data.name)
    except FileNotFoundError:
            prediction = {"prediction": 'file not found error'}
    except Exception as e:
            prediction = {"prediction": str(e)}
    return PredictionReturned(prediction=prediction.get("prediction", ""), score=prediction.get("score", 0))

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}



