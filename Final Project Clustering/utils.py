"""
reference:
    1. https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html
"""

from itertools import cycle, islice
import numpy as np
from sklearn import datasets
from matplotlib import pyplot as plt

np.random.seed(0)

# ============
# Generate datasets. We choose the size big enough to see the scalability
# of the algorithms, but not too big to avoid too long running times
# ============
n_samples = 500
noisy_circles = datasets.make_circles(n_samples=n_samples, factor=0.5, noise=0.05)
noisy_moons = datasets.make_moons(n_samples=n_samples, noise=0.05)
blobs = datasets.make_blobs(n_samples=n_samples, random_state=8)
no_structure = np.random.rand(n_samples, 2), None

# Anisotropicly distributed data
random_state = 170
X, y = datasets.make_blobs(n_samples=n_samples, random_state=random_state)
transformation = [[0.6, -0.6], [-0.4, 0.8]]
X_aniso = np.dot(X, transformation)
aniso = (X_aniso, y)

# blobs with varied variances
varied = datasets.make_blobs(
    n_samples=n_samples, cluster_std=[1.0, 2.5, 0.5], random_state=random_state
)

datasets = [
    noisy_circles,
    noisy_moons,
    varied,
    aniso,
    blobs,
    no_structure,
]

# ============
# Generate colors for clusters
# ============
colors = cycle(
    [
        "#377eb8",
        "#ff7f00",
        "#4daf4a",
        "#f781bf",
        "#a65628",
        "#984ea3",
        "#999999",
        "#e41a1c",
        "#dede00",
    ]
)


def get_dataset_list():
    return datasets


def get_colors_by_n_cluster(n_cluster: int) -> np.ndarray:
    res = np.array(
        list(
            islice(
                cycle(
                    [
                        "#377eb8",
                        "#ff7f00",
                        "#4daf4a",
                        "#f781bf",
                        "#a65628",
                        "#984ea3",
                        "#999999",
                        "#e41a1c",
                        "#dede00",
                    ]
                ),
                n_cluster,
            )
        )
    )
    # add black color for outliers (if any)
    res = np.append(res, ["#000000"])
    return res


def illustrate_datasets(save=False):
    dataset = get_dataset_list()
    titles = ["Noisy Circles", "Noisy Moons", "Blobs", "No Structure", "Anisotropicly", "Varied Blobs"]

    plt.figure(figsize=(9, 6))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.05, top=0.92, wspace=0.05, hspace=0.13
    )

    _plt_num = 1
    for _ds_idx, (_x, _gt) in enumerate(dataset):
        plt.subplot(2, 3, _plt_num)

        if _gt is None:
            _gt = np.full(len(_x), -1, dtype=int)
        _t_colors = get_colors_by_n_cluster(n_cluster=int(max(_gt) + 1))
        plt.scatter(_x[:, 0], _x[:, 1], s=10, color=_t_colors[_gt])

        # if _ds_idx == 0:
        #     plt.title(titles[_param_idx], size=18)
        # plt.xlim(-2.5, 2.5)
        # plt.ylim(-2.5, 2.5)
        plt.xlabel("%s" % titles[_ds_idx], size=12)
        plt.xticks(())
        plt.yticks(())

        _plt_num += 1

    plt.suptitle(r"Datasets", size=18)
    if save is False:
        plt.show()
    else:
        path = "plots/dataset.png"
        plt.savefig(path, dpi=200)
        print("Saved to:", path)


if "__main__" == __name__:
    illustrate_datasets(True)
