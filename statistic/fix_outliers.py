import numpy as np


OX = np.array([1, 2, 3, 4, 5, 54, 6, -66, 7, 24, 8,  9,  10, 545, 2121])
OY = np.array([1, 2, 3, 4, 5, 6,  7, 8,   9, 10, 11, 12, 13, 14,  15])


def detect_outliers_by_iqr(data):
    q1 = np.percentile(data, 25, method='midpoint')
    q3 = np.percentile(data, 75, method='midpoint')
    iqr = q3 - q1
    return [idx for idx, d in enumerate(data) if (q3 + 1.5 * iqr) <= d or d <= (q1 - 1.5 * iqr)]


if __name__ == '__main__':

    outliers_indexes = detect_outliers_by_iqr(OX)
    print(outliers_indexes)

    # TODO: interpolate them

