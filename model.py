import pandas as pd
import numpy as np
from datetime import date
from superugby import cleanup
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_selection import SelectFwe, f_regression
from sklearn.linear_model import ElasticNetCV, LassoLarsCV
from sklearn.pipeline import make_pipeline, make_union
from sklearn.externals import joblib
from tpot.builtins import StackingEstimator, ZeroCount


def fit_predict(op_df, retrain=True):

    # make copy of dataframe
    df = pd.DataFrame(op_df)
    df = cleanup(df)

    # scale numerical features
    scaler = StandardScaler()

    numeric = ['home_streak', 'home_avg_marg', 'away_streak', 'away_avg_marg', 'home_win_prob']
    df[numeric] = scaler.fit_transform(df[numeric].astype('float64'))

    # calculate number of upcoming fixtures in data set (to be excluded from training data)
    today = pd.to_datetime(date.today())
    n_upcoming = len(df[df.Date >= pd.to_datetime(date.today())])

    print('predicting results for ', n_upcoming, 'upcoming fixtures...')

    X = df[n_upcoming:].drop(['Date', 'home_margin', 'home_win'], axis=1).values.astype(np.float64)
    y = df[n_upcoming:].home_margin.values.astype(np.float64)

    # hold the upcoming fixtures out of the train set:
    X_temp = df[:n_upcoming].drop(['Date', 'home_margin', 'home_win'], axis=1).values.astype(np.float64)
    y_temp = df[:n_upcoming].home_margin.values.astype(np.float64)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if retrain:
        # retrain model
        pipeline = make_pipeline(
            ZeroCount(),
            StackingEstimator(estimator=GradientBoostingRegressor(alpha=0.99,
                                                                  learning_rate=0.01,
                                                                  loss="quantile",
                                                                  max_depth=4,
                                                                  max_features=0.95,
                                                                  min_samples_leaf=17,
                                                                  min_samples_split=8,
                                                                  n_estimators=100,
                                                                  subsample=0.35)),
            StackingEstimator(estimator=ElasticNetCV(l1_ratio=0.05, tol=0.1, cv=5)),
            SelectFwe(score_func=f_regression, alpha=0.031),
            LassoLarsCV(normalize=True, cv=5)
        )

        pipeline.fit(X_train, y_train)

        # save model and bag of words as pickle files
        joblib.dump(pipeline, 'model.pkl')

    else:
    # load trained model from pickle file
        pipeline_pkl = open('model.pkl','rb')
        pipeline = joblib.load(pipeline_pkl)

    predictions = pipeline.predict(df.drop(['Date', 'home_margin', 'home_win'], axis=1).values.astype(np.float64))

    return np.round(predictions)
