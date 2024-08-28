import pandas as pd
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import MinMaxScaler
from copy import deepcopy
import joblib


class TRAILDataset(Dataset):

    def __init__(
        self, data: pd.DataFrame, input_size: int, columns_input: list[str], column_to_predict: str, column_to_normalize: list[str], predict_scaler=None, scaler=None, normalize_predict_row=True
    ):
        """
        Args:
            data: A panda dataframe
            input_size : Number of consecutive rows to load in each sample.
            columns_input : List of column to return in each sample. These columns are the one used by the model
            column_to_predict: Column that contain the data the model will predict. This column will be sent as ground truth
            column_to_normalize: List of column to apply a min max normalization to.
            predict_scaler: sklearn scaler for the prediction. If None the scaler will be initialized automatically
            scaler: sklearn scaler for the columns_input. If None the scaler will be initialized automatically
            normalize_predict_row: If True the predict row will be normalized
        """
        self.data = data
        self.input_size = input_size
        self.columns_input = columns_input
        self.column_to_predict = deepcopy(column_to_predict)
        self.column_to_normalize = deepcopy(column_to_normalize)

        if self.column_to_predict in self.column_to_normalize:
            self.column_to_normalize = self.column_to_normalize.remove(column_to_predict)

        # Normalization
        self.scaler = scaler
        if self.column_to_normalize is not None:
            rows_to_scale = self.data[self.column_to_normalize]
            if self.scaler is None:
                scaler = MinMaxScaler()
                scaler = scaler.fit(rows_to_scale)
            self.scaler = scaler
            scaled_rows = self.scaler.transform(rows_to_scale)
            self.data[self.column_to_normalize] = scaled_rows

        row_to_scale = np.array(self.data[self.column_to_predict])
        if (predict_scaler is None) and normalize_predict_row:
            predict_scaler = MinMaxScaler()
            predict_scaler = predict_scaler.fit(row_to_scale.reshape(-1, 1))
        self.predict_scaler = predict_scaler
        scaled_row = self.predict_scaler.transform(np.array(row_to_scale).reshape(-1, 1))
        self.data[self.column_to_predict] = scaled_row

        return

    def __len__(self):
        # Return the number of samples we can extract
        return len(self.data) - (self.input_size + 4)

    def __getitem__(self, idx):
        # Select a slice of `input_size` rows starting from `idx`
        slice_df = self.data.iloc[idx : idx + self.input_size][self.columns_input]
        slice_tensor = torch.tensor(slice_df.values, dtype=torch.float32)

        # Select the next 4 rows of the 'Total load' column
        total_load_df = self.data.iloc[idx + self.input_size : idx + self.input_size + 4][self.column_to_predict]
        total_load_tensor = torch.tensor(total_load_df.values, dtype=torch.float32)

        # Return both tensors
        return slice_tensor.transpose_(0, 1), total_load_tensor

    def get_scaler(self):
        return self.scaler

    def get_predict_scaler(self):
        return self.predict_scaler

    def dernormalize(self, output):
        res = torch.zeros_like(output)
        for b in range(output.shape[0]):  # loop along batchsize
            res1 = torch.from_numpy(self.predict_scaler.inverse_transform(output[b, :].reshape(-1, 1)))
            res[b, :] = res1.reshape(4)
        return res

    def save_scaler(self, name=""):
        joblib.dump(self.scaler, name + "scaler.pkl")
        joblib.dump(self.predict_scaler, name + "predict_scaler.pkl")
