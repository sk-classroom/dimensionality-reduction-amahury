# %%
import numpy as np
from scipy import sparse
from sklearn.datasets import make_blobs
from typing import Any

# TODO: implement the PCA with numpy
# Note that you are not allowed to use any existing PCA implementation from sklearn or other libraries.
class PrincipalComponentAnalysis:
    def __init__(self, n_components: int) -> None:
        """_summary_

        Parameters
        ----------
        n_components : int
            The number of principal components to be computed. This value should be less than or equal to the number of features in the dataset.
        """
        self.n_components = n_components
        self.components = None
        self.mean = None

    # TODO: implement the fit method
    def fit(self, X: np.ndarray):
        """
        Fit the model with X.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        self.mean = X.mean(axis=0)
        Xc = X - self.mean
        Cov = Xc.T @ Xc / (Xc.shape[0] - 1)
        w, self.components = np.linalg.eig(Cov)
        order = np.argsort(-w)[:self.n_components]
        w, self.components = w[order], self.components[:, order]
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Apply dimensionality reduction to X.

        X is projected on the first principal components previously extracted from a training set.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            New data, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        X_new : ndarray of shape (n_samples, n_components)
            Transformed values.
        """
        Xc = X - self.mean
        X_new = Xc @ self.components
        return X_new


# TODO: implement the LDA with numpy
# Note that you are not allowed to use any existing LDA implementation from sklearn or other libraries.
class LinearDiscriminantAnalysis:
    def __init__(self, n_components: int) -> None:
        self.n_components = n_components
        self.components = None
        self.mean = None

    def fit(self, X: np.ndarray, y: np.ndarray):
        """
        Fit the model according to the given training data.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Training data, where n_samples is the number of samples
            and n_features is the number of features.
        y : ndarray of shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
            Returns the instance itself.

        Hint:
        -----
        To implement LDA with numpy, follow these steps:
        1. Compute the mean vectors for each class.
        2. Compute the within-class scatter matrix.
        3. Compute the between-class scatter matrix.
        4. Compute the eigenvectors and corresponding eigenvalues for the scatter matrices.
        5. Sort the eigenvectors by decreasing eigenvalues and choose k eigenvectors with the largest eigenvalues to form a d×k dimensional matrix W.
        6. Use this d×k eigenvector matrix to transform the samples onto the new subspace.
        """
        ylab = np.unique(y)
        Sw = np.zeros((X.shape[1], X.shape[1]))  # Within class covariance
        Sb = np.zeros((X.shape[1], X.shape[1]))  # Between class covariance
        for yc in ylab:
            Xclass = X[y == yc]
            Sw += np.cov(Xclass.T)
            
        self.mean = X.mean(axis=0)
        for i, yc in enumerate(ylab):
            Xclass = X[y == yc]
            mc = Xclass.mean(axis=0)
            Sb += Xclass.shape[1] * (mc - self.mean) @ (mc - self.mean).T 
            
        w, self.components = sparse.linalg.eigs(Sb, M=Sw, k=self.n_components, which="LM")
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Apply dimensionality reduction to X.

        X is projected on the first principal components previously extracted from a training set.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            New data, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        X_new : ndarray of shape (n_samples, n_components)
            Transformed values.
        """
        Xc = X - self.mean
        X_new = Xc @ self.components
        return X_new


# TODO: Generating adversarial examples for PCA.
# We will generate adversarial examples for PCA. The adversarial examples are generated by creating two well-separated clusters in a 2D space. Then, we will apply PCA to the data and check if the clusters are still well-separated in the transformed space.
# Your task is to generate adversarial examples for PCA, in which
# the clusters are well-separated in the original space, but not in the PCA space. The separabilit of the clusters will be measured by the K-means clustering algorithm in the test script.
#
# Hint:
# - You can place the two clusters wherever you want in a 2D space.
# - For example, you can use `np.random.multivariate_normal` to generate the samples in a cluster. Repeat this process for both clusters and concatenate the samples to create a single dataset.
# - You can set any covariance matrix, mean, and number of samples for the clusters.
class AdversarialExamples:
    def __init__(self) -> None:
        pass

    def pca_adversarial_data(self, n_samples, n_features):
        """Generate adversarial examples for PCA

        Parameters
        ----------
        n_samples : int
            The number of samples to generate.
        n_features : int
            The number of features.

        Returns
        -------
        X: ndarray of shape (n_samples, n_features)
            Transformed values.

        y: ndarray of shape (n_samples,)
            Cluster IDs. y[i] is the cluster ID of the i-th sample.

        """
        X, y =  make_blobs(n_samples=n_samples, n_features=n_features, centers=5, random_state=42, center_box = (-5, 5), cluster_std = 0.5)
        return X, y
