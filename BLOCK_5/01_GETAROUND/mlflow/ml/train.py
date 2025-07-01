import pandas as pd
import time
import mlflow
import os
from xgboost import XGBRegressor
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


if __name__ == "__main__":

    ### MLFLOW Experiment setup
    experiment_name = "get-around-pricing"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    client = mlflow.tracking.MlflowClient(tracking_uri=os.environ["MLFLOW_TRACKING_URI"])
    run = client.create_run(experiment.experiment_id)

    print("training model...")

    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False)  # We won't log models right away

    # Import dataset
    df_prices = pd.read_csv(
        "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv",
        index_col=0
    )

    # X, y split
    target_variable = "rental_price_per_day"
    X = df_prices.drop(target_variable, axis = 1)
    y = df_prices[target_variable]

    # Preprocessing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 3)

    numerical_features = X.select_dtypes(include="int64").columns
    categorical_features = X.select_dtypes(exclude="int64").columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(drop="first"), categorical_features)
        ]
    )
    
    # Pipeline
    model = Pipeline(
        steps=[
            ("Preprocessing", preprocessor),
            (
                "Regressor",
                XGBRegressor(
                    learning_rate=0.1, max_depth=7, subsample=0.7
                ),
            ),
        ],
        verbose=True
    )

    # Log experiment to MLFlow
    with mlflow.start_run(run_id=run.info.run_id) as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_train)

        # Log model seperately to have more flexibility on setup
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="get-around-princing",
            registered_model_name="get-around-princing_XGBR",
            signature=infer_signature(X_train, predictions),
        )

    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")
