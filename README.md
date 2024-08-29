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
|[Linear Model](Linear.ipynb)|85.2385|129.439|160.070|193.590|0.00805|0.01204|0.01499|0.01800|
|[Ridge Model](Linear.ipynb)|85.4773|128.964|159.194|192.266|0.00806|0.01197|0.01489|0.01788|
|[Random Forest](Ensemble.ipynb)|86.4348|121.865|147.196|173.907|0.00819|0.01132|0.01372|0.01624|
|[XGBoost](Ensemble.ipynb)|86.9875|121.567|147.213|171.274|0.00830|0.01136|0.01374|0.01606|
| | | | | | | | | |
