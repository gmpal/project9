import numpy as np
import pandas as pd
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import SlidingWindowSplitter
from tqdm.auto import tqdm

def get_windows(y, cv, shift, excluded_columns):
    inputs = []
    outputs = []
    for i, (train, test) in tqdm(enumerate(cv.split(y["Total Load Interpolated"]))):
        if not (i%shift):
            inputs.append(y[y.columns[~y.columns.isin(excluded_columns)]].loc[train].to_numpy().flatten())
            outputs.append(y.loc[test, ["Total Load Interpolated"]].to_numpy().flatten())
    return inputs, outputs

def get_train_test(window_length=12, horizon=4, total_size = int(24*4*365*2.5),
                  excluded_columns = ['Total Load', 'Difference with previous load', 'Datetime', 'Resolution code', 'Total Load Persistence', 'Most recent forecast', 
                                      'Most recent P10', 'Most recent P90', 'Day-ahead 6PM forecast', 'Day-ahead 6PM P10', 'Day-ahead 6PM P90', 'Week-ahead forecast', 
                                      'Total Load Interpolated Persistence']):
    last_train_sample = 335428
    last_test_sample = 338403
    
    train = pd.read_csv("Processed_data.csv")
    train = train[len(train)-total_size:last_train_sample+1].reset_index()
    train = train.drop([train.columns[0], train.columns[1]], axis=1)
    
    test = pd.read_csv("Processed_data.csv")
    test = test[last_train_sample-window_length:last_test_sample+1+horizon-4].reset_index()
    test = test.drop([test.columns[0], test.columns[1]], axis=1)
    
    shift = 4
    fh = ForecastingHorizon(list(range(1, horizon+1)))
    cv = SlidingWindowSplitter(window_length=window_length, fh=fh)
    n_splits_train = cv.get_n_splits(train)
    n_splits_test = cv.get_n_splits(test)
    
    X_train, Y_train = get_windows(train, cv, shift, excluded_columns)
    X_test, Y_test = get_windows(test, cv, shift, excluded_columns)
    return np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)

def get_columns():
    train = pd.read_csv("Processed_data.csv")
    train = train.drop([train.columns[0], train.columns[1]], axis=1)
    return train.columns.to_list()