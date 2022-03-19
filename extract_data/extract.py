import time
from datetime import datetime

import numpy as np
import extract_data.krx_condition as CONDITION
from .basic_factor_data.korean_market_factor_data import KoreanMarketFactorData
import OpenDartReader
from config.api_key import OPEN_DART_KEY
from const.market import KOREA_MARKET
import pandas as pd

condition = {
    'PBR': 1.0,
    'PER': 8,
    'DIV': 5.0
}

report_code = [
    '11013',  # "1분기보고서":
    '11012',  # "반기보고서":
    '11014',  # "3분기보고서":
    '11011'  # "사업보고서"
]

indicators = [
    '유동자산',
    '부채총계',
    '자본총계',
    '자산총계',
    '매출액',
    '매출총이익',
    '영업이익',
    '당기순이익',
    '영업활동현금흐름',
    '잉여현금흐름'
]

financial_column_header = ["종목코드", "연도", "시가총액", '유동자산', '부채총계', '자본총계', '자산총계', '매출액', '매출총이익', '영업이익',
                           '당기순이익', '영업활동현금흐름', '잉여현금흐름']


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

        df = self.__get_data(market)

        pbr_condition = df['PBR'] <= condition["PBR"]
        per_condition = df['PER'] <= condition["PER"]
        df = df[pbr_condition & per_condition]
        # df = df.drop(["PER", "PBR"], axis=1)
        print(f"Filtered {len(df)} companies")
        df.sort_values(by=['PER', 'PBR'])
        df = self.__join_finance_data(df)
        # df = self.__join_finance_data(df[df["종목명"] == "삼성전자"])

        # print(df)

        return df.sort_values(by=['PER','PBR','종목코드', '연도',])

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
        pd.set_option('display.max_columns', None)

        # print(df)
        dart = OpenDartReader(OPEN_DART_KEY)
        pd.options.display.float_format = '{:.2f}'.format

        data = []
        # print(df)

        for row in df.itertuples():
            print(f"extracting {row[2]}...")
            for year in [2020, 2021]:
                dt = self.__find_financial_indicator(row[1], year, dart)
                data += dt

            time.sleep(0.3)

        # print(data)
        df_financial = pd.DataFrame(data, columns=financial_column_header)
        df_financial.drop_duplicates(inplace=True)
        # for indicator in indicators:
        #     df_financial[indicator] = df_financial[indicator].apply(self.__str_to_float)

        # print(df_financial)

        df_financial = self.__calculate_indicator(df_financial)
        # df_financial = df_financial.drop(['시가총액'], axis=1)
        print("Join Data------------")
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

    def __get_data(self, market):
        df = pd.DataFrame()
        if "KOSPI" == KOREA_MARKET[market]:
            df = self.factor_data.get_kospi_market_data()
        elif "KOSDAQ" == KOREA_MARKET[market]:
            df = self.factor_data.get_kosdaq_market_data()

        df = df.replace([0], np.nan)
        df = df.dropna(axis=0)

        return df

    def __find_financial_indicator(self, stock_name, year, dart):
        current_assets = [0, 0, 0, 0]  # 유동자산
        liabilities = [0, 0, 0, 0]  # 부채총계
        equity = [0, 0, 0, 0]  # 자본총계
        total_assets = [0, 0, 0, 0]  # 자산총계
        revenue = [0, 0, 0, 0]  # 매출액
        grossProfit = [0, 0, 0, 0]  # 매출총이익
        income = [0, 0, 0, 0]  # 영업이익
        net_income = [0, 0, 0, 0]  # 당기순이익
        cfo = [0, 0, 0, 0]  # 영업활동현금흐름
        cfi = [0, 0, 0, 0]  # 투자활동현금흐름
        fcf = [0, 0, 0, 0]  # 잉여현금흐름 : 편의상 영업활동 - 투자활동 현금흐름으로 계산
        market_cap = [0, 0, 0, 0]
        market_listed_shares = [0, 0, 0, 0]
        date_year = str(year)  # 년도 변수 지정

        nogp_list = ['035420', '035720', '036570', '017670', '251270', '263750', '030200', '293490',
                     '112040', '259960', '032640', '180640', '058850']  # 매출총이익 계산 못하는 회사들

        data = []
        record = []

        for j, report_name in enumerate(report_code):
            report = dart.finstate_all(stock_name, year, report_name, fs_div='CFS')

            if report is None:  # 리포트가 없다면
                pass

            else:
                condition1 = CONDITION.get_condition1(report)
                condition2 = CONDITION.get_condition2(report)
                condition3 = CONDITION.get_condition3(report)
                condition4 = CONDITION.get_condition4(report)
                condition5 = CONDITION.get_condition5(report)
                condition6 = CONDITION.get_condition6(report)
                condition7 = CONDITION.get_condition7(report)
                condition8 = CONDITION.get_condition8(report)
                condition9 = CONDITION.get_condition9(report)
                condition10 = CONDITION.get_condition10(report)

                current_assets[j] = self.__get_condition_value(report, condition1)
                liabilities[j] = self.__get_condition_value(report, condition2)
                equity[j] = self.__check_index_error(report, condition3)

                try:
                    if stock_name == '003550':  # LG의 경우, 매출이 쪼개져있으므로 매출원가 + 매출총이익을 더한다.
                        revenue[j] = self.__get_condition_value(report, CONDITION.get_condition11(report)) + \
                                     self.__get_condition_value(report, condition5)
                    else:
                        revenue[j] = self.__get_condition_value(report, condition4)
                except IndexError:
                    revenue[j] = 1

                try:
                    if stock_name == '011810':  # 매출총이익 항목이 없는 회사도 있다. 이 경우, 매출액 - 매출원가로 계산.
                        grossProfit[j] = revenue[j] - self.__get_condition_value(report,
                                                                                 CONDITION.get_condition11(report))
                    elif stock_name in nogp_list:  # 매출총이익도 없고 이를 계산할 매출원가도 없다.
                        grossProfit[j] = 1
                    elif stock_name == '008770':
                        grossProfit[j] = revenue[j] - self.__get_condition_value(report,
                                                                                 CONDITION.get_condition14(report))
                    else:
                        grossProfit[j] = self.__get_condition_value(report, condition5)

                except IndexError:
                    grossProfit[j] = 1

                income[j] = self.__check_index_error(report, condition6)
                if stock_name == '008600':
                    net_income[j] = self.__get_condition_value(report, CONDITION.get_condition12(
                        report)) - self.__get_condition_value(report, CONDITION.get_condition13(report))
                else:
                    net_income[j] = self.__check_index_error(report, condition7)

                cfo[j] = self.__check_index_error(report, condition8)
                cfi[j] = self.__check_index_error(report, condition9)
                total_assets[j] = self.__check_index_error(report, condition10)

                if report_name == '11013':  # 1분기
                    date_month = '03'
                    date_day = 31  # 일만 계산할꺼니까 이것만 숫자로 지정

                elif report_name == '11012':  # 2분기
                    date_month = '06'
                    date_day = 30
                    cfo[j] = cfo[j] - cfo[j - 1]  # 현금흐름은 2분기부터 시작
                    cfi[j] = cfi[j] - cfi[j - 1]  # 현금흐름은 2분기부터 시작

                elif report_name == '11014':  # 3분기
                    date_month = '09'
                    date_day = 30
                    cfo[j] = cfo[j] - (cfo[j - 1] + cfo[j - 2])
                    cfi[j] = cfi[j] - (cfi[j - 1] + cfi[j - 2])

                else:  # 4분기. 1 ~ 3분기 데이터를 더한다음 사업보고서에서 빼야 함
                    date_month = '12'
                    date_day = 30
                    revenue[j] = revenue[j] - (revenue[0] + revenue[1] + revenue[2])
                    grossProfit[j] = grossProfit[j] - (grossProfit[0] + grossProfit[1] + grossProfit[2])
                    income[j] = income[j] - (income[0] + income[1] + income[2])
                    net_income[j] = net_income[j] - (net_income[0] + net_income[1] + net_income[2])
                    cfo[j] = cfo[j] - (cfo[j - 1] + cfo[j - 2] + cfo[j - 3])
                    cfi[j] = cfi[j] - (cfi[j - 1] + cfi[j - 2] + cfo[j - 3])
                    fcf[j] = fcf[j] - (fcf[0] + fcf[1] + fcf[2])

                date_day = self.__check_weekend(date_year, date_month, date_day)
                date = date_year + date_month + str(date_day)
                path_string = date_year + '-' + date_month + '-' + str(date_day)
                fcf[j] = (cfo[j] - cfi[j])
                market_cap_df = self.factor_data.stock.get_market_cap_by_date(date, date, stock_name)
                market_cap[j] = market_cap_df.loc[path_string]["시가총액"]
                # market_listed_shares[j] = market_cap_df.loc[path_string]["상장주식수"]

                record = [stock_name, path_string, market_cap[j], current_assets[j], liabilities[j], equity[j],
                          total_assets[j],
                          revenue[j], grossProfit[j], income[j], net_income[j], cfo[j],
                          fcf[j]]
            data.append(record)
        return data

    def __calculate_indicator(self, df):
        df.sort_values(by=['종목코드', '연도'], inplace=True)
        print(df)
        df['PER'] = np.nan
        df['PBR'] = np.nan
        df['PSR'] = np.nan
        df['GP/A'] = np.nan
        df['POR'] = np.nan
        df['PCR'] = np.nan
        df['PFCR'] = np.nan
        df['NCAV/MK'] = np.nan

        status = ['영업이익 상태', '매출액 상태', '당기순이익 상태']
        three_indicators = ['영업이익', '매출액', '당기순이익']

        df_temp = pd.DataFrame(columns=df.columns)

        corp_ticker = df.loc[:,["종목코드"]].drop_duplicates().values.tolist()

        for row in corp_ticker:
            if row is None:
                continue
            print(f"Calculating {row[0]} factor indicators" )
            df_finance = df[df["종목코드"] == row[0]].reset_index()

            # print(df_finance)

            for i in range(3, len(df_finance)):
                # print(df_finance)
                # print(df_finance.iloc[i])
                df_finance.loc[i,"PER"] = df_finance.iloc[i]['시가총액'] / (
                            df_finance.iloc[i - 3]['당기순이익'] + df_finance.iloc[i - 2]['당기순이익'] +
                            df_finance.iloc[i - 1]['당기순이익'] + df_finance.iloc[i]['당기순이익'])
                df_finance.loc[i, "PBR"] = df_finance.iloc[i]['시가총액'] / df_finance.iloc[i]['부채총계']
                df_finance.loc[i, "PSR"] = df_finance.iloc[i]['시가총액'] / (
                            df_finance.iloc[i - 3]['매출액'] + df_finance.iloc[i - 2]['매출액'] +
                            df_finance.iloc[i - 1]['매출액'] + df_finance.iloc[i]['매출액'])
                df_finance.loc[i, "GP/A"] = (df_finance.iloc[i - 3]['매출총이익'] + df_finance.iloc[i - 2]['매출총이익'] +
                                                 df_finance.iloc[i - 1]['매출총이익'] + df_finance.iloc[i]['매출총이익']) / \
                                                df_finance.iloc[i]['자산총계']
                df_finance.loc[i, "POR"] = df_finance.iloc[i]['시가총액'] / (
                            df_finance.iloc[i - 3]['영업이익'] + df_finance.iloc[i - 2]['영업이익'] +
                            df_finance.iloc[i - 1]['영업이익'] + df_finance.iloc[i]['영업이익'])
                df_finance.loc[i, "PCR"] = df_finance.iloc[i]['시가총액'] / (
                        df_finance.iloc[i - 3]['영업활동현금흐름'] + df_finance.iloc[i - 2]['영업활동현금흐름'] +
                        df_finance.iloc[i - 1]['영업활동현금흐름'] + df_finance.iloc[i]['영업활동현금흐름'])
                df_finance.loc[i, "PFCR"] = df_finance.iloc[i]['시가총액'] / (
                            df_finance.iloc[i - 3]['잉여현금흐름'] + df_finance.iloc[i - 2]['잉여현금흐름'] +
                            df_finance.iloc[i - 1]['잉여현금흐름'] + df_finance.iloc[i]['잉여현금흐름'])
                df_finance.loc[i, "NCAV/MK"] = (df_finance.iloc[i]['유동자산'] - df_finance.iloc[i]['부채총계']) / \
                                                   df_finance.iloc[i]['시가총액']

            # df_finance.sort_values(by=['연도'], inplace=True, ascending=False)
            ## 부채 비율
            df_finance['부채비율'] = (df_finance['부채총계'] / df_finance['자본총계']) * 100

            ###영업이익 / 매출액 / 당기순이익 증가율
            df_finance['영업이익 증가율'] = (df_finance['영업이익'].diff() / df_finance['영업이익'].shift(1)).fillna(
                0) * 100
            df_finance['매출액 증가율'] = (df_finance['매출액'].diff() / df_finance['매출액'].shift(1)).fillna(0) * 100
            df_finance['당기순이익 증가율'] = (df_finance['당기순이익'].diff() / df_finance['당기순이익'].shift(1)).fillna(
                0) * 100

            df_finance.sort_values(by=['연도'], inplace=True, ascending=False)

            for i in range(len(status)):
                df_finance[status[i]] = np.nan

                df_finance.loc[
                    (df_finance[three_indicators[i]].iloc[0:] > 0) & (df_finance[three_indicators[i]].iloc[:-1] > 0),
                    status[i]
                ] = "흑자 지속"
                df_finance.loc[
                    (df_finance[three_indicators[i]].iloc[0:] <= 0) & (df_finance[three_indicators[i]].iloc[:-1] <= 0),
                    status[i]
                ] = "적자 지속"
                df_finance.loc[
                    (df_finance[three_indicators[i]].iloc[0:] > 0) & (df_finance[three_indicators[i]].iloc[:-1] <= 0),
                    status[i]
                ] = "흑자 전환"
                df_finance.loc[
                    (df_finance[three_indicators[i]].iloc[0:] <= 0) & (df_finance[three_indicators[i]].iloc[:-1] > 0),
                    status[i]
                ] = "적자 전환"

            # print("-------------")
            # print(df_temp)
            df_temp = pd.concat([df_finance, df_temp])

        ### reindexing columns and return
        return df_temp.reindex(
            columns=['종목코드', '연도', '시가총액', 'PER', 'PBR', 'PSR', 'GP/A', 'POR', 'PCR', 'PFCR', 'NCAV/MK']
                    + indicators
                    + ['부채비율', '영업이익 증가율', status[0], '매출액 증가율', status[1], '당기순이익 증가율', status[2]]
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

    def __get_condition_value(self, report, condition):

        return int(report.loc[condition].iloc[0]['thstrm_amount'])

    def __check_weekend(self, date_year, date_month, date_day):
        date = date_year + date_month + str(date_day)
        date_formated = datetime.strptime(date, "%Y%m%d")  # datetime format 으로 변환

        if date_formated.weekday() == 5:
            if date_month == '12':
                date_day -= 2  # 연말의 경우 2일을 뺀다.
            else:
                date_day -= 1  # 토요일일 경우 1일을 뺀다.
        elif date_formated.weekday() == 6:
            if date_month == '12':
                date_day -= 3  # 연말의 경우 3일을 뺀다.
            else:
                date_day -= 2  # 일요일일 경우 2일을 뺀다.
        elif date_formated.weekday() == 4 and date_month == '12':
            date_day -= 1  # 연말인데 금요일이면 1일을 뺀다.

        # 추석에 대한 처리
        if date_month == '09' and date_year == '2020':
            date_day -= 1
        elif date_month == '09' and date_year == '2023':
            date_day -= 3

        return date_day

    def __check_index_error(self, report, condition):
        try:
            return self.__get_condition_value(report, condition)
        except IndexError:
            return 1
        except ValueError:
            return 1
