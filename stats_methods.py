import numpy as np
from scipy import stats


class StatResult:
    def __init__(self, p0=0.05, **kwargs):
        self.method = kwargs['method']
        self.statistic = kwargs['statistic']
        self.p = kwargs['p']
        self.is_significant = self.p < p0
        self.size = kwargs['size']

    def __repr__(self):
        return "{method}\n N={size}\nStatistic={statistic}, P={p}, Significant difference? {sig}". \
            format(method=self.method, size=self.size, statistic=self.statistic, p=self.p, sig=self.is_significant)


def is_normal(*arrays):
    return stats.mstats.normaltest(np.concatenate(arrays))[1] > 0.05


def is_equal_variance(*arrays):
    return stats.levene(*arrays)[1] > 0.05


def paired_t(data1, data2):
    statistic, p = stats.ttest_rel(data1, data2)
    return StatResult(method='Paired t-test', statistic=statistic, p=p, size=(len(data1), len(data2)))


def two_comp(data1, data2):
    try:
        if is_normal(data1, data2) and is_equal_variance(data1, data2):
            statistic, p = stats.ttest_ind(data1, data2)
            method = 'Unpaired t-test'
        else:
            statistic, p = stats.mannwhitneyu(data1, data2)
            method = 'Mann-Whitney Rank Sum Test'
    except ValueError:
        statistic, p = stats.ttest_ind(data1, data2)
        method = 'Unpaired t-test'
    return StatResult(method=method, statistic=statistic, p=p, size=(len(data1), len(data2)))


def oneway(*data):
    try:
        if is_normal(*data) and is_equal_variance(*data):
            statistic, p = stats.f_oneway(*data)
            method = 'One-Way ANOVA'
        else:
            statistic, p = stats.kruskal(*data)
            method = 'One-Way ANOVA on Ranks'
    except ValueError:
        statistic, p = stats.f_oneway(*data)
        method = 'One-Way ANOVA'
    return StatResult(method=method, statistic=statistic, p=p, size=tuple(map(len, data)))


def tukey(*data):
    def get_s(x):
        return (len(x)-1)*(np.std(x) ** 2)

    from itertools import combinations
    from functools import reduce

    num_group = len(data)
    indexes = np.arange(num_group)
    ss = reduce(lambda x, y: x+y, map(get_s, data))
    df = reduce(lambda x, y: x+y, map(len, data)) - num_group
    print(ss, df)
    ms = ss/df
    print(ms)
    cbs = combinations(indexes, 2)


if __name__ == '__main__':
    x = [[5, 2, 5, 4, 2], [3, 3, 0, 2, 2], [1, 0, 1, 2, 1]]
    tukey(*x)
