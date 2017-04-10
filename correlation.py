import data_util

import pandas as pd

import datetime


def get_common_dates_slice(df1, df2):
    common_dates = set(df1[data_util.KEY_DATE]) & set(df2[data_util.KEY_DATE])
    df1 = df1[df1[data_util.KEY_DATE].isin(common_dates)]
    df2 = df2[df2[data_util.KEY_DATE].isin(common_dates)]
    return df1, df2, common_dates


def get_correlation(df1: pd.DataFrame, df2: pd.DataFrame):
    df1, df2, common_dates = get_common_dates_slice(df1, df2)
    # print(len(common_dates))

    corrs = []

    if len(common_dates) == 0:
        return []

    min_year = min(common_dates, key=lambda x: x.year).year
    max_year = max(common_dates, key=lambda x: x.year).year

    for year in range(min_year, max_year + 1):
        df1_sliced = df1[
            df1[data_util.KEY_DATE].between(
                datetime.date(year=year, month=1, day=1),
                datetime.date(year=year, month=12, day=31))
        ]
        df2_sliced = df2[
            df2[data_util.KEY_DATE].between(
                datetime.date(year=year, month=1, day=1),
                datetime.date(year=year, month=12, day=31))
        ]
        # print(df1_sliced[data_util.KEY_OPEN_PRICE].max(), df1_sliced[data_util.KEY_OPEN_PRICE].min())
        # print(df2_sliced[data_util.KEY_OPEN_PRICE].max(), df2_sliced[data_util.KEY_OPEN_PRICE].min())

        df1_sliced = df1_sliced.sort_values(by=data_util.KEY_DATE)
        df2_sliced = df2_sliced.sort_values(by=data_util.KEY_DATE)

        prices1 = df1_sliced[data_util.KEY_OPEN_PRICE]
        prices2 = df2_sliced[data_util.KEY_OPEN_PRICE]
        prices1.reset_index(inplace=True, drop=True)
        prices2.reset_index(inplace=True, drop=True)

        # this is if for some reason all values were exactly the same e.g. due to insufficient dates in this year
        if len(prices1) <= 100 or len(prices2) <= 100 or min(prices1) == max(prices1) or min(prices2) == max(prices2):
            continue

        prices1 = (prices1 - prices1.min()) / (prices1.max() - prices1.min())
        prices2 = (prices2 - prices2.min()) / (prices2.max() - prices2.min())

        corrs.append((year, prices1.corr(prices2)))

    return corrs


def get_corr_with_lag(df1: pd.DataFrame, df2: pd.DataFrame, lag: datetime.timedelta):
    df1_orig = df1.copy(deep=True)
    df2_orig = df2.copy(deep=True)
    df2[data_util.KEY_DATE] = df2[data_util.KEY_DATE].apply(lambda date: date - lag)
    df1[data_util.KEY_DATE] = df1[data_util.KEY_DATE].apply(lambda date: date - lag)

    return get_correlation(df1, df2_orig), get_correlation(df1_orig, df2)


if __name__ == '__main__':
    prices1 = pd.Series(data=[1, 2, 3, 4, 5])
    prices2 = pd.Series(data=[1, 2, 3, 4, 5])
    prices1 = (prices1 - prices1.min()) / (prices1.max() - prices1.min())
    prices2 = (prices2 - prices2.min()) / (prices2.max() - prices2.min())

    print(prices1.corr(prices2))
