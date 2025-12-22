import numpy as np
# from datetime import datetime,timedelta
import pandas as pd
import time
import matplotlib.pyplot as plt
import tqdm

import joblib
import os

from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_absolute_error

def data_preparation(data, look_back = 2, forecast_horizon = 1 ):
    features = []
    targets = []
    num_samples = data.shape[0]

    for i in range(num_samples - look_back - forecast_horizon + 1):
        # The input features are the last `look_back` values of all series
        X_window = data.iloc[i : i + look_back].values

        # The target variables are the next `forecast_horizon` values of all series
        y_window = data.iloc[i + look_back : i + look_back + forecast_horizon].values

        # Flatten the windows to create a single row for the features and targets
        features.append(X_window.flatten())
        targets.append(y_window.flatten())

    X = np.array(features)
    y = np.array(targets)

    print(f"Shape of X (input features): {X.shape}")
    print(f"Shape of y (target variables): {y.shape}")

    X_scaler = StandardScaler()
    y_scaler = StandardScaler()

    X_scaled = X_scaler.fit_transform(X)
    y_scaled = y_scaler.fit_transform(y)
    
    return X_scaler, X_scaled, y_scaler, y_scaled

def pred_by_model(model_filename, X_scaled, y_scaler, y_scaled, forecast_horizon = 1):
    model = joblib.load(model_filename)
    y_pred_scaled = model.predict(X_scaled)

    # Inverse transform the predictions and the actual test data to their original scale
    y_pred_original = y_scaler.inverse_transform(y_pred_scaled)
    y_test_original = y_scaler.inverse_transform(y_scaled)
    
    y_test_reshaped = y_test_original.reshape(y_test_original.shape[0], forecast_horizon, -1)
    y_pred_reshaped = y_pred_original.reshape(y_pred_original.shape[0], forecast_horizon, -1)
    
    return y_test_reshaped, y_pred_reshaped