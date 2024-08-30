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
|[Linear Model](Models_Pascal/Linear.ipynb)|85.2385|129.439|160.070|193.590|0.00805|0.01204|0.01499|0.01800|
|[Ridge Model](Models_Pascal/Linear.ipynb)|85.4773|128.964|159.194|192.266|0.00806|0.01197|0.01489|0.01788|
|[Random Forest](Models_Pascal/Ensemble.ipynb)|86.4348|121.865|147.196|173.907|0.00819|0.01132|0.01372|0.01624|
|[XGBoost](Models_Pascal/Ensemble.ipynb)|86.9875|121.567|147.213|171.274|0.00830|0.01136|0.01374|0.01606|
|Arima(1,2,2) 1day refitting|94.8876|151.737|196.648|249.593|0.00879|0.01398|0.01845|0.02397|
|Arima(1,2,2) 1week no refitting |94.0714|150.129|192.768|244.266|0.00873|0.01367|0.01778|0.02314|
|[Extra Trees](Models_Pascal/Ensemble.ipynb)|84.2570|116.050|139.287|161.741|0.00809|0.01085|0.01296|0.01510|
|[MLP](DeepLearningForecastingWithTotalLoadOnly.ipynb)|129.140|162.836|192.684|227.441|0.01251|0.01576|0.01885|0.02253|
| | | | | | | | | |

One month errors for Great Britain (last month of 2023)
|Model Name|RMSE t+1|RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|
|-|-|-|-|-|-|-|-|-|
|[Linear Model](Models_Pascal/GBEvaluation.ipynb)|534.63676|1137.63607|1660.70263|2077.06687|0.01481|0.03140|0.04657|0.05902|
|[Extra Trees](Models_Pascal/GBEvaluation.ipynb)|459.78825|715.86959|1113.03923|1497.24006|0.01144|0.01897|0.03036|0.04033|
