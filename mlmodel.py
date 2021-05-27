import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error as mse

def compute_model(x,y):
    X_train, X_test, y_train, y_test = tts(X, y, random_state=0, test_size=1/3)
    regr = LinearRegression()

    regr.fit(X_train, y_train)

    y_pred = regr.predict(X_test)

    return y_pred, regr.intercept_, regr.coef_