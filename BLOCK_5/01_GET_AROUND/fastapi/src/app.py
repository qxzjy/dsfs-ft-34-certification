import pandas as pd
import mlflow
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile

description = """
This API provide endpoints allowing to navigate through the pricing dataset and predict daily rental price based on features

## EDA

* `/preview` To be able to preview a few rows of the dataset
* `/unique-values` To be able to get unique values of a given column in the dataset

## Data operations

* `/groupby` To be able to group by a given column and chose an aggregation metric
* `/filterby` To be able to filter by one or several, categories within your dataset

## Machine Learning

* `/predict` To predict daily rental price based on features, on one observation
* `/batch-predict` To predict daily rental price based on features, on a batch of observation

Check out documentation below 👇 for more information on each endpoint.
"""

tags_metadata = [
    {
        "name": "EDA",
        "description": "Endpoints allowing to make basic Exploratory Data Analysis (EDA)"
    },
    {
        "name": "Data operations",
        "description": "Endpoints allowing to make operations on Data (groupBy, filterBy)"
    },
    {
        "name": "Machine-Learning",
        "description": "Endpoints that uses our Machine Learning model for pricing estimation",
    }
]

app = FastAPI(
    title="Getaround pricing API",
    description=description,
    version="0.1",
    contact={
        "name": "Maxime RENAULT",
        "url": "https://github.com/qxzjy/",
    },
    openapi_tags=tags_metadata
)

class GroupBy(BaseModel):
    column: str
    aggregation_metric: Literal["sum", "mean", "max", "min", "median", "count"]

class FilterBy(BaseModel):
    column: str
    category: List[str]

class PredictionFeatures(BaseModel):
    model_key: str
    mileage: Union[int, float]
    engine_power: Union[int, float]
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car : bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.get("/preview", tags=["EDA"])
async def preview_dataset(rows: int=5):
    """
    Get a dataset preview.
    
    * `rows` : The number of rows you want to preview (default value `5`)
    """

    dataset = pd.read_csv(
        "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv",
        index_col=0
    )

    return dataset.head(rows).to_json()


@app.get("/unique-values", tags=["EDA"])
async def unique_values(column: str):
    """
    Get unique values from a column.

    * `column` : The column you want to retrieve unique values from
    """

    dataset = pd.read_csv(
        "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv",
        index_col=0
    )
    
    return pd.Series(dataset[column].unique()).to_json()


@app.post("/group_by", tags=["Data operations"])
async def group_by(group_by: GroupBy):
    """
    Get a dataset grouped by one or several columns.

    * `column` : The column you want to grouped by
    * `aggregation_metric` : Aggregation metric to grouped by, within `sum`, `mean`, `max`, `min`, `median`, `count`
    """
    
    dataset = pd.read_csv(
        "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv",
        index_col=0
    )

    aggregation_function = getattr(pd.core.groupby.generic.DataFrameGroupBy, group_by.aggregation_metric)

    return aggregation_function(dataset.groupby(group_by.column)).to_json()


@app.post("/filter_by", tags=["Data operations"])
async def filter_by(filter_by: FilterBy):
    """
    Get a dataset filtered by one or several categories on one column.
    
    * `column` : The column you want to filtered by
    * `category` : Categories (at least one) to filtered by, within possible value for the column
    """

    dataset = pd.read_csv(
        "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv",
        index_col=0
    )

    return dataset[dataset[filter_by.column].isin(filter_by.category)].to_json()

@app.post("/predict", tags=["Machine-Learning"])
async def predict(predictionFeatures: PredictionFeatures):
    """
    Prediction for one observation. Endpoint will return a dictionnary like this:

    ```
    {'prediction': PREDICTION_VALUE}
    ```

    You need to give this endpoint all columns values as dictionnary, or form data.
    """
    # Read data
    # df = pd.DataFrame(dict(predictionFeatures), index=[0])
    df = pd.DataFrame([predictionFeatures.dict()])
    # Log model from mlflow
    logged_model = "runs:/db53a9e5d72348d8b6b8d595b06ba841/get-around-princing"

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    # prediction = loaded_model.predict(df)
    prediction = loaded_model.predict(pd.DataFrame(df))

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response


@app.post("/batch-predict", tags=["Machine-Learning"])
async def batch_predict(file: UploadFile = File(...)):
    """
    Make prediction on a batch of observation. This endpoint accepts only **csv files** containing
    all the trained columns WITHOUT the target variable.
    """
    # Read file
    df = pd.read_csv(file.file)

    # Log model from mlflow
    logged_model = "runs:/db53a9e5d72348d8b6b8d595b06ba841/get-around-princing"

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    
    predictions = loaded_model.predict(pd.DataFrame(df))

    return predictions.tolist()