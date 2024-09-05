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

| Model Name                                    | RMSE t+1 | RMSE t+2 | RMSE t+3  | RMSE t+4  | MAPE t+1 | MAPE t+2 | MAPE t+3  | MAPE t+4  |
|-----------------------------------------------|----------|----------|-----------|-----------|----------|----------|-----------|-----------|
| [Linear Model](Models_Pascal/Linear.ipynb)    | 85.6921  | 125.456  | 154.316   | 184.128   | 0.00813  | 0.01175  | 0.01466   | 0.01754   |
| [Ridge Model](Models_Pascal/Linear.ipynb)     | 85.6604  | 125.267  | 154.121   | 183.717   | 0.00812  | 0.01173  | 0.01462   | 0.01751   |
| [Random Forest](Models_Pascal/Ensemble.ipynb) | 87.9629  | 120.311  | 144.373   | 167.454   | 0.00833  | 0.01122  | 0.01349   | 0.01574   |
| [XGBoost](Models_Pascal/Ensemble.ipynb)       | 92.3735  | 125.339  | 150.321   | 173.336   | 0.00888  | 0.01169  | 0.01389   | 0.01609   |
| Arima(1,2,2) 1day refitting                   | 94.8876  | 151.737  | 196.648   | 249.593   | 0.00879  | 0.01398  | 0.01845   | 0.02397   |
| Arima(1,2,2) 1week no refitting               | 94.0714  | 150.129  | 192.768   | 244.266   | 0.00873  | 0.01367  | 0.01778   | 0.02314   |
| [Extra Trees](Models_Pascal/Ensemble.ipynb)   | 84.4788  | 115.733  | `139.186` | `162.136` | 0.00814  | 0.01087  | `0.01304` | `0.01515` |
| [MLP](Models_Pascal/MLP_Tuning.ipynb)         | 85.6119  | 125.439  | 156.732   | 184.247   | 0.00801  | 0.01178  | 0.01471   | 0.01730   |
| [RNN](DeepLearningForecastingRNNs.ipynb)      | 97.1521  | 158.245  | 194.166   | 228.928   | 0.00947  | 0.01543  | 0.01865   | 0.02160   |
| [LSTM](DeepLearningForecastingRNNs.ipynb)     | 117.666  | 152.433  | 184.008   | 222.276   | 0.01143  | 0.01452  | 0.01757   | 0.02132   |
| [GRU](DeepLearningForecastingRNNs.ipynb)      | 89.7485  | 143.286  | 172.319   | 207.350   | 0.00850  | 0.01381  | 0.01676   | 0.01987   |
| RLS                                           | 88.3534  | 138.603  | 176.399   | 218.273   | 0.00826  | 0.01282  | 0.01650   | 0.02057   |
| [LightGBM](LightGBM_Lisbon3_2024.ipynb)       | `72.70`  | `109.69` | 147.09    | 178.94    | `0.0068` | `0.0103` | 0.0137    | 0.0169    |
| LSTCN                                         | 93.3717  | 149.023  | 190.526   | 237.091   | 0.00893  | 0.01411  | 0.01834   | 0.02326   |
| LightGBM with extra features                  | 97.4491  | 147.111  | 181.713   | 210.000   | 0.00918  | 0.01375  | 0.01726   | 0.02009   |

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

| Model Name                                                                                                                                     | RMSE t+1      | RMSE t+2      | RMSE t+3      | RMSE t+4      | MAPE t+1      | MAPE t+2      | MAPE t+3      | MAPE t+4      |
|------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| [ABR](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html)                                               | 149.7663588   | 216.9561629   | 282.9675474   | 341.2898536   | 0.012696262   | 0.01917904    | 0.024749363   | 0.029844881   |
| [Enet](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html)                                                 | 805.12067     | 825.3492322   | 854.1196017   | 885.8410933   | 0.071598247   | 0.073763242   | 0.076626729   | 0.079662532   |
| [GBR](https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_regression.html)                                           | `119.8813732` | 176.7792652   | 230.2961201   | 281.2698089   | 0.009770161   | 0.015129321   | 0.019940721   | 0.024405835   |
| [KNN](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html)                                            | 122.7812732   | 183.8218228   | 241.1708486   | 294.1097608   | 0.009957092   | 0.015514292   | 0.020589624   | 0.02512241    |
| [Lasso](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html)                                                     | 1431.458929   | 1430.469106   | 1437.855833   | 1443.481235   | 0.12158141    | 0.121603214   | 0.122242076   | 0.12304306    |
| [LightGBM - DARTS implementation ](https://unit8co.github.io/darts/generated_api/darts.models.forecasting.lgbm.html)                           | 121.1925801   | `175.1941693` | `226.6601246` | `276.9468668` | 0.009792854   | `0.014825221` | `0.019368965` | `0.023747315` |
| [LSTCN](https://github.com/gnapoles/lstcn)                                                                                                     | 153.4960911   | 198.8336719   | 249.5457369   | 302.0305694   | 0.012600304   | 0.016623318   | 0.020923845   | 0.025443885   |
| [NHITS](https://unit8co.github.io/darts/generated_api/darts.models.forecasting.nhits.html)                                                     | 120.9480871   | 176.6735725   | 229.7699426   | 281.2862785   | 0.009765661   | 0.014957715   | 0.019756316   | 0.024196061   |
| Persistent (Forwarding the last observed value)                                                                                                | 142.9297543   | 226.7981141   | 306.9628467   | 383.5750149   | 0.011655288   | 0.019273415   | 0.026429694   | 0.033318215   |
| [PipeRF - Pipeline with feature selection for Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) | 142.9765677   | 226.4254766   | 306.5504363   | 382.3688243   | 0.011887619   | 0.019613771   | 0.026748552   | 0.033441327   |
| [PLS](https://scikit-learn.org/stable/modules/generated/sklearn.cross_decomposition.PLSRegression.html)                                        | 120.8110094   | 180.3042776   | 236.0703381   | 290.4696883   | `0.009678559` | 0.015132448   | 0.01994419    | 0.024645917   |
| [RandomForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)                                  | 207.1472685   | 268.7281241   | 336.6578883   | 404.7777121   | 0.017176777   | 0.023441271   | 0.029662085   | 0.035824254   |
| [Ridge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html)                                                     | 122.1126159   | 181.4998124   | 237.4520215   | 291.9484466   | 0.00982804    | 0.015294604   | 0.020135574   | 0.024843265   |
| [RNN - Darts implementation](https://unit8co.github.io/darts/generated_api/darts.models.forecasting.rnn_model.html)                            | 126.6329175   | 183.9643409   | 238.8998715   | 291.8182698   | 0.010268488   | 0.01547342    | 0.020199682   | 0.024680977   |


### Lags 24 (6 hours)

| Model Name         | RMSE t+1        | RMSE t+2      | RMSE t+3      | RMSE t+4      | MAPE t+1      | MAPE t+2      | MAPE t+3      | MAPE t+4      |
|--------------------|-----------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| ABR                | 139.0528243     | 212.4004402   | 273.1170053   | 328.636086    | 0.012169597   | 0.018057727   | 0.023454714   | 0.02823376    |
| Enet               | 626.0075073     | 678.8812908   | 731.2325276   | 783.1493299   | 0.056961149   | 0.06154771    | 0.06657339    | 0.071763522   |
| GBR                | 107.9735579     | 170.9580287   | 219.4292958   | 266.2327056   | 0.009220344   | 0.014133421   | 0.018151204   | 0.022042992   |
| KNN                | 180.9251216     | 228.8683716   | 272.9151027   | 315.8920748   | 0.015511635   | 0.019034726   | 0.022708668   | 0.026020288   |
| Lasso              | 1428.281106     | 1428.682137   | 1434.282917   | 1439.555034   | 0.12144781    | 0.121258535   | 0.122009092   | 0.122796661   |
| LightGBM           | 107.608104      | 166.7476945   | 208.9241248   | 250.4238132   | 0.009098713   | 0.013657047   | 0.01719472    | 0.0208455     |
| LightGBM_pip_extra | 110.6069457     | 175.2307702   | 223.4332781   | 270.8326254   | 0.009473177   | 0.014370403   | 0.018458176   | 0.02253039    |
| NHITS              | `106.936547`    | `162.3574285` | `200.4577351` | `242.7527846` | `0.009065029` | `0.013223495` | `0.016439657` | `0.020083599` |
| Persistent         | 142.4798596     | 240.8576115   | 324.57721     | 407.4278393   | 0.01184973    | 0.019863537   | 0.02739097    | 0.034648358   |
| PipeRF             | 191.4680891     | 274.5936443   | 350.312982    | 427.8476879   | 0.016163168   | 0.023499999   | 0.030580763   | 0.037614254   |
| PLS                | 114.5598537     | 188.1483653   | 243.32812     | 299.8718054   | 0.009871744   | 0.015748957   | 0.020519889   | 0.025499514   |
| RandomForest       | 122.4393996     | 194.4468768   | 251.0837659   | 308.0790774   | 0.010576807   | 0.016267194   | 0.021004706   | 0.025918579   |
| Ridge              | 115.3236073     | 188.2021562   | 243.7039617   | 300.1214647   | 0.009942083   | 0.015802709   | 0.020513744   | 0.025506527   |
| RNN                | **OUT OF TIME** |

### Lags 48 (12 hours)

| Model Name                                                                                                                   | RMSE t+1        | RMSE t+2     | RMSE t+3      | RMSE t+4      | MAPE t+1      | MAPE t+2      | MAPE t+3      | MAPE t+4     |
|------------------------------------------------------------------------------------------------------------------------------|-----------------|--------------|---------------|---------------|---------------|---------------|---------------|--------------|
| ABR                                                                                                                          | 142.7329948     | 201.5780788  | 256.6538383   | 310.6597671   | 0.01167508    | 0.017436196   | 0.02241507    | 0.026873159  |
| Enet                                                                                                                         | 641.6783215     | 687.5732905  | 740.2055214   | 788.4869014   | 0.058620538   | 0.061878709   | 0.066334511   | 0.070776666  |
| GBR                                                                                                                          | 113.0919412     | 160.7988188  | 202.398073    | 239.0677171   | 0.009117468   | 0.013684927   | 0.017474897   | 0.020826198  |
| KNN                                                                                                                          | 229.906994      | 254.3672349  | 278.9953945   | 306.0883148   | 0.019499966   | 0.021781373   | 0.024094305   | 0.02645779   |
| Lasso                                                                                                                        | 1436.272507     | 1433.642362  | 1441.618223   | 1445.017432   | 0.12196638    | 0.121629971   | 0.122311842   | 0.123321677  |
| LightGBM                                                                                                                     | `103.3151898`   | `144.855292` | `178.1028108` | `215.0817916` | `0.008293836` | `0.012076173` | `0.014974196` | `0.01838854` |
| [LightGBM_pip_extra](https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html#lightgbm.LGBMRegressor) | 110.4592813     | 158.3183102  | 194.9119953   | 233.4880581   | 0.008888442   | 0.013243492   | 0.016359913   | 0.019766536  |
| NHITS                                                                                                                        | 109.2366624     | 153.5494285  | 185.679715    | 222.8547369   | 0.008894059   | 0.012915885   | 0.01566968    | 0.018973658  |
| Persistent                                                                                                                   | 144.8653831     | 234.9701975  | 318.5997471   | 396.8535242   | 0.011783165   | 0.019834258   | 0.02712167    | 0.034210729  |
| PipeRF                                                                                                                       | 149.864792      | 238.6528849  | 322.3495456   | 401.0603179   | 0.012223194   | 0.020256623   | 0.027592231   | 0.034409216  |
| PLS                                                                                                                          | 120.8503803     | 179.316565   | 234.106728    | 287.0083628   | 0.009924076   | 0.015295215   | 0.019963055   | 0.024325218  |
| RandomForest                                                                                                                 | 146.6429055     | 211.4142921  | 274.9182619   | 333.747158    | 0.012360768   | 0.018306387   | 0.023904708   | 0.029021125  |
| Ridge                                                                                                                        | 118.3334577     | 176.9581551  | 231.0699492   | 282.8739517   | 0.009539638   | 0.015003187   | 0.0196562     | 0.024044317  |
| RNN                                                                                                                          | **OUT OF TIME** |

### Lags 72 (18 hours)

| Model Name         | RMSE t+1        | RMSE t+2      | RMSE t+3      | RMSE t+4      | MAPE t+1      | MAPE t+2      | MAPE t+3      | MAPE t+4      |
|--------------------|-----------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| ABR                | 108.9409036     | 158.8276724   | 198.0430831   | 237.1922996   | 0.009497188   | 0.013964239   | 0.017335767   | 0.020233107   |
| Enet               | 601.0722729     | 646.3330135   | 689.535159    | 732.0954298   | 0.053993558   | 0.058002637   | 0.062275235   | 0.066493923   |
| GBR                | 100.3852377     | 144.6609246   | 182.5637512   | 218.779494    | 0.008879519   | 0.012688017   | 0.015500348   | 0.018150304   |
| KNN                | 278.5918396     | 304.3633848   | 322.4574483   | 343.254066    | 0.024094659   | 0.02603951    | 0.027830069   | 0.030039766   |
| Lasso              | 1407.915213     | 1409.943202   | 1415.890099   | 1417.777673   | 0.119069622   | 0.119040909   | 0.119553318   | 0.119695152   |
| LightGBM           | `93.93027807`   | `127.9045315` | `158.5019659` | `199.2810894` | `0.008163751` | `0.011102789` | `0.013721039` | `0.016779612` |
| LightGBM_pip_extra | 97.8090612      | 146.9259457   | 184.3541713   | 221.8573463   | 0.008588008   | 0.012874724   | 0.015633381   | 0.01859898    |
| NHITS              | **OUT OF TIME** |
| Persistent         | 136.6357403     | 223.4792208   | 301.6511041   | 381.8901476   | 0.011836293   | 0.019341243   | 0.026076065   | 0.03319432    |
| PipeRF             | 141.5309206     | 230.7738853   | 309.1652181   | 390.7638044   | 0.012387144   | 0.020144762   | 0.026724928   | 0.033956942   |
| PLS                | 109.7900847     | 160.6611447   | 205.0478714   | 244.7273891   | 0.009506959   | 0.01402796    | 0.01746557    | 0.020437683   |
| RandomForest       | 208.7897794     | 265.3248998   | 323.7248662   | 389.4942457   | 0.017700163   | 0.023222821   | 0.028640204   | 0.034586349   |
| Ridge              | 106.1351908     | 157.946018    | 202.4093915   | 241.922406    | 0.009203941   | 0.013920247   | 0.017409343   | 0.020465755   |
| RNN                | **OUT OF TIME** |

### Lags 96 (24 hours)

| Model Name         | RMSE t+1        | RMSE t+2      | RMSE t+3      | RMSE t+4      | MAPE t+1      | MAPE t+2      | MAPE t+3      | MAPE t+4      |
|--------------------|-----------------|---------------|---------------|---------------|---------------|---------------|---------------|---------------|
| ABR                | 177.3716498     | 200.9649566   | 253.3008621   | 294.7677751   | 0.012906552   | 0.017178804   | 0.021958894   | 0.025388082   |
| Enet               | 542.4526441     | 571.686928    | 603.5306071   | 632.3949974   | 0.049478109   | 0.052448152   | 0.055758744   | 0.058446425   |
| GBR                | 158.9653899     | 160.6851296   | 201.1073531   | 228.7685834   | 0.010298235   | 0.012813353   | 0.016607775   | 0.018834914   |
| KNN                | 295.1613284     | 304.7189856   | 319.0345748   | 329.4329967   | 0.025462625   | 0.026592867   | 0.027987634   | 0.029006558   |
| Lasso              | 1416.738692     | 1426.497265   | 1436.338882   | 1441.04838    | 0.120158366   | 0.12152215    | 0.12291089    | 0.123932641   |
| LightGBM           | `146.5966411`   | `140.8565588` | `168.1688784` | `185.5501953` | `0.008983941` | `0.011013345` | `0.013497918` | `0.015444816` |
| LightGBM_pip_extra | 154.0346083     | 153.1336533   | 184.8298451   | 206.1386711   | 0.009772663   | 0.012348363   | 0.015450514   | 0.017946549   |
| Persistent         | 182.4342627     | 237.1435935   | 323.7755837   | 404.4736116   | 0.012730975   | 0.019952388   | 0.027636093   | 0.034655118   |
| PipeRF             | 190.5153584     | 226.2945184   | 294.5396456   | 361.5795547   | 0.013652471   | 0.019046648   | 0.024862174   | 0.030463994   |
| PLS                | 158.1558607     | 158.584736    | 195.9374767   | 221.8814247   | 0.009371503   | 0.011972523   | 0.015176825   | 0.0174278     |
| RandomForest       | 190.179785      | 216.207648    | 272.2594846   | 328.1407512   | 0.013624431   | 0.017983247   | 0.022928445   | 0.027642722   |
| Ridge              | 159.070905      | 160.6860418   | 197.5722688   | 223.3844548   | 0.009819136   | 0.012347566   | 0.015583662   | 0.017782134   |
| RNN                | **OUT OF TIME** |

### *Notes:*

- *LightGBM_pip* refers to the implementation provided by the python package that we can install directly with pip.
- *LightGBM_pip_extra* refers to training *LightGBM_pip* with additional features extracted from the instances conformed during 
the processing of the time series. When l=4, there were not enough information to extract some of the additional features. 
Therefore, *LightGBM_pip_extra* was not run with this setting
- LSTCN results are not provided for l={24, 48 72, 96} because uses L=H
- NHITS was stopped after l=48 because it was taking a complete day to optimize its hyperparameters
- RNN was still running for l>=24 at the moment of writing this file

The additional features extracted for each instance were obtained with the library [`tsfel`](https://tsfel.readthedocs.io/en/latest/) 
and they are:

- Max
- Mean
- Median
- Min
- Variance
- Signal distance
- Entropy
- Interquartile range
- Lempel-Ziv complexity
- Mean absolute deviation
- Mean absolute diff
- Mean diff
- Median absolute deviation
- Median absolute diff
- Median diff
- Negative turning points
- Petrosian fractal dimension
- Positive turning points
- Root mean square
- Slope

### *Hyperopt configuration*

- Iterations (number of hyperparameters configurations evaluated): 75
- gamma: 0.25
- candidates per iteration: 24





