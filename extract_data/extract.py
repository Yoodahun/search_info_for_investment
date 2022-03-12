import time
import numpy as np
from .factor_data.korean_market_factor_data import KoreanMarketFactorData
import OpenDartReader
from config.api_key import OPEN_DART_KEY
from const.market import KOREA_MARKET
import pandas as pd

condition = {
    'PBR': 1.5,
    'PER': 20,
    'DIV': 5.0
}


def filter_low_pbr_and_per(market):
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


def filter_high_div_and_dps(market):
    """
    div over 5 percent
    :param market:
    :return:
    """
    factor_data = KoreanMarketFactorData()

    df = __get_data(factor_data, market)
    div_condition = df['DIV'] >= condition["DIV"]

    return __join_dividend_data(df[div_condition].sort_values(by=['DIV', 'PBR', 'PER'], axis=0, ascending=False))


def __join_finance_data(df):
    dart = OpenDartReader(OPEN_DART_KEY)

    pass


def __join_dividend_data(df):
    dart = OpenDartReader(OPEN_DART_KEY)

    data = []
    for row in df.itertuples():

        record = [row[2]]
        for year in [2020]:
            # 지정한 해의 전전기, 전기, 당기 3년치.
            lwfr_dividends, frmtrm_dividends, thstrm_dividends = __find_dividends(row[2], year, dart)
            record += [lwfr_dividends, frmtrm_dividends, thstrm_dividends]
        data.append(record)
        time.sleep(0.3)

    df_dividend = pd.DataFrame(data, columns=["종목명", "2019", "2020", "2021"])

    return pd.merge(df, df_dividend, left_on="종목명", right_on="종목명")

def __get_data(factor_data, market):
    df = pd.DataFrame()
    if "KOSPI" == KOREA_MARKET[market]:
        df = factor_data.get_kospi_market_data()
    elif "KOSDAQ" == KOREA_MARKET[market]:
        df = factor_data.get_kosdaq_market_data()

    df = df.replace([0], np.nan)
    df = df.dropna(axis=0)

    return df


def __find_dividends(stock_name, year, dart):
    stock_name_report = dart.report(stock_name, "배당", year, "11011")
    if stock_name_report is None:
        return np.nan, np.nan, np.nan
    else:
        stock_name_report = stock_name_report.loc[(stock_name_report['se'] == '주당 현금배당금(원)')].iloc[0]

        thstrm_dividends = int(stock_name_report['thstrm'].replace('-', '0').replace(',', ''))
        frmtrm_dividends = int(stock_name_report['frmtrm'].replace('-', '0').replace(',', ''))
        lwfr_dividends = int((stock_name_report['lwfr'].replace('-', '0').replace(',', '')))

        return lwfr_dividends, frmtrm_dividends, thstrm_dividends
