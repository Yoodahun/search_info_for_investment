import numpy as np

from . import factor_data
from .factor_data.korean_market_factor_data import KoreanMarketFactorData
from const.market import KOREA_MARKET
from pandas import DataFrame

condition = {
    'PBR': 1.5,
    'PER': 20,
    'DIV': 5.0
}


def low_pbr_and_per(market):
    """
    pbr under 1.5
    per under 20
    :param market:
    :return:
    """
    factor_data = KoreanMarketFactorData()

    df = __get_data(factor_data, market)
    pbr_condition = df['PBR'] <= condition["PBR"]
    per_condition = df['PER'] <= condition["PER"]

    return df[pbr_condition & per_condition].sort_values(by=['PBR', 'PER'])


def high_div_and_dps(market):
    """
    div over 5 percent
    :param market:
    :return:
    """
    factor_data = KoreanMarketFactorData()

    df = __get_data(factor_data, market)
    div_condition = df['DIV'] >= condition["DIV"]

    return df[div_condition].sort_values(by=['DIV','PBR', 'PER'], axis=0, ascending=False)


def __get_data(factor_data, market):
    df = DataFrame()
    if "KOSPI" == KOREA_MARKET[market]:
        df = factor_data.get_kospi_market_data()
    elif "KOSDAQ" == KOREA_MARKET[market]:
        df = factor_data.get_kosdaq_market_data()

    df = df.replace([0], np.nan)
    df = df.dropna(axis=0)

    return df
