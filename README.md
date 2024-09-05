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
| [RNN](DeepLearningForecastingRNNs.ipynb) |97.1521|158.245|194.166|228.928|0.00947|0.01543|0.01865|0.02160|
| [LSTM](DeepLearningForecastingRNNs.ipynb) |117.666|152.433|184.008|222.276|0.01143|0.01452|0.01757|0.02132|
| [GRU](DeepLearningForecastingRNNs.ipynb) |89.7485|143.286|172.319|207.350|0.00850|0.01381|0.01676|0.01987|
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

## Additional Benchmark

The dataset corresponds to ELIA data once it was preprocessed and imputed the missing values. The first 105 months 
(8 years and 9 months) were considered as training set (set A) and the rest (1 year) as test set (set B). From the training set, 
the first 93 months (7 years and 9 months) were used to train the algorithms (set A1) and the next 1 year (set A2) to validate 
the algorithms during Hyperparameter optimization (Hyperopt configuration is discussed later). Once the optimal hyperparameter configuration is obtained, the algorithm 
is retrained with set A and its performance is evaluated with the test B. The results shown in the following tables 
corresponds to this last evaluation.

The time series was processed using a window of size *l={4, 24, 48, 72, 96}* (1, 6, 12, 18, 24 hours respectively) to get a subsequence of the time series as instance and the 
next 4 observations as the forecasting target. To get the next instance, the window is moved *4l* steps ahead.

Best values per forecasting timestep (column) is highlighted.

### Lags 4 (1 hour)

| Model Name                                    |RMSE t+1|RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|
|-----------------------------------------------|-|-|-|-|-|-|-|-|
|ABR|149.7663588|216.9561629|282.9675474|341.2898536|0.012696262|0.01917904|0.024749363|0.029844881|
|Enet|805.12067|825.3492322|854.1196017|885.8410933|0.071598247|0.073763242|0.076626729|0.079662532|
|GBR|`119.8813732`|176.7792652|230.2961201|281.2698089|0.009770161|0.015129321|0.019940721|0.024405835|
|KNN|122.7812732|183.8218228|241.1708486|294.1097608|0.009957092|0.015514292|0.020589624|0.02512241|
|Lasso|1431.458929|1430.469106|1437.855833|1443.481235|0.12158141|0.121603214|0.122242076|0.12304306|
|LightGBM|121.1925801|`175.1941693`|`226.6601246`|`276.9468668`|0.009792854|`0.014825221`|`0.019368965`|`0.023747315`|
|LSTCN|153.4960911|198.8336719|249.5457369|302.0305694|0.012600304|0.016623318|0.020923845|0.025443885|
|NHITS|120.9480871|176.6735725|229.7699426|281.2862785|0.009765661|0.014957715|0.019756316|0.024196061|
|Persistent|142.9297543|226.7981141|306.9628467|383.5750149|0.011655288|0.019273415|0.026429694|0.033318215|
|PipeRF|142.9765677|226.4254766|306.5504363|382.3688243|0.011887619|0.019613771|0.026748552|0.033441327|
|PLS|120.8110094|180.3042776|236.0703381|290.4696883|`0.009678559`|0.015132448|0.01994419|0.024645917|
|RandomForest|207.1472685|268.7281241|336.6578883|404.7777121|0.017176777|0.023441271|0.029662085|0.035824254|
|Ridge|122.1126159|181.4998124|237.4520215|291.9484466|0.00982804|0.015294604|0.020135574|0.024843265|
|RNN|126.6329175|183.9643409|238.8998715|291.8182698|0.010268488|0.01547342|0.020199682|0.024680977|


### Lags 24 (6 hours)

| Model Name                                    | RMSE t+1   |RMSE t+2|RMSE t+3|RMSE t+4|MAPE t+1|MAPE t+2|MAPE t+3|MAPE t+4|
|-----------------------------------------------|------------|-|-|-|-|-|-|-|
|ABR| 139.0528243 |212.4004402|273.1170053|328.636086|0.012169597|0.018057727|0.023454714|0.02823376|
|Enet| 626.0075073 |678.8812908|731.2325276|783.1493299|0.056961149|0.06154771|0.06657339|0.071763522|
|GBR| 107.9735579 |170.9580287|219.4292958|266.2327056|0.009220344|0.014133421|0.018151204|0.022042992|
|KNN| 180.9251216 |228.8683716|272.9151027|315.8920748|0.015511635|0.019034726|0.022708668|0.026020288|
|Lasso| 1428.281106 |1428.682137|1434.282917|1439.555034|0.12144781|0.121258535|0.122009092|0.122796661|
|LightGBM| 107.608104 |166.7476945|208.9241248|250.4238132|0.009098713|0.013657047|0.01719472|0.0208455|
|LightGBM_pip_extra| 110.6069457 |175.2307702|223.4332781|270.8326254|0.009473177|0.014370403|0.018458176|0.02253039|
|NHITS| `106.936547` |`162.3574285`|`200.4577351`|`242.7527846`|`0.009065029`|`0.013223495`|`0.016439657`|`0.020083599`|
|Persistent| 142.4798596 |240.8576115|324.57721|407.4278393|0.01184973|0.019863537|0.02739097|0.034648358|
|PipeRF| 191.4680891 |274.5936443|350.312982|427.8476879|0.016163168|0.023499999|0.030580763|0.037614254|
|PLS| 114.5598537 |188.1483653|243.32812|299.8718054|0.009871744|0.015748957|0.020519889|0.025499514|
|RandomForest| 122.4393996 |194.4468768|251.0837659|308.0790774|0.010576807|0.016267194|0.021004706|0.025918579|
|Ridge| 115.3236073 |188.2021562|243.7039617|300.1214647|0.009942083|0.015802709|0.020513744|0.025506527|





