# Total Load Forecasting
## Evaluation Procedure
The samples $335428$ up to $338403$ have to be predicted. Those correspond roughly to the last month, starting at midnight and ending at 23:45.
The output should be placed in a `csv` file structured as:
|Row Number|Prediction|
|-|-|
|0| |
|1| |
|...|...|
|2974| |

The `Row Number` is not a column.

Then, the metrics will be evaluated as RMSE and MAPE. Those metrics will be computed separately on samples at minutes 00, 15, 30 and 45.
In order to get the measurements, execute the (not yet provided) evaluation script as
`python3 evaluate.py your_file.csv`
You can modify the following table to put your results:

|Model Name|RMSE t+1|RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|
|-|-|-|-|-|-|-|-|-|
|Ridge Regression (input:44 previous, output: 4 next)|85.9996|125.568|154.075|183.728|0.00808|0.01161|0.01444|0.01731|
|Random Forest Regressor (input:44 previous, output: 4 next)|87.6351|121.536|145.942|167.905|0.00821|0.01129|0.01359|0.01577|
| | | | | | | | | |
