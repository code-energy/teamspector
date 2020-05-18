import os
import sys
import logging

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from pymongo import MongoClient

from teamspector import datasets

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__file__.split("/")[-1])

get_db = lambda exp: getattr(MongoClient(), exp['dataset'])


def _forecast(experiment):
    results = []
    db = get_db(experiment)
    target = db[f"exp_{experiment['id']}"]

    df = pd.DataFrame(list(target.find())).set_index('_id')

    y = df['top100']
    drop = ['title', 'ypct_rating', 'ypct_votes', 'ypct', 'top100', 'year']
    X = df.drop(drop, axis=1)

    pipe = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='median')),
        ('scaler',  MinMaxScaler()),
        ('regressor', LogisticRegression(solver='lbfgs', max_iter=500)),
    ])

    cv = StratifiedKFold(shuffle=True, random_state=0, n_splits=5)
    scores = cross_val_score(pipe, X, y, cv=cv, n_jobs=1, scoring='roc_auc')
    print("    mean AUC: %f, +/- %f" % (np.mean(scores), np.std(scores)))
    print("    AUC scores", scores)
    results.append(np.mean(scores))
    # if i >= 1:
    #    x = utils.mean_confidence_interval(results)
    #    print("    %.3f, %.4f" % (x[0], x[1]))

    # x = utils.mean_confidence_interval(results)
    # print("%.3f, %.4f" % (x[0], x[1]))
    print(results)


def main():
    dataset_code = sys.argv[1] if len(sys.argv) > 1 else None
    exp_id = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if dataset_code is None or exp_id is None:
        logger.error(f"Usage: {sys.argv[0]} <dataset_code> <experiment id>")
        sys.exit()

    try:
        experiment = getattr(datasets, dataset_code).experiments[exp_id]
    except KeyError:
        logger.error(f"Experiment {exp_id} not found in {dataset_code}.")
        sys.exit()
    except AttributeError:
        logger.error(f"The dataset {dataset_code} doesn't exist.")
        sys.exit()

    _forecast(experiment)


if __name__ == "__main__":
    main()
