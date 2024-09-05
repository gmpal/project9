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
            # print(train,test)
            inputs.append(y[y.columns[~y.columns.isin(excluded_columns)]].loc[train].to_numpy())
            outputs.append(y.loc[test, ["Total Load Interpolated"]].to_numpy().flatten())
            # print(y.loc[test, ["Total Load Interpolated"]].to_numpy().flatten())
            # if i == 12:
            #     break
    return inputs, outputs


def get_train_test(window_length=12, horizon=4, total_size = int(24*4*365*2.5), shift=4,
                  excluded_columns = ['Total Load', 'Difference with previous load', 'Datetime', 'Resolution code', 'Total Load Persistence', 'Most recent forecast', 
                                      'Most recent P10', 'Most recent P90', 'Day-ahead 6PM forecast', 'Day-ahead 6PM P10', 'Day-ahead 6PM P90', 'Week-ahead forecast', 
                                      'Total Load Interpolated Persistence']):
    last_train_sample = 335428
    last_test_sample = 338403
    train = pd.read_csv("Processed_data.csv", index_col=0)
    train = train[len(train)-total_size:last_train_sample+1].reset_index(drop=True)
    test = pd.read_csv("Processed_data.csv", index_col=0)
    test = test[last_train_sample-window_length:last_test_sample+1+horizon-4]
    # print(test.index[:10], test.index[-10:])
    # print(last_train_sample-window_length)
    test = test.reset_index(drop=True)

    
    fh = ForecastingHorizon(list(range(1, horizon+1)))
    cv = SlidingWindowSplitter(window_length=window_length, fh=fh)


    # n_splits_train = cv.get_n_splits(train)
    # n_splits_test = cv.get_n_splits(test)
    
    X_train, Y_train = get_windows(train, cv, shift, excluded_columns)
    X_test, Y_test = get_windows(test, cv, shift, excluded_columns)
    return np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)
 

def get_train_test_new(window_length=12, horizon=4, total_size = int(24*4*365*2.5), shift=4,
                  excluded_columns = ['Total Load', 'Difference with previous load', 'Datetime', 'Resolution code', 'Total Load Persistence', 'Most recent forecast', 
                                      'Most recent P10', 'Most recent P90', 'Day-ahead 6PM forecast', 'Day-ahead 6PM P10', 'Day-ahead 6PM P90', 'Week-ahead forecast', 
                                      'Total Load Interpolated Persistence']):

    last_train_sample = 335428
    last_test_sample = 338403

    max_window_length = 80

    train = pd.read_csv("Processed_data.csv", index_col=0)
    train = train[len(train)-total_size:last_train_sample+1].reset_index(drop=True)
    test = pd.read_csv("Processed_data.csv", index_col=0)
    test = test[last_train_sample-max_window_length:last_test_sample+1+horizon-4].reset_index(drop=True)

    n_splits_train = (train.shape[0] - 1 - max_window_length)//4 - 1
    n_splits_test = (test.shape[0] - 1 - max_window_length)//4

    # Pre-allocate arrays
    base_x_train = np.zeros((n_splits_train + 1, window_length))
    base_y_train = np.zeros((n_splits_train + 1, horizon))

    # Pre-allocate arrays
    base_x_test = np.zeros((n_splits_test + 1, window_length))
    base_y_test = np.zeros((n_splits_test + 1, horizon))

    # Initialize base_x and base_y with initial values
    base_x_train[0] = np.arange(max_window_length - window_length, max_window_length)
    base_y_train[0] = np.arange(max_window_length, max_window_length + horizon)

    base_x_test[0] = np.arange(max_window_length - window_length, max_window_length)
    base_y_test[0] = np.arange(max_window_length, max_window_length + horizon)


    inputs_train = []
    inputs_train.append(train.iloc[base_x_train[0]][train.columns[~train.columns.isin(excluded_columns)]].to_numpy().flatten(order='F'))
    for i in tqdm(range(1, n_splits_train + 1 )):
        shifted_base_x = base_x_train[i-1] + shift
        base_x_train[i] = shifted_base_x

        inputs_train.append(train.iloc[base_x_train[i]][train.columns[~train.columns.isin(excluded_columns)]].to_numpy().flatten(order='F'))

        shifted_base_y = base_y_train[i-1] + shift
        base_y_train[i] = shifted_base_y

    inputs_test = []
    inputs_test.append(test.iloc[base_x_test[0]][test.columns[~test.columns.isin(excluded_columns)]].to_numpy().flatten(order='F'))
    for i in tqdm(range(1, n_splits_test + 1)):
        shifted_base_x = base_x_test[i-1] + shift
        base_x_test[i] = shifted_base_x

        inputs_test.append(test.iloc[base_x_test[i]][test.columns[~test.columns.isin(excluded_columns)]].to_numpy().flatten(order='F'))

        shifted_base_y = base_y_test[i-1] + shift
        base_y_test[i] = shifted_base_y

    
    Y_test = test.iloc[base_y_test.flatten()]['Total Load Interpolated'].to_numpy().reshape(-1,horizon)
    Y_train = train.iloc[base_y_train.flatten()]['Total Load Interpolated'].to_numpy().reshape(-1,horizon)

    return np.array(inputs_train), np.array(Y_train), np.array(inputs_test), np.array(Y_test)
 
def get_columns():
    train = pd.read_csv("Processed_data.csv")
    train = train.drop([train.columns[0], train.columns[1]], axis=1)
    return train.columns.to_list()