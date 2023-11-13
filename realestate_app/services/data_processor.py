import numpy as np
from sklearn.linear_model import LinearRegression
from models import RealEstateListing


def run_simple_linear_regression():
    listings = RealEstateListing.objects.all()
    X = np.array([listing.area for listing in listings]).reshape(-1, 1)
    y = np.array([listing.price for listing in listings])

    model = LinearRegression()
    model.fit(X, y)

    for listing in listings:
        listing.predicted_price_simple = model.predict([[listing.area]])[0]
        listing.save()


def run_multifactor_linear_regression():
    return None


run_simple_linear_regression()
run_multifactor_linear_regression()
