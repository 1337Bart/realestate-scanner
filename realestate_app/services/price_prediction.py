import numpy as np
import pandas as pd
import os
import django
import logging

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from realestate_app.models import RealEstateListing
from realestate_app.models import PricePrediction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

from sklearn.ensemble import RandomForestRegressor


from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


def calculate_predictions():
    listings = RealEstateListing.objects.all()
    y = np.array([listing.price for listing in listings])

    # Prepare data for simple linear regression
    X_simple = np.array([listing.area for listing in listings]).reshape(-1, 1)

    # Train simple linear regression model
    model_simple = LinearRegression()
    model_simple.fit(X_simple, y)

    # Prepare data for multiple linear regression and Random Forest regression
    X_multiple = []
    for listing in listings:
        row = [
            listing.rooms,
            listing.area,
            listing.district,
            listing.city,
            listing.voivodeship,
        ]
        X_multiple.append(row)

    df_train = pd.DataFrame(
        X_multiple, columns=["rooms", "area", "district", "city", "voivodeship"]
    )
    df_train = pd.get_dummies(df_train, columns=["district", "city", "voivodeship"])

    # Train multiple linear regression model
    model_multiple = LinearRegression()
    model_multiple.fit(df_train, y)

    # Train Random Forest regression model
    model_rf = RandomForestRegressor(n_estimators=100)
    model_rf.fit(df_train, y)

    for listing in listings:
        # Predict using simple linear regression
        predicted_price_simple = model_simple.predict([[listing.area]])[0]

        # Prepare data for multiple
        input_data = pd.DataFrame(
            [
                {
                    "rooms": listing.rooms,
                    "area": listing.area,
                    "district": listing.district,
                    "city": listing.city,
                    "voivodeship": listing.voivodeship,
                }
            ]
        )
        input_data = pd.get_dummies(
            input_data, columns=["district", "city", "voivodeship"]
        )
        input_data = input_data.reindex(columns=df_train.columns, fill_value=0)

        # Predict using multiple linear regression
        predicted_price_multiple = model_multiple.predict(input_data)[0]

        # Predict using Random Forest regression
        predicted_price_rf = model_rf.predict(input_data)[0]

        # Post-process predictions to ensure non-negativity
        predicted_price_simple = max(predicted_price_simple, 0)
        predicted_price_multiple = max(predicted_price_multiple, 0)
        predicted_price_rf = max(predicted_price_rf, 0)

        # Save predictions
        PricePrediction.objects.update_or_create(
            listing=listing,
            defaults={
                "simple_linear_regression_predicted_price": predicted_price_simple,
                "multiple_linear_regression_predicted_price": predicted_price_multiple,
                "random_forest_predicted_price": predicted_price_rf,
            },
        )
