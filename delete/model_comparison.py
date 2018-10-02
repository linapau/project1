# -*- coding: utf-8 -*-
#
# model_comparison.py
#
# The module is part of model_comparison.
#

"""
The model comparison framework.
"""

__author__ = 'Hanna Svennevik', 'Paulina Tedesco'
__email__ = 'hanna.svennevik@fys.uio.no', 'paulinatedesco@gmail.com'


import algorithms
import numpy as np
from model_selection import GridSearch

# Google gridsearch sklearn
    # finne lmd verdien som er best for hvert dataset.


# we have another bootstrap function
# def bootstrap(x):
#         bootVec = np.random.choice(x, len(x))
#         return bootVec, x  # returns x_train, x_test


def generateDesignmatrix(p, x, y):
    m = int((p**2+3*p+2)/2)  # returnerer heltall for p = [1:5]
    X = np.zeros((len(x), m))
    X[:, 0] = 1
    counter = 1
    for i in range(1, p+1):
        for j in range(i+1):
            X[:, counter] = x**(i-j) * y**j
            counter += 1
    return X


def frankeFunction(x, y):
    term1 = 0.75*np.exp(-(0.25*(9*x-2)**2) - 0.25*((9*y-2)**2))
    term2 = 0.75*np.exp(-((9*x+1)**2)/49.0 - 0.1*(9*y+1))
    term3 = 0.5*np.exp(-(9*x-7)**2/4.0 - 0.25*((9*y-3)**2))
    term4 = -0.2*np.exp(-(9*x-4)**2 - (9*y-7)**2)
    return term1 + term2 + term3 + term4


def bootstrap(X, z, random_state):

    # For random randint
    np.random.seed(random_state)

    nrows, ncols = np.shape(X)

    selected_rows = np.random.randint(
        low=0, high=nrows, size=(nrows, ncols)
    )
    selected_cols = np.random.randint(
        low=0, high=ncols, size=(nrows, ncols)
    )
    X_subset = X[selected_rows, selected_cols]
    z_subset = z[selected_rows]

    return X_subset, z_subset


def train_test_split(X, z, split_size=0.2, random_state=None):

    # For random choice.
    np.random.seed(random_state)

    # Extract number of rows and columns in data matrix.
    nrows, ncols = np.shape(X)

    # Determine the proportion of training and test samples
    # from the data matrix size-
    ntest_samples = int(nrows * split_size)
    ntrain_samples = int(nrows - ntest_samples)
    # Randomly select indices for training and test samples
    # without replacement.
    row_samples = np.arange(nrows)
    selected_train_samples = np.random.choice(
        row_samples, ntrain_samples, replace=False
    )
    selected_test_samples = [
        sample for sample in row_samples
        if sample not in selected_train_samples
    ]
    # Extract training and test samples based on selected
    # indices.
    X_train = X[selected_train_samples, :]
    X_test = X[selected_test_samples, :]
    z_train = z[selected_train_samples]
    z_test = z[selected_test_samples]

    return X_train, X_test, z_train, z_test


def model_comparison(models, param_grid, X, z, split_size=0.2, verbose=True):
    """Perform the model comparison experiment.

    Args:
        models (dict):
        param_grid (dict):
        X (array-like):
        y (array-like):
        random_state (array-like)

    Returns:
        (dict): Model scores.
    """

    # NOTE: Increase for more general results.
    random_states = np.arange(4) # number of boots

    results = {}
    for name, estimator in models.items():

        if verbose:
            print('Testing model: {}'.format(name))

        X_boot_std, X_boot_mean = [], []
        z_boot_std, z_boot_mean = [], []

        avg_train_scores_mse, avg_test_scores_mse = [], []
        avg_train_scores_r2, avg_test_scores_r2 = [], []
        bias_models = []  # store the bias of each model
        var_model = []  # store the variance of each model (this is the covariance)
        for num, random_state in enumerate(random_states):

            # Generate data (bootstrap sampling in your case).

            #x_train, x_test = bootstrap(x, random_state=random_state)
            #y_train, y_test = bootstrap(y, random_state=random_state)

            #X_train = generateDesignmatrix(p, x_train, y_train)
            #X_test = generateDesignmatrix(p, x_test, y_test)

            #z_train = frankeFunction(x_train, y_train)
            #z_test = frankeFunction(x_test, y_test)
            #print(np.shape())
            #print(np.shape())
            # Pass algorithm + corresponding params to grid searcher and
            # determine optimal alpha param.

            X_subset, z_subset = bootstrap(X, z, random_state)
            X_train, X_test, z_train, z_test = train_test_split(
                X_subset, z_subset, split_size=split_size
            )
            # TODO: May need to change axis
            X_boot_mean.append(np.mean(X_subset, axis=1))
            X_boot_std.append(np.std(X_subset, axis=1))

            grid = GridSearch(estimator, param_grid[name], random_state)
            grid.fit(X_train, X_test, z_train, z_test)

            # Store average score values (over all lambdas) for each model.
            avg_train_scores_mse.append(np.mean(grid.train_scores_mse)) # we should save the avg over all boots for the best lambda !!!
            avg_test_scores_mse.append(np.mean(grid.test_scores_mse))

            avg_train_scores_r2.append(np.mean(grid.train_scores_r2))
            avg_test_scores_r2.append(np.mean(grid.test_scores_r2))


        if verbose:
            print('Best average train score (mse): {}'.format(
                np.max(avg_train_scores_mse))
            )
            print('Best average train score (r2): {}'.format(
                np.max(avg_train_scores_r2))
            )

            print('Best average test score (mse): {}'.format(
                np.max(avg_test_scores_mse))
            )
            print('Best average test score (r2): {}'.format(
                np.max(avg_test_scores_r2))
            )

        results[name] = {
            'avg_train_scores_mse': avg_train_scores_mse,
            'avg_test_scores_mse': avg_test_scores_mse,
            'avg_train_scores_r2': avg_train_scores_r2,
            'avg_test_scores_r2': avg_test_scores_r2
        }

    return results