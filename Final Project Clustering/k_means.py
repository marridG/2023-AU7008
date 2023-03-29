"""
reference:
    1. https://scikit-learn.org/stable/modules/clustering.html#k-means
    2. https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
    3. https://towardsdatascience.com/k-means-clustering-introduction-to-machine-learning-algorithms-c96bf0d5d57a
    4. https://towardsdatascience.com/create-your-own-k-means-clustering-algorithm-in-python-d7d4c9077670
"""
import numpy as np
from matplotlib import pyplot as plt

import utils


class KMeans:
    def __init__(self, n_clusters: int = 10, max_iter: int = 300, tol: float = 1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tol = tol

        # fit result
        self.centroids = np.array([])
        self.fit_cgt = None  # None as default, fit as convergent otherwise
        self.fit_label_last = np.array([])

    @staticmethod
    def _cal_euclidean_dist(op_1: np.ndarray, op_2: np.ndarray) -> np.ndarray or float:
        """
        calculate the Euclidean distance between the two given vectors
        :param op_1:    (n_samples, n_features)
        :param op_2:    (n_samples, n_features)
        :return:        Euclidean distance (n_samples,)
        """
        # euclidean distance is equivalent to l-2 norm of `op_1 - op_2`
        res = np.linalg.norm(op_1 - op_2, axis=-1)
        return res

    @staticmethod
    def _cal_frobenius_norm(op_1: np.ndarray, op_2: np.ndarray) -> float:
        """
        calculate the Frobenius norm between the two given vectors
        :param op_1:    (n_samples, n_features)
        :param op_2:    (n_samples, n_features)
        :return:        Frobenius norm (n_samples,)
        """
        res = np.linalg.norm(op_1 - op_2, ord='fro')
        return res

    def fit(self, x: np.ndarray) -> None:
        """
        :param x: of shape (n_samples, n_features)
        """
        # randomize the centroids, within each feature
        x_min = np.min(x, axis=0)  # (n_features,)
        x_max = np.max(x, axis=0)  # (n_features,)
        self.centroids = np.array([
            np.random.uniform(low=x_min, high=x_max)
            for _ in range(self.n_clusters)
        ])  # (n_clusters, n_features)

        _crt_loss = 9999.999
        _crt_iter = 0
        while _crt_iter < self.max_iter and _crt_loss > self.tol:
            _crt_cluster_2_sample = [[] for _ in range(self.n_clusters)]
            _crt_sample_label = np.zeros(x.shape[0], dtype=int)

            # assign each item to the cluster which has the closest centroid
            for _x_idx, _x_sample in enumerate(x):
                _dist_2_centroids = self._cal_euclidean_dist(_x_sample, self.centroids)
                _best_centroid_idx = np.argmin(_dist_2_centroids)
                _crt_cluster_2_sample[_best_centroid_idx].append(_x_sample)
                _crt_sample_label[_x_idx] = _best_centroid_idx

            # calculate the new centroid, as mean on feature-dim, for each cluster
            _crt_centroids = np.zeros_like(self.centroids)
            for __cluster_idx in range(self.n_clusters):
                __cluster_samples = _crt_cluster_2_sample[__cluster_idx]
                if 0 == len(__cluster_samples):
                    continue
                _crt_centroids[__cluster_idx, :] = np.mean(
                    __cluster_samples, axis=0)  # (n_features, N) -> (n_features,)

            # calculate the Frobenius norm of the difference in the cluster centers of two consecutive iterations
            _crt_loss = self._cal_frobenius_norm(_crt_centroids, self.centroids)

            # update & prepare for the next iter
            self.fit_label_last = _crt_sample_label
            self.centroids = _crt_centroids
            _crt_iter += 1

        # handles end-of-training
        if _crt_iter >= self.max_iter:
            self.fit_cgt = False
        else:
            self.fit_cgt = True

    def get_labels(self) -> np.ndarray:
        assert self.fit_cgt is not None, "ERROR. Do Training First."
        return self.fit_label_last

    def predict(self, x: np.ndarray):
        raise NotImplemented


if "__main__" == __name__:
    t_all_datasets = utils.get_dataset_list()
    t_n_clusters = 2
    for _t_dataset_idx, (_t_x, _t_gt) in enumerate(t_all_datasets):
        _kmeans_obj = KMeans(n_clusters=t_n_clusters, max_iter=300, tol=1e-4)
        _kmeans_obj.fit(x=_t_x)
        _t_predict = _kmeans_obj.get_labels()
        _t_colors = utils.get_colors_by_n_cluster(n_cluster=t_n_clusters)
        plt.scatter(_t_x[:, 0], _t_x[:, 1], s=10, color=_t_colors[_t_predict])
        plt.show()
