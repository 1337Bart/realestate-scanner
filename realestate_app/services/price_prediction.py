import numpy as np
import pandas as pd
import os
import django

# from sklearn.linear_model import LinearRegression
from realestate_app.models import RealEstateListing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()


def get_listings():
    listings = RealEstateListing.objects.all().values(
        "district", "city", "voivodeship", "rooms", "area", "price"
    )

    df = pd.DataFrame(listings)

    print(df)


# def run_simple_linear_regression(listings=RealEstateListing.objects.all()):
#     X = np.array([listing.area for listing in listings]).reshape(-1, 1)
#     y = np.array([listing.price for listing in listings])

#     model = LinearRegression()
#     model.fit(X, y)

#     for listing in listings:
#         listing.predicted_price_simple = model.predict([[listing.area]])[0]
#         listing.save()


# def run_multifactor_linear_regression():
#     return None


# run_simple_linear_regression()
# run_multifactor_linear_regression()
