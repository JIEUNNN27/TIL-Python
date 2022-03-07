# -*- coding: utf-8 -*-
"""Boston(GridSearchCV).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cQ91Vyd2JBDCCi37rao9ByCFI8vPdliN
"""

import pandas as pd
import numpy as np
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as  plt

# Boston house dataset을 읽어온다.
boston = load_boston()

# 데이터 프레임 형태로 저장한다.
df = pd.DataFrame(boston.data, columns = boston.feature_names)
df['PRICE'] = boston.target

# 데이터 스케일 조정. 데이터 표준화에 대해서는 추후 정리할 예정임.
df['ZN'] /= 10
df['AGE'] /= 10
df['TAX'] /= 100
df['PTRATIO'] /= 10
df['B'] /= 100
df['PRICE'] /= 10

df.head()

# 학습 데이터와 시험 데이터로 분리한다.
x_train, x_test, y_train, y_test = train_test_split(boston.data, boston.target, test_size = 0.15)
x_train.shape, x_test.shape

d_max = 10
dt_params = [{'max_depth': np.arange(1, d_max)}]
dt = DecisionTreeRegressor()
dt_grid = GridSearchCV(estimator=dt, param_grid=dt_params, cv=5, refit=True)
dt_grid.fit(x_train, y_train)

# grid.cv_results_     : K-fold cross validation test 결과 dictionary
# grid.best_params_    : best parameter ==> {'max_depth': 5}
# grid.best_estimator_ : best parameter로 생성한 tree

sv_params = [{'kernel': ['rbf'], 'C':[1000, 10000, 20000], 'epsilon':[0.1, 1.0, 2.0]}]
sv = SVR()
sv_grid = GridSearchCV(estimator=sv, param_grid=sv_params, cv=5, refit=True)
sv_grid.fit(x_train, y_train)

print('Decision Tree: Best paramter =', dt_grid.best_params_)
dt_best = dt_grid.best_estimator_
print('Decision Tree: evaluation data의 score = {:.3f}'.format(dt_best.score(x_test, y_test)))

print('\nSVR: Best paramter =', sv_grid.best_params_)
sv_best = sv_grid.best_estimator_
print('SVR: evaluation data의 score = {:.3f}'.format(dt_best.score(x_test, y_test)))

# test data의 추정 결과를 육안으로 확인한다. SVR만 확인.
y_pred = sv_best.predict(x_test)

# 원래 스케일로 환원한다.
d_test = y_test * 10
d_pred = y_pred * 10

df_pred = pd.DataFrame(np.c_[d_test, d_pred], columns=['d_test', 'd_pred'])
df_pred.head()

# 추정 결과를 시각화 한다.
plt.figure(figsize=(6, 6))
plt.scatter(d_test, d_pred, c='red', s=30, alpha=0.5)
plt.xlabel("house price")
plt.ylabel("predicted price")
plt.show()

