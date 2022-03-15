import time
import numpy as np
from .basic_factor_data.korean_market_factor_data import KoreanMarketFactorData
import OpenDartReader
from config.api_key import OPEN_DART_KEY
from const.market import KOREA_MARKET
import pandas as pd

condition = {
    'PBR': 1.5,
    'PER': 20,
    'DIV': 5.0
}

report_code = {
    "사업보고서": '11011',
    "반기보고서": '11012',
    "1분기보고서": '11013',
    "3분기보고서": '11014'
}

indicators = [
    '유동자산',
    '자산총계',
    '부채총계',
    '자본총계',
    '매출액',
    '매출총이익',
    '영업이익',
    '당기순이익',
    '영업활동현금흐름', '잉여현금흐름'
]



class Extract:

    def __init__(self):
        self.factor_data = KoreanMarketFactorData()
        pass

    def filter_low_pbr_and_per(self, market):
        """
        pbr under 1.5
        per under 20
        :param market:
        :return:
        """

        df = self.__get_data(self.factor_data, market)
        pbr_condition = df['PBR'] <= condition["PBR"]
        per_condition = df['PER'] <= condition["PER"]

        # df = self.__join_finance_data(df[df[pbr_condition & per_condition]])
        df = self.__join_finance_data(df[df["종목명"]=="삼성전자"])

        return df.sort_values(by=['PBR', 'PER'])

    def filter_high_div_and_dps(self, market):
        """
        div over 5 percent
        :param market:
        :return:
        """
        factor_data = KoreanMarketFactorData()

        df = self.__get_data(factor_data, market)
        div_condition = df['DIV'] >= condition["DIV"]

        return self.__join_dividend_data(
            df[div_condition].sort_values(by=['DIV', 'PBR', 'PER'], axis=0, ascending=False))

    def __join_finance_data(self, df):
        dart = OpenDartReader(OPEN_DART_KEY)
        pd.options.display.float_format = '{:.2f}'.format
        pd.set_option('display.max_columns', None)

        data = []

        for row in df.itertuples():
            print(f"extracting {row[2]}...")
            for year in [2020, 2021]:
                dt = self.__find_financial_indicator(row[1], year, indicators, dart)
                data += dt

            time.sleep(0.3)


        df_financial = pd.DataFrame(data, columns=["종목코드", "연도"] + indicators)
        df_financial.drop_duplicates(inplace=True)
        for indicator in indicators:
            df_financial[indicator] = df_financial[indicator].apply(self.__str_to_float)

        df_financial = self.__calculate_indicator(df_financial)

        return pd.merge(df, df_financial, left_on="종목코드", right_on="종목코드", how="outer")

    def __join_dividend_data(self, df):
        dart = OpenDartReader(OPEN_DART_KEY)
        pd.options.display.float_format = '{:.5f}'.format

        data = []
        for row in df.itertuples():
            print(f"extracting {row[2]}...")
            record = [row[1]]
            for year in [2020]:
                # 지정한 해의 전전기, 전기, 당기 3년치.
                lwfr_dividends, frmtrm_dividends, thstrm_dividends = self.__find_dividends(row[1], year, dart)
                record += [lwfr_dividends, frmtrm_dividends, thstrm_dividends]
            data.append(record)
            time.sleep(0.3)
        # print(data)
        df_dividend = pd.DataFrame(data, columns=["종목코드", "2019", "2020", "2021"])

        return pd.merge(df, df_dividend, left_on="종목코드", right_on="종목코드")

    def __get_data(self, factor_data, market):
        df = pd.DataFrame()
        if "KOSPI" == KOREA_MARKET[market]:
            df = factor_data.get_kospi_market_data()
        elif "KOSDAQ" == KOREA_MARKET[market]:
            df = factor_data.get_kosdaq_market_data()

        df = df.replace([0], np.nan)
        df = df.dropna(axis=0)

        return df

    def __find_financial_indicator(self, stock_name, year, indicators, dart):
        report = dart.finstate_all(stock_name, year)

        data = []
        record = []
        if report is None: #리포트가 없다면
            #당기, 전기, 전전기 값을 모두 없앰.
            for i in range(0, -3, -1):
                record = [stock_name, year+i]
                record.extend([np.nan] * len(indicators))
                data.append(record)
            return data

        else:
            report = report[report['account_nm'].isin(indicators)] ##해당 지표들로 필터링

            print(report['account_nm'] == '매출총이익')
            if sum(report['fs_nm'] == "연결재무제표") > 0:
                # 'fs_nm' 중에 연결재무제표가 있다면, 그것을 사용함.
                report = report.loc[report['fs_nm'] == "연결재무제표"]
            else:
                report = report.loc[report['fs_nm'] == '재무제표']

            #당기, 전기, 전전기
            for year, column in zip([year, year-1, year-2], ['thstrm_amount', 'frmtrm_amount', 'bfefrmtrm_amount']):
                record = [stock_name, year]
                print(report['account_nm'])
                for indicator in indicators:
                    if sum( report['account_nm'] == indicator )>0:
                        value = report.loc[report['account_nm'] == indicator, column].iloc[0]
                    else:
                        value = np.nan
                    record.append(value)
                data.append(record)



            return data

    def __calculate_indicator(self, df_finance):
        df_finance.sort_values(by = ['종목코드', '연도'], inplace=True, ascending=False)
        ## 부채 비율
        df_finance['부채비율'] = df_finance['부채총계'] / df_finance['자본총계'] * 100

        ###영업이익 / 매출액 / 당기순이익 증가율
        print(df_finance['영업이익'].iloc[0:])
        print("----")
        print(df_finance['영업이익'].iloc[1:])
        print("----")
        print(df_finance['영업이익'].iloc[:-1])
        print("----")

        df_finance['영업이익 증가율'] = (df_finance['영업이익'].diff(periods=-1) / df_finance['영업이익'].shift(-1)).fillna(0) * 100
        df_finance['매출액 증가율'] = (df_finance['매출액'].diff(periods=-1) / df_finance['매출액'].shift(-1)).fillna(0) * 100
        df_finance['당기순이익 증가율'] = (df_finance['당기순이익'].diff(periods=-1) / df_finance['당기순이익'].shift(-1)).fillna(0) * 100


        ###영업이익 / 매출액 / 당기순이익 증가 상태
        status = ['영업이익 상태', '매출액 상태', '당기순이익 상태']
        three_indicators = ['영업이익', '매출액', '당기순이익']

        for i in range(len(status)):
            df_finance[status[i]] = np.nan
            df_finance.loc[
                (df_finance[three_indicators[i]].iloc[0:] > 0) & (df_finance[three_indicators[i]].iloc[:-1] > 0), status[i]
            ] = "흑자 지속"
            df_finance.loc[
                (df_finance[three_indicators[i]].iloc[0:] <= 0) & (df_finance[three_indicators[i]].iloc[:-1] <= 0), status[i]
            ] = "적자 지속"
            df_finance.loc[
                (df_finance[three_indicators[i]].iloc[0:] > 0) & (df_finance[three_indicators[i]].iloc[:-1] <= 0), status[i]
            ] = "흑자 전환"
            df_finance.loc[
                (df_finance[three_indicators[i]].iloc[0:] <= 0) & (df_finance[three_indicators[i]].iloc[:-1] > 0), status[i]
            ] = "적자 전환"

        ### ROA
        df_finance['ROA'] = df_finance['당기순이익'] / df_finance['자산총계'] * 100
        ### ROE
        average_equity = df_finance['자본총계'].rolling(1).mean()
        df_finance['ROE'] = (df_finance['당기순이익'] / average_equity) * 100

        ### reindexing columns and return
        return df_finance.reindex(columns= [
                                      '종목코드', '연도', 'ROA', 'ROE'
                                  ] + indicators + [
                                      '부채비율',
            '영업이익 증가율',status[0],
            '매출액 증가율', status[1],
            '당기순이익 증가율', status[2]
                                  ]
                                  )

    def __find_dividends(self, stock_name, year, dart):
        stock_name_report = dart.report(stock_name, "배당", year, report_code["사업보고서"])
        if stock_name_report is None:
            return np.nan, np.nan, np.nan
        else:
            stock_name_report = stock_name_report.loc[(stock_name_report['se'] == '주당 현금배당금(원)')].iloc[0]

            thstrm_dividends = int(stock_name_report['thstrm'].replace('-', '0').replace(',', ''))
            frmtrm_dividends = int(stock_name_report['frmtrm'].replace('-', '0').replace(',', ''))
            lwfr_dividends = int((stock_name_report['lwfr'].replace('-', '0').replace(',', '')))

            return lwfr_dividends, frmtrm_dividends, thstrm_dividends

    def __str_to_float(self, value):
        if type(value) is float:
            return value
        elif value == '-':
            return 0
        else:
            return int(value.replace(',', ''))



