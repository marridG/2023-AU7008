"""
reference:
    1. https://scikit-learn.org/stable/modules/clustering.html#dbscan
    2. https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN
    3. https://en.wikipedia.org/wiki/DBSCAN
    4. https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree
"""
import numpy as np
from sklearn.neighbors import KDTree
from matplotlib import pyplot as plt

import utils


class DBSCAN:
    _LABEL_INIT = -99
    _LABEL_NOISE = -1

    def __init__(self, eps: float = 0.5, min_samples: int = 5):
        self.eps = eps
        self.min_samples = min_samples

        # fit
        self._x = np.array([])  # (n_samples, n_features)
        self._x_kdtree = None
        self._crt_cluster_label = 0
        self._fit_labels = np.array([])  # (n_samples,)

    def _expand_neigh(self, sample_idx: int):
        """
        expand neighbours of the current sample
        :param sample_idx:      idx of the current sample
        """
        crt_sample = self._x[sample_idx, :]
        # Reshape your data  using:
        #   either `array.reshape(-1, 1)` if your data has a single feature
        #   or array.reshape(1, -1) if it contains a single sample
        crt_sample_reshaped = crt_sample.reshape(1, -1)
        # find all neighbours (within radius) of the current sample
        crt_neigh_idx = self._x_kdtree.query_radius(crt_sample_reshaped, r=self.eps)[0]  # (N,) of indices

        # if cnt_neigh thresh is NOT reached: mark the current sample as noise
        if self.min_samples > len(crt_neigh_idx):
            self._fit_labels[sample_idx] = self._LABEL_NOISE
            return

        # otherwise, create a new cluster with the current sample as seed
        _crt_neigh_idx_as_leaf = crt_neigh_idx[
            np.where(self._LABEL_NOISE == self._fit_labels[crt_neigh_idx])
        ]
        _crt_neigh_idx_as_unassigned_seed = crt_neigh_idx[
            np.where(self._LABEL_INIT == self._fit_labels[crt_neigh_idx])
        ]
        self._fit_labels[_crt_neigh_idx_as_leaf] = self._crt_cluster_label
        self._fit_labels[_crt_neigh_idx_as_unassigned_seed] = self._crt_cluster_label

        # recursively expand from each neighboring seed
        for _seed_idx in _crt_neigh_idx_as_unassigned_seed:
            self._expand_neigh(sample_idx=_seed_idx)

        # proceed to the nest seed
        self._crt_cluster_label += 1

    def fit(self, x: np.ndarray) -> None:
        """
        :param x: of shape (n_samples, n_features)
        """
        self._x = x
        self._fit_labels = np.full(x.shape[0], self._LABEL_INIT, dtype=int)
        self._x_kdtree = KDTree(x, leaf_size=30)

        _crt_cluster_label = 0
        for _crt_sample_idx, _crt_sample in enumerate(x):
            # skip assigned samples
            if self._LABEL_INIT != self._fit_labels[_crt_sample_idx]:
                continue

            # expand neighbours of the current sample
            self._expand_neigh(sample_idx=_crt_sample_idx)

        # noise is labeled -1, iff. -1 == self._LABEL_NOISE

    def get_labels(self) -> np.ndarray:
        assert self._x is not None, "ERROR. Do Training First."
        return self._fit_labels

    def predict(self, x: np.ndarray):
        raise NotImplemented


if "__main__" == __name__:
    t_all_datasets = utils.get_dataset_list()
    t_eps, t_min_samples = 0.25, 5
    for _t_dataset_idx, (_t_x, _t_gt) in enumerate(t_all_datasets):
        _dbscan_obj = DBSCAN(eps=t_eps, min_samples=t_min_samples)
        _dbscan_obj.fit(x=_t_x)
        _t_predict = _dbscan_obj.get_labels()
        _t_colors = utils.get_colors_by_n_cluster(n_cluster=int(max(_t_predict) + 1))
        plt.scatter(_t_x[:, 0], _t_x[:, 1], s=10, color=_t_colors[_t_predict])
        plt.show()
