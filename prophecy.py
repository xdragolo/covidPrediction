import itertools
import warnings

import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from pylab import rcParams, np
import statsmodels.api as sm

warnings.filterwarnings("ignore")
plt.style.use('fivethirtyeight')

df = pd.read_csv('nakazeni-vyleceni-umrti-testy.csv')
df['datum'] = pd.to_datetime(df['datum'])
df.set_index(['datum'], inplace=True)
df = df['kumulativni_pocet_nakazenych']


# autocorrelation_plot(df)
# plt.show()

# decomposition = sm.tsa.seasonal_decompose(df, model='additive')
# fig = decomposition.plot()
# plt.show()

# rcParams['figure.figsize'] = 15, 10
# df.plot(figsize=(15,10))
# plt.show()

# parametrs for ARIMA
p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

# grid search
r = []
i = 0

# for param in pdq:
#     for param_seasonal in seasonal_pdq:
#         try:
#             print(i)
#             i += 1
#             mod = sm.tsa.statespace.SARIMAX(df, order=param,
#                                             seasonal_order=param_seasonal,
#                                             enforce_stationarity=False,
#                                             enforce_invertibility=False)
#             results = mod.fit(disp=0)
#             r.append((param, param_seasonal, results.aic))
#             # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
#             # print(results)
#         except:
#             continue

# optimal params
# r.sort(key=lambda x: x[2], reverse=False)
# order = r[0][0]
# seasonal_order = r[0][0]
order = (1 ,1, 1)
# seasonal_order = (0, 1, 1, 12)

mod = sm.tsa.statespace.SARIMAX(df, order= order)
results = mod.fit()
# print(results.summary().tables[1])
#
# results.plot_diagnostics(figsize=(16,8))
# plt.show()

prediction = results.get_prediction(start=pd.to_datetime('2020-12-01'), dynamic=False)
pred_ci = prediction.conf_int()
#
# # prediction graph
ax = df['2020-12':].plot(label='real')
prediction.predicted_mean.plot(ax=ax,label='one-step ahead', alpha=.7, figsize=(14,7))
ax.fill_between(pred_ci.index, pred_ci.iloc[:,0], pred_ci.iloc[:,1], color = 'k', alpha=.2)
ax.set_xlabel('Date')
ax.set_ylabel('infected')

plt.legend()
# plt.savefig('./Figures/decemberPrediction.png', bbox_inches = 'tight' )
plt.show()
#
y_predicted = prediction.predicted_mean
y_real = df['2020-10-01']
mse = ((y_predicted - y_real) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error of our forecasts is {}'.format(round(np.sqrt(mse), 2)))

# future prediction
# future = results.get_forecast(steps=100)
# pred_ci = future.conf_int()
#
# ax = df.plot(label='observed', figsize=(14,7))
# future.predicted_mean.plot(ax=ax,label= 'forecast')
# ax.fill_between(pred_ci.index, pred_ci.iloc[:,0], pred_ci.iloc[:,1], color='k', alpha=.25)
# ax.set_xlabel('Date')
# ax.set_ylabel('Infected')
#
# plt.legend()
# plt.show()
