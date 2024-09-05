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

| Model Name                                    |RMSE t+1|RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|
|-----------------------------------------------|-|-|-|-|-|-|-|-|
| [Linear Model](Models_Pascal/Linear.ipynb)    |85.6921|125.456|154.316|184.128|0.00813|0.01175|0.01466|0.01754|
| [Ridge Model](Models_Pascal/Linear.ipynb)     |85.6604|125.267|154.121|183.717|0.00812|0.01173|0.01462|0.01751|
| [Random Forest](Models_Pascal/Ensemble.ipynb) |87.9629|120.311|144.373|167.454|0.00833|0.01122|0.01349|0.01574|
| [XGBoost](Models_Pascal/Ensemble.ipynb)       |92.3735|125.339|150.321|173.336|0.00888|0.01169|0.01389|0.01609|
| Arima(1,2,2) 1day refitting                   |94.8876|151.737|196.648|249.593|0.00879|0.01398|0.01845|0.02397|
| Arima(1,2,2) 1week no refitting               |94.0714|150.129|192.768|244.266|0.00873|0.01367|0.01778|0.02314|
| [Extra Trees](Models_Pascal/Ensemble.ipynb)   |84.4788|115.733|139.186|162.136|0.00814|0.01087|0.01304|0.01515|
| [MLP](Models_Pascal/MLP_Tuning.ipynb)         |85.6119|125.439|156.732|184.247|0.00801|0.01178|0.01471|0.01730|
| RLS                                           |88.3534|138.603|176.399|218.273|0.00826|0.01282|0.01650|0.02057|
| [LightGBM](LightGBM_Lisbon3_2024.ipynb)       |72.70|109.69|147.09|178.94|0.0068|0.0103|0.0137|0.0169|
| LSTCN                                         |93.3717|149.023|190.526|237.091|0.00893|0.01411|0.01834|0.02326|
| LightGBM with extra features                  |97.4491|147.111|181.713|210.000|0.00918|0.01375|0.01726|0.02009|

| | | | | | | | | |

One month errors for Great Britain (last month of 2023)
|Model Name|RMSE t+1|RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|
|-|-|-|-|-|-|-|-|-|
|[Linear Model](Models_Pascal/GBEvaluation.ipynb)|534.63676|1137.63607|1660.70263|2077.06687|0.01481|0.03140|0.04657|0.05902|
|[Extra Trees](Models_Pascal/GBEvaluation.ipynb)|459.78825|715.86959|1113.03923|1497.24006|0.01144|0.01897|0.03036|0.04033|
