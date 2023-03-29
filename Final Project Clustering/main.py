"""
reference:
    1. https://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_comparison.html
"""
import time
from matplotlib import pyplot as plt

from k_means import KMeans
from dbscan import DBSCAN
import utils

dataset = utils.get_dataset_list()


def dbscan_best(save=False):
    ds_param = [(0.26, 5), (0.35, 5), (0.4, 5), (0.65, 5), (0.55, 5), (0.30, 5)]
    plt.figure(figsize=(9, 6))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.05, top=0.92, wspace=0.05, hspace=0.13
    )

    _plt_num = 1
    for _ds_idx, (_x, _) in enumerate(dataset):
        _eps, _min_samples = ds_param[_ds_idx]
        plt.subplot(2, 3, _plt_num)

        t0 = time.time()
        _dbscan_obj = DBSCAN(eps=_eps, min_samples=_min_samples)
        _dbscan_obj.fit(x=_x)
        t1 = time.time()

        _t_predict = _dbscan_obj.get_labels()

        _t_colors = utils.get_colors_by_n_cluster(n_cluster=int(max(_t_predict) + 1))
        plt.scatter(_x[:, 0], _x[:, 1], s=10, color=_t_colors[_t_predict])

        # if _ds_idx == 0:
        #     plt.title(titles[_param_idx], size=18)
        # plt.xlim(-2.5, 2.5)
        # plt.ylim(-2.5, 2.5)
        plt.xlabel(r"$eps=%.2f, min\_sample=%d$" % (_eps, _min_samples), size=12)
        plt.xticks(())
        plt.yticks(())
        plt.text(
            0.99,
            0.01,
            ("%.2fs" % (t1 - t0)).lstrip("0"),
            transform=plt.gca().transAxes,
            size=15,
            horizontalalignment="right",
        )

        _plt_num += 1

    plt.suptitle(r"DBSCAN (best)", size=18)
    if save is False:
        plt.show()
    else:
        path = "plots/dbscan_best.png"
        plt.savefig(path, dpi=200)
        print("Saved to:", path)


def dbscan_param_eps(save=False):
    plt.figure(figsize=(9 * 2 + 3, 13))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.92, wspace=0.05, hspace=0.01
    )

    min_samples = 5
    eps_values = [0.15 + i * 0.05 for i in range(1, 11)]
    titles = ["$eps=%.2f$" % _eps for _eps in eps_values]
    params = [(_eps, min_samples) for _eps in eps_values]

    _plt_num = 1
    for _ds_idx, (_x, _) in enumerate(dataset):
        for _param_idx, (_eps, _min_samples) in enumerate(params):
            plt.subplot(len(dataset), len(params), _plt_num)

            t0 = time.time()
            _dbscan_obj = DBSCAN(eps=_eps, min_samples=_min_samples)
            _dbscan_obj.fit(x=_x)
            t1 = time.time()

            _t_predict = _dbscan_obj.get_labels()

            _t_colors = utils.get_colors_by_n_cluster(n_cluster=int(max(_t_predict) + 1))
            plt.scatter(_x[:, 0], _x[:, 1], s=10, color=_t_colors[_t_predict])

            if _ds_idx == 0:
                plt.title(titles[_param_idx], size=18)
            # plt.xlim(-2.5, 2.5)
            # plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(
                0.99,
                0.01,
                ("%.2fs" % (t1 - t0)).lstrip("0"),
                transform=plt.gca().transAxes,
                size=15,
                horizontalalignment="right",
            )

            _plt_num += 1

    plt.suptitle(r"DBSCAN ($min\_samples=%d$)" % min_samples, size=20)
    if save is False:
        plt.show()
    else:
        path = "plots/dbscan_param_eps.png"
        plt.savefig(path, dpi=200)
        print("Saved to:", path)


def dbscan_param_min_sample(save=False):
    plt.figure(figsize=(9 * 2 + 3, 13))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.92, wspace=0.05, hspace=0.01
    )

    min_samples_values = [5 + 2 * i for i in range(10)]
    eps = 0.3
    titles = [r"$min\_sample=%d$" % _min_samples for _min_samples in min_samples_values]
    params = [(eps, _min_samples) for _min_samples in min_samples_values]

    _plt_num = 1
    for _ds_idx, (_x, _) in enumerate(dataset):
        for _param_idx, (_eps, _min_samples) in enumerate(params):
            plt.subplot(len(dataset), len(params), _plt_num)

            t0 = time.time()
            _dbscan_obj = DBSCAN(eps=_eps, min_samples=_min_samples)
            _dbscan_obj.fit(x=_x)
            t1 = time.time()

            _t_predict = _dbscan_obj.get_labels()

            _t_colors = utils.get_colors_by_n_cluster(n_cluster=int(max(_t_predict) + 1))
            plt.scatter(_x[:, 0], _x[:, 1], s=10, color=_t_colors[_t_predict])

            if _ds_idx == 0:
                plt.title(titles[_param_idx], size=16)
            # plt.xlim(-2.5, 2.5)
            # plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(
                0.99,
                0.01,
                ("%.2fs" % (t1 - t0)).lstrip("0"),
                transform=plt.gca().transAxes,
                size=15,
                horizontalalignment="right",
            )

            _plt_num += 1

    plt.suptitle(r"DBSCAN ($eps=%.2f$)" % eps, size=20)
    if save is False:
        plt.show()
    else:
        path = "plots/dbscan_param_min_samples.png"
        plt.savefig(path, dpi=200)
        print("Saved to:", path)


def kmeans(save=False):
    plt.figure(figsize=(9 * 2 + 3, 13))
    plt.subplots_adjust(
        left=0.02, right=0.98, bottom=0.001, top=0.92, wspace=0.05, hspace=0.01
    )

    n_clusters_values = [1 + i for i in range(1, 11)]
    titles = [r"$n\_cluster=%d$" % _n_clusters for _n_clusters in n_clusters_values]
    params = [_n_clusters for _n_clusters in n_clusters_values]

    _plt_num = 1
    for _ds_idx, (_x, _) in enumerate(dataset):
        for _param_idx, _n_cluster in enumerate(params):
            plt.subplot(len(dataset), len(params), _plt_num)

            t0 = time.time()
            _dbscan_obj = KMeans(n_clusters=_n_cluster)
            _dbscan_obj.fit(x=_x)
            t1 = time.time()

            _t_predict = _dbscan_obj.get_labels()

            _t_colors = utils.get_colors_by_n_cluster(n_cluster=int(max(_t_predict) + 1))
            plt.scatter(_x[:, 0], _x[:, 1], s=10, color=_t_colors[_t_predict])

            if _ds_idx == 0:
                plt.title(titles[_param_idx], size=18)
            # plt.xlim(-2.5, 2.5)
            # plt.ylim(-2.5, 2.5)
            plt.xticks(())
            plt.yticks(())
            plt.text(
                0.99,
                0.01,
                ("%.2fs" % (t1 - t0)).lstrip("0"),
                transform=plt.gca().transAxes,
                size=15,
                horizontalalignment="right",
            )

            _plt_num += 1

    plt.suptitle(r"KMeans", size=20)
    if save is False:
        plt.show()
    else:
        path = "plots/kmeans.png"
        plt.savefig(path, dpi=200)
        print("Saved to:", path)


if "__main__" == __name__:
    pass
    dbscan_best(True)
    dbscan_param_eps(True)
    dbscan_param_min_sample(True)
    kmeans(True)
