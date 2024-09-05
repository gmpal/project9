import pandas as pd
from sklearn.metrics import root_mean_squared_error, mean_absolute_percentage_error

from sys import argv

filename = argv[1]

# Check if a second argument is passed
if len(argv) > 2:
    truth_filename = argv[2]
else:
    truth_filename = "truth.csv"
print(truth_filename)

predictions = pd.read_csv(filename)
truth = pd.read_csv(truth_filename)

t0_rmse = root_mean_squared_error(truth["Total Load Interpolated"][::4], predictions["Prediction"][::4])
t1_rmse = root_mean_squared_error(truth["Total Load Interpolated"][1::4], predictions["Prediction"][1::4])
t2_rmse = root_mean_squared_error(truth["Total Load Interpolated"][2::4], predictions["Prediction"][2::4])
t3_rmse = root_mean_squared_error(truth["Total Load Interpolated"][3::4], predictions["Prediction"][3::4])

t0_mape = mean_absolute_percentage_error(truth["Total Load Interpolated"][::4], predictions["Prediction"][::4])
t1_mape = mean_absolute_percentage_error(truth["Total Load Interpolated"][1::4], predictions["Prediction"][1::4])
t2_mape = mean_absolute_percentage_error(truth["Total Load Interpolated"][2::4], predictions["Prediction"][2::4])
t3_mape = mean_absolute_percentage_error(truth["Total Load Interpolated"][3::4], predictions["Prediction"][3::4])

print("|Model Name|RMSE t+1|RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|")
print(
    "| |",
    str(t0_rmse)[:7],
    "|",
    str(t1_rmse)[:7],
    "|",
    str(t2_rmse)[:7],
    "|",
    str(t3_rmse)[:7],
    "|",
    str(t0_mape)[:7],
    "|",
    str(t1_mape)[:7],
    "|",
    str(t2_mape)[:7],
    "|",
    str(t3_mape)[:7],
    "|",
    sep="",
)
