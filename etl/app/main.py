from datetime import date
from typing import Final, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from app.data_preparation_service import DataPreparationService
from app.meteo_france_service import MeteoFranceService
from app.rte_france_service import RTEFranceService

GE_STATIC_ROOT: Final = "/great-expectations"

app = FastAPI()

meteo_france_service: Final = MeteoFranceService()
rte_france_service: Final = RTEFranceService()
data_preparation_service: Final = DataPreparationService()


@app.get("/")
def read_root():
    """GET the API documentation of all endpoints"""
    return RedirectResponse("/docs")



@app.get("/retrieve-raw-weather-data")
def retrieve_raw_weather_data(year: int, start_month: int, end_month: int, dataset_name: Optional[str] = "train"):
    """GET weather data based on parameters: Year, start_month, end_month and dataset name"""

    # Query validation
    if year < 1996:
        raise HTTPException(status_code=400, detail="Cannot query data before 1996")
    if start_month > end_month:
        raise HTTPException(status_code=400, detail="Bad parameter : start month > end month")
    today = date.today()
    if year > today.year or (year == today.year and end_month > today.month):
        raise HTTPException(status_code=400, detail="Cannot query data into the future")

    # retrieving and saving the data
    try:
        meteo_france_service.retrieve_raw_weather_data(year, start_month, end_month, dataset_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"response": "ok"}


@app.get("/retrieve-raw-rte-data")
def retrieve_raw_rte_data(year: int, start_month: int, end_month: int, dataset_name: Optional[str] = "train"):
    """GET rte france consumption data based on parameters: Year, start_month, end_month and dataset name"""
    # End_month is exclusive in RTE service (and we want the API to be inclusive)
    end_month += 1

    # Query validation
    if year < 2013:
        raise HTTPException(status_code=400, detail="Cannot query data before 2013")
    if start_month > end_month:
        raise HTTPException(status_code=400, detail="Bad parameter : start month > end month")
    if end_month - start_month > 6:
        raise HTTPException(status_code=400, detail="Cannot query more than 6 months of data")
    today = date.today()
    if year > today.year or (year == today.year and end_month > today.month):
        raise HTTPException(status_code=400, detail="Cannot query data into the future")

    # retrieving and saving the data
    try:
        rte_france_service.retrieve_raw_short_term_data(year, start_month, end_month, dataset_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"response": "ok"}


@app.get("/prepare-raw-weather-data")
def prepare_raw_weather_data(dataset_name: Optional[str] = "train"):
    data_preparation_service.prepare_raw_weather_data(dataset_name)
    return {"response": "ok"}


@app.get("/prepare-raw-rte-data")
def prepare_raw_rte_data(dataset_name: Optional[str] = "train"):
    data_preparation_service.prepare_raw_rte_data(dataset_name)
    return {"response": "ok"}


@app.get("/merge-curated-data")
def merge_curated_data(dataset_name: Optional[str] = "train"):
    data_preparation_service.merge_curated_data(dataset_name)
    return {"response": "ok"}


@app.get("/run-whole-pipeline")
def run_whole_pipeline(year: int, start_month: int, end_month: int, dataset_name: Optional[str] = "train"):
    # 1) retrieve raw data
    retrieve_raw_weather_data(year, start_month, end_month, dataset_name)
    retrieve_raw_rte_data(year, start_month, end_month, dataset_name)
    # 2) prepare data and store in curated
    prepare_raw_weather_data(dataset_name)
    prepare_raw_rte_data(dataset_name)
    # 3) merge data and store in refined : ready to train
    merge_curated_data(dataset_name)
    return {"response": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
