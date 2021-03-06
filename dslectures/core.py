# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/utils00_core.ipynb (unless otherwise specified).

__all__ = ['get_dataset', 'rmse', 'convert_strings_to_categories', 'fill_missing_values_with_median',
           'make_polynomial_data', 'PolynomialRegressor', 'display_large', 'rf_feature_importance',
           'plot_feature_importance', 'plot_dendogram', 'plot_fitting_graph', 'plot_classifier_boundaries']

# Cell
from nbdev.showdoc import *
import wget
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from pandas.api.types import is_object_dtype, is_numeric_dtype
import seaborn as sns
import scipy
from scipy.cluster import hierarchy as hc
import matplotlib.pyplot as plt

# Cell
def get_dataset(dataset_name: str, path="../data/"):
    """
    Download datasets from Google Drive.
    """

    name_to_id = {
        "word2vec-google-news-300.pkl": "1dRwSXbFTcQbn8c3V24G92wFY4DXZ1SDt",
        "imdb.csv": "1wF0YEmQOwceJz2d6w4CfhBgydU87dPGl",
        "housing.csv": "1d7oOKdDmZFx8wf0c8OfuTW1FpUyJHABh",
        "housing_gmaps_data_raw.csv": "1R1RUHAXxzrIngRJMFwyp4vZRVICd-I6T",
        "housing_addresses.csv": "1mOK0uyRz5Zs-Qo7mVMlxwtb2xn1E6N9Q",
        "housing_merged.csv": "1bdYuBtIPrKiU-ut2MeSSsL47onPtZrRt",
        "housing_processed.csv": "12PxnWhPg_Pj0yx75vD22gwfdkkx80E6_",
        "churn.csv": "1-IO-JQr7tjQGIKZyo_SyupCpX2VNDQIf",
        "kaggle_housing_train.csv": "1BHiuZyMab7rPA8Rog29fIYhJmjvJLkVI",
        "kaggle_housing_test.csv": "1KSfBhIdFlejUWAnrfFl10c-rjA4VhgkT",
        "kaggle_titanic_train.csv": "1BHiuZyMab7rPA8Rog29fIYhJmjvJLkVI",
        "kaggle_titanic_test.csv": "1NFCDTBF4dM8rllv0fP3VnPmoRLmfdOEB",
        "fine_tuned.pth": "S3",
        "data_lm.pkl": "S3"
    }
    os.makedirs(path, exist_ok=True)
    gdrive_path = "https://docs.google.com/uc?export=download&id="
    s3_path = "https://dslectures.s3.eu-central-1.amazonaws.com/"

    if dataset_name in name_to_id:
        if os.path.exists(path + dataset_name):
            print(
                f"Dataset already exists at '{path + dataset_name}' and is not downloaded again."
            )
            return
        try:
            if name_to_id[dataset_name]=="S3":
                file_url = s3_path + dataset_name
            else:
                file_url = gdrive_path + name_to_id[dataset_name]
            wget.download(file_url, out=path)
        except Exception as e:
            print("Something went wrong during download. Try again.")
            raise e
        print(f"Download of {dataset_name} dataset complete.")
    else:
        raise KeyError("File not on Google Drive.")

# Cell
def rmse(y, yhat):
    """A utility function to calculate the Root Mean Square Error (RMSE).

    Args:
        y (array): Actual values for target.
        yhat (array): Predicted values for target.

    Returns:
        rmse (double): The RMSE.
    """
    return np.sqrt(mean_squared_error(y, yhat))

# Cell
def convert_strings_to_categories(df):
    """A utility function to convert all string columns to Categorical data type."""
    for col in df.columns:
        if is_object_dtype(df[col]):
            df[col] = df[col].astype("category")

# Cell
def fill_missing_values_with_median(df):
    """Replaces missing values in numerical columns with the median."""
    for column in df.columns:
        if is_numeric_dtype(df[column]):
            if pd.isnull(df[column]).sum():
                column_median = df[column].median()
                df[column].fillna(column_median, inplace=True)

# Cell
def make_polynomial_data(weight, n_samples=100, seed=42):
    """
    Creates noisy polynomial data.

    Args:
        weight (array): polynomial weights in descending order
        n_samples (int): number of samples
        seed (int): random seed

    returns:
        x (array): x-values
        y (array): y-values
    """

    np.random.seed(seed)

    # generate random points on the x axis
    x = (0.5-np.random.rand(n_samples))*2

    # sort the array
    x = np.sort(x)

    # evalute polynomial with weight w at positions x
    y_true = np.polyval(weight, x)

    # add noise samples from the normal gaussian
    # distribution to the data.
    y = y_true + np.random.randn(n_samples)

    return x, y

# Cell

class PolynomialRegressor:
    """
    Scikit-like interface to fit polynomials.
    """
    def __init__(self, degree=0, w_hat=None):
        """
        Initialize polynomial fitter.

        args:
            degree (int): degree of polynomial to fit, default: 0.
            w_hat (array): polynomial weights, default: None.

        """
        self.degree = degree
        self.w_hat = w_hat

    def fit(self, x, y):
        """Fit polynomial to x,y data."""
        self.w_hat = np.polyfit(x, y, self.degree)
        return self

    def predict(self, x):
        """Predict y with fitted polynomial."""
        if self.w_hat is not None:
            return np.polyval(self.w_hat, x)
        else:
            raise ValueError('You need to first fit the model.')

    def evaluate(self, x, y):
        """Evaluate RMSE score of y and predictions for y."""
        if self.w_hat is not None:
            y_hat = np.polyval(self.w_hat, x)
            return rmse(y, y_hat)
        else:
            raise ValueError('You need to first fit the model.')

    def get_params(self, **kwargs):
        return {'w_hat': self.w_hat,
                'degree': self.degree}


# Cell
def display_large(df):
    """Displays up to 1000 columns and rows of pandas.DataFrame or pandas.Series objects."""
    with pd.option_context("display.max_rows", 1000, "display.max_columns", 1000):
        display(df)

# Cell
def rf_feature_importance(fitted_model, df):
    "Creates a pandas.Dataframe of a Random Forest's feature importance per column."
    return pd.DataFrame(
        {"Column": df.columns, "Importance": fitted_model.feature_importances_}
    ).sort_values("Importance", ascending=False)

# Cell
def plot_feature_importance(feature_importance):
    fig, ax = plt.subplots(figsize=(12,8))
    return sns.barplot(y="Column", x="Importance", data=feature_importance, color="b")

# Cell
def plot_dendogram(X):
    """Plots a dendogram to see which features are related."""
    # calculate correlation coefficient
    corr = np.round(scipy.stats.spearmanr(X).correlation, 4)
    # convert to distance matrix
    corr_condensed = hc.distance.squareform(1 - corr)
    # perform clustering
    z = hc.linkage(corr_condensed, method="average")
    # plot dendogram
    fig = plt.figure(figsize=(16, 10))
    dendrogram = hc.dendrogram(
        z, labels=X.columns, orientation="left", leaf_font_size=16
    )
    plt.show()

# Cell
def plot_fitting_graph(x, metric_train, metric_valid, metric_name='metric', xlabel='x', yscale='linear'):
    """Plot fitting graph for train and validation metrics."""
    plt.plot(x, metric_train, label='train')
    plt.plot(x, metric_valid, label='valid')
    plt.yscale(yscale)
    plt.title('Fitting graph')
    plt.ylabel(metric_name)
    plt.xlabel(xlabel)
    plt.legend(loc='best')
    plt.grid(True)

# Cell
def plot_classifier_boundaries(X, y, clf):
    """
    Given features X and labels y along with classifier, plot decision boundaries in two dimensions.

    Args:
        X: feature array of shape (n_samples, n_features)
        y: label array of shape (n_samples)
    """

    h = .02  # step size in the mesh

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, alpha=1)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())