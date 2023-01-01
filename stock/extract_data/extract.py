import time
from datetime import datetime

import numpy as np
from requests.exceptions import SSLError

import stock.extract_data.krx_condition as CONDITION
from .basic_factor_data.korean_market_factor_data import KoreanMarketFactorData
import OpenDartReader
from config.api_key import OPEN_DART_KEY
import pandas as pd


class Extract:

    def __init__(self):
        self.factor_data = KoreanMarketFactorData()
        self.dart = OpenDartReader(OPEN_DART_KEY)  # config/api_key.py에서 api key의 설정이 필요함.
        self.report_code = [
            '11013',  # "1분기보고서":
            '11012',  # "반기보고서":
            '11014',  # "3분기보고서":
            '11011'  # "사업보고서"
        ]
        self.basic_columns = [
            "종목코드",
            "종목명",
            "업종",
            "종가",
            "시가총액",
            "거래량",
            "거래대금",
            "상장주식수",
            "BPS",
            "PER",
            "PBR",
            "EPS",
            "DIV",
            "DPS",
            "average_roe",
            "S-RIM 적정주가",
            "S-RIM -10%",
            "S-RIM -20%"
        ]

        self.indicators = [
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

        self.financial_column_header = ["종목코드", "연도", "시가총액", "분기"] + self.indicators

    def get_data(self):
        print(f"Getting data from KRX")
        pd.set_option('display.max_columns', None)

        df_kospi = self.factor_data.get_kospi_market_data()
        df_kosdaq = self.factor_data.get_kosdaq_market_data()
        s_rim_data = self.__extract_s_rim_data()

        df_kospi_kosdaq = self.__calculate_s_rim_data_per_marketcap(
            pd.merge(
                pd.concat([df_kospi, df_kosdaq]),
                s_rim_data,
                left_on="종목코드",
                right_on="종목코드"
            )
        )

        return df_kospi_kosdaq[self.basic_columns]

    def extract_finance_data(self, finance_years, df):
        pd.set_option('display.max_columns', None)

        pd.options.display.float_format = '{:.6f}'.format

        data = []

        count = 1
        for row in df.itertuples():
            print(f"extracting {count}/{len(df)} {row[2]}...")
            count += 1
            for year in finance_years:
                # calling finance data using OpenDartReader
                dt = self.__find_financial_indicator(row[1], year)
                data += dt

            # time.sleep(0.15)

        df_financial = pd.DataFrame(data, columns=self.financial_column_header)

        # calculating factor data
        df_financial = self.__calculate_indicator(df_financial)

        print("Join Data------------")
        return pd.merge(df, df_financial, left_on="종목코드", right_on="종목코드", how="outer")

    def __find_financial_indicator(self, stock_code, year):
        current_assets = [0, 0, 0, 0]  # 유동자산
        liabilities = [0, 0, 0, 0]  # 부채총계
        equity = [0, 0, 0, 0]  # 자본총계
        total_assets = [0, 0, 0, 0]  # 자산총계
        revenue = [0, 0, 0, 0]  # 매출액
        grossProfit = [0, 0, 0, 0]  # 매출총이익
        income = [0, 0, 0, 0]  # 영업이익
        net_income = [0, 0, 0, 0]  # 당기순이익
        cfo = [0, 0, 0, 0]  # 영업활동현금흐름
        # cfi = [0, 0, 0, 0]  # 투자활동현금흐름
        capex = [0, 0, 0, 0]  # 유형자산의 증가
        fcf = [0, 0, 0, 0]  # 잉여현금흐름 : 영업활동의흐름 - 유형자산의 증가

        market_cap = [0, 0, 0, 0]  # 시가 총액
        date_year = str(year)  # 년도 변수 지정
        quarter = 0  # 분기

        no_report_list = ['035420', '035720', '036570', '017670', '251270', '263750', '030200', '293490',
                          '112040', '259960', '032640', '180640', '058850']  # 매출총이익 계산 못하는 회사들

        data = []

        for j, report_name in enumerate(self.report_code):
            time.sleep(0.1)
            # 연결 재무제표 불러오기
            try:
                report = self.dart.finstate_all(stock_code, year, report_name, fs_div='CFS')
            except SSLError:  # 재시도
                report = self.dart.finstate_all(stock_code, year, report_name, fs_div='CFS')

            today = datetime.today().date()

            # 각 분기별 재무제표를 불러올때, 아직 안나왔다면 그냥 재무제표계산을 중단하기.
            if year == today.year:
                if report_name == "11012" and today.month < 7:  # 2분기
                    break
                if report_name == "11014" and today.month < 11:  # 3분기
                    break
                if report_name == "11011" and today.month <= 12:  # 4분기
                    break

            if report is None:  # 리포트가 없다면 반복문 종료하기
                continue

            else:
                # 조건들에 대해 추출하기
                condition1 = CONDITION.get_condition1(report)
                condition2 = CONDITION.get_condition2(report)
                condition3 = CONDITION.get_condition3(report)
                condition4 = CONDITION.get_condition4(report)
                condition5 = CONDITION.get_condition5(report)
                condition6 = CONDITION.get_condition6(report)
                condition7 = CONDITION.get_condition7(report)
                condition8 = CONDITION.get_condition8(report)
                # condition9 = CONDITION.get_condition9(report)
                condition10 = CONDITION.get_condition10(report)
                condition15 = CONDITION.get_condition15(report)

                # 유동자산
                current_assets[j] = self.__check_index_error(report, condition1)
                # 부채총계
                liabilities[j] = self.__check_index_error(report, condition2)
                # 자본총계
                equity[j] = self.__check_index_error(report, condition3)

                # 매출액 계산
                if stock_code == '003550':  # LG의 경우, 매출이 쪼개져있으므로 매출원가 + 매출총이익을 더한다.
                    revenue[j] = self.__check_index_error(report, CONDITION.get_condition11(report)) + \
                                 self.__check_index_error(report, condition5)
                else:
                    revenue[j] = self.__check_index_error(report, condition4)

                # 매출총이익 계산
                if stock_code == '011810':  # 매출총이익 항목이 없는 회사도 있다. 이 경우, 매출액 - 매출원가로 계산.
                    grossProfit[j] = revenue[j] - self.__check_index_error(report,
                                                                           CONDITION.get_condition11(report))
                elif stock_code == '008770':
                    grossProfit[j] = revenue[j] - self.__check_index_error(report,
                                                                           CONDITION.get_condition14(report))
                elif stock_code in no_report_list:  # 매출총이익도 없고 이를 계산할 매출원가도 없다.
                    grossProfit[j] = -1
                else:
                    grossProfit[j] = self.__check_index_error(report, condition5)

                # 매출총이익이 에러핸들링으로 인해서 -1인 경우.
                # 특히 IT 서비스 몇몇 기업의 경우 매출총이익항목이 별도로 없고 재료비 항목도 없다.
                # 이 경우에는 그냥 매출액을 매출총이익으로 넣어준다.
                # 예시로 네이버증권에서 NAVER 항목에 대해서 참조.
                if grossProfit[j] == -1:
                    grossProfit[j] = revenue[j]

                # 영업이익
                income[j] = self.__check_index_error(report, condition6)

                # 당기순이익
                if stock_code == '008600':  # 법인세 차감전 금액에서 법인세 비용을 차감
                    net_income[j] = self.__check_index_error(report, CONDITION.get_condition12(report)) \
                                    - self.__check_index_error(report, CONDITION.get_condition13(report))
                else:
                    net_income[j] = self.__check_index_error(report, condition7)

                # 영업활동 현금흐름
                cfo[j] = self.__check_index_error(report, condition8)
                # 투자활동 현금흐름
                # cfi[j] = self.__check_index_error(report, condition9)
                # 유형자산의 증가
                capex[j] = self.__check_index_error(report, condition15)
                # 자산총계
                total_assets[j] = self.__check_index_error(report, condition10)

                # 계정에서 자본과부채의 총계 등으로 표현되는 경우, 순수 자본총계를 구할 수가 없어서 에러핸들링이 됨.
                # 이때는 자산총계에서 부채총계를 뺴는 것으로 자본총계를 구해줄 수 있음.
                if equity[j] == -1:
                    equity[j] = total_assets[j] - liabilities[j]

                if report_name == '11013':  # 1분기
                    date_month = '03'
                    date_day = 31  # 일만 계산할꺼니까 이것만 숫자로 지정
                    quarter = 1

                elif report_name == '11012':  # 2분기
                    date_month = '06'
                    date_day = 30
                    cfo[j] = cfo[j] - cfo[j - 1]  # 현금흐름은 2분기부터 시작
                    # cfi[j] = cfi[j] - cfi[j - 1]  # 현금흐름은 2분기부터 시작
                    capex[j] = capex[j] - capex[j - 1]
                    quarter = 2

                elif report_name == '11014':  # 3분기
                    date_month = '09'
                    date_day = 30
                    cfo[j] = cfo[j] - (cfo[j - 1] + cfo[j - 2])
                    # cfi[j] = cfi[j] - (cfi[j - 1] + cfi[j - 2])
                    capex[j] = capex[j] - (capex[j - 1] + capex[j - 2])
                    quarter = 3

                else:  # 4분기. 1 ~ 3분기 데이터를 더한다음 사업보고서에서 빼야 함
                    date_month = '12'
                    date_day = 30
                    revenue[j] = revenue[j] - (revenue[0] + revenue[1] + revenue[2])
                    grossProfit[j] = grossProfit[j] - (grossProfit[0] + grossProfit[1] + grossProfit[2])
                    income[j] = income[j] - (income[0] + income[1] + income[2])
                    net_income[j] = net_income[j] - (net_income[0] + net_income[1] + net_income[2])
                    cfo[j] = cfo[j] - (cfo[j - 1] + cfo[j - 2] + cfo[j - 3])
                    # cfi[j] = cfi[j] - (cfi[j - 1] + cfi[j - 2] + cfo[j - 3])
                    capex[j] = capex[j] - (capex[j - 1] + capex[j - 2] + capex[j - 3])
                    quarter = 4

                # 잉여현금흐름 : 영업활동의흐름 - 유형자산의 증가
                fcf[j] = (cfo[j] - capex[j])

                # 날짜 계산
                date_day = self.__check_weekend(date_year, date_month, date_day)
                date = date_year + date_month + str(date_day).zfill(2)
                date_string = date_year + '-' + date_month + '-' + str(date_day).zfill(2)

                # 각 분기별 마지막 영업일의 시가총액
                market_cap_df = self.factor_data.stock.get_market_cap_by_date(date, date, stock_code)

                try:
                    market_cap[j] = market_cap_df.loc[date_string]["시가총액"]
                except KeyError:
                    print(market_cap_df)
                    market_cap[j] = 0

                # TODO
                # market_listed_shares[j] = market_cap_df.loc[path_string]["상장주식수"]

                # 각 데이터들을 순서대로 리스트를 만들어서 record변수에 저장한다.
                record = [stock_code, date_string, market_cap[j], quarter, current_assets[j], liabilities[j], equity[j],
                          total_assets[j],
                          revenue[j], grossProfit[j], income[j], net_income[j], cfo[j],
                          fcf[j]]

            # 각 사업보고서별로 계산한 데이터들을 data 변수에 차곡차곡 넣는다.
            data.append(record)
        return data

    def __calculate_indicator(self, df):
        """
        추출한 재무제표 데이터를 이용해서 팩터데이터 및 참고데이터들을 계산한다.
        :param df:
        :return Dataframe:
        """
        df.sort_values(by=['종목코드', '연도'], inplace=True)
        # print(df)

        # 분기별 PER
        df['분기 PER'] = np.nan
        # 분기별 PBR
        df['분기 PBR'] = np.nan
        df['분기 PEG'] = np.nan
        df['PGPR'] = np.nan
        df['PSR'] = np.nan
        df['GP/A'] = np.nan
        df['POR'] = np.nan
        df['PCR'] = np.nan
        df['PFCR'] = np.nan
        df['NCAV/MC'] = np.nan
        df['분기 ROE'] = np.nan

        three_indicators = ['매출액', '영업이익', '당기순이익']
        three_indicators_status = ['매출액 상태', '영업이익 상태', '당기순이익 상태']
        three_qoq_growth_indicators = ['QoQ 매출액 증가율', 'QoQ 영업이익 증가율', 'QoQ 당기순이익 증가율']
        three_yoy_growth_indicators = ['YoY 매출액 증가율', 'YoY 영업이익 증가율', 'YoY 당기순이익 증가율']

        df_temp = pd.DataFrame(columns=df.columns)

        # 전체 데이터들 중에 종목코드만 추출해서 배열로 만듦.
        corp_ticker = df.loc[:, ["종목코드"]].drop_duplicates().values.tolist()

        for row in corp_ticker:
            if row is None:
                continue
            print(f"Calculating {row[0]} factor indicators")
            # 종목코드별로 반복문이 실행됨.
            df_finance = df[df["종목코드"] == row[0]].reset_index()

            # 종목이 가진 데이터길이 만큼 반복. 3부터 시작하는 이유는, 4개분기 데이터로 계산하는 데이터때문에.
            # 과거 데이터를 참조해야하는데, 최초 3개 데이터까지는 참조할 데이터가 없음.
            for i in range(3, len(df_finance)):
                # PSR : 시가총액 / 매출액
                df_finance.loc[i, "PSR"] = self.__calculate_quarter_data(i, df_finance, three_indicators[0])
                # PGPR : 시가총액 / 매출총이익
                df_finance.loc[i, "PGPR"] = self.__calculate_quarter_data(i, df_finance, "매출총이익")
                # POR : 시가총액 / 영업이익
                df_finance.loc[i, "POR"] = self.__calculate_quarter_data(i, df_finance, three_indicators[1])
                # PER : 시가총액 / 당기 순이익
                df_finance.loc[i, "분기 PER"] = self.__calculate_quarter_data(i, df_finance, three_indicators[2])
                # PCR : 시가총액 / 영업활동 현금흐름
                df_finance.loc[i, "PCR"] = self.__calculate_quarter_data(i, df_finance, "영업활동현금흐름")
                # PFCR : 시가총액 / 잉여현금 흐름
                df_finance.loc[i, "PFCR"] = self.__calculate_quarter_data(i, df_finance, "잉여현금흐름")

                # ROE : 당기순이익 / 자본총계
                df_finance.loc[i, "분기 ROE"] = ((df_finance.iloc[i - 3][three_indicators[2]] +
                                                df_finance.iloc[i - 2][three_indicators[2]] +
                                                df_finance.iloc[i - 1][three_indicators[2]] +
                                                df_finance.iloc[i][three_indicators[2]]) /
                                               df_finance.iloc[i]['자본총계']) * 100

            # PBR : 시가총액 / 자본총계
            df_finance["분기 PBR"] = df_finance['시가총액'] / df_finance['자본총계']

            # GP/A : 최근 분기 매출총이익 / 자산총계
            df_finance["GP/A"] = (df_finance['매출총이익'] / df_finance['자산총계']) * 100

            # NCAV/MK : 청산가치(유동자산 - 부채총계) / 시가총액
            df_finance["NCAV/MC"] = (df_finance['유동자산'] - df_finance['부채총계']) / \
                                    df_finance['시가총액'] * 100

            # 부채 비율
            df_finance['부채비율'] = (df_finance['부채총계'] / df_finance['자본총계']) * 100

            # 분기별 매출액 / 영업이익 / 당기순이익 증가율
            for i in range(0, len(three_indicators)):
                s = df_finance[three_indicators[i]].shift()
                df_finance[three_qoq_growth_indicators[i]] = df_finance[three_indicators[i]].sub(s).div(s.abs()) * 100

            # 전년동기대비 매출액 / 영업이익 / 당기순이익 증가율
            for i in range(0, len(three_indicators)):
                s = df_finance.groupby('분기')[three_indicators[i]].shift()
                df_finance[three_yoy_growth_indicators[i]] = df_finance[three_indicators[i]].sub(s).div(s.abs()) * 100

            # PEG : PER / 당기순이익 증가율
            df_finance["분기 PEG"] = df_finance['분기 PER'] / df_finance[three_qoq_growth_indicators[2]]

            # 매출총이익률 / 영업이익률 / 당기순이익률
            df_finance['매출총이익률'] = (df_finance['매출총이익'] / df_finance[three_indicators[0]]) * 100
            df_finance['영업이익률'] = (df_finance[three_indicators[1]] / df_finance[three_indicators[0]]) * 100
            df_finance['당기순이익률'] = (df_finance[three_indicators[2]] / df_finance[three_indicators[0]]) * 100

            # 분기열 삭제
            df_finance.drop(['분기'], axis=1)

            # 정렬 순서를 다시 바꿈. 과거 -> 현재순으로.
            df_finance.sort_values(by=['연도'], inplace=True, ascending=False)

            # 매출액, 영업이익, 당기순이익 확인 지표
            # 이전 분기의 값과 비교하여 흑자인지 적자인지를 판단.
            for i in range(len(three_indicators_status)):
                df_finance[three_indicators_status[i]] = np.nan
                df_finance.loc[
                    (df_finance[three_indicators[i]] > 0) & (df_finance[three_indicators[i]].shift(-1) <= 0),
                    three_indicators_status[i]
                ] = "흑자 전환"
                df_finance.loc[
                    (df_finance[three_indicators[i]] <= 0) & (df_finance[three_indicators[i]].shift(-1) > 0),
                    three_indicators_status[i]
                ] = "적자 전환"
                df_finance.loc[
                    (df_finance[three_indicators[i]] > 0) & (df_finance[three_indicators[i]].shift(-1) > 0),
                    three_indicators_status[i]
                ] = "흑자 지속"
                df_finance.loc[
                    (df_finance[three_indicators[i]] <= 0) & (df_finance[three_indicators[i]].shift(-1) <= 0),
                    three_indicators_status[i]
                ] = "적자 지속"

            ## 기존 데이터프레임 하단에 종목별로 정제데이터들을 붙이기.
            df_temp = pd.concat([df_finance, df_temp])

        ### 데이터들의 헤더 순서를 다시 지정해준다.
        return df_temp.reindex(
            columns=[
                        '종목코드', '연도', '시가총액',
                        '분기 PBR', 'PSR', 'PGPR', 'POR', '분기 PER', '분기 PEG', 'PCR', 'PFCR',
                        '분기 ROE', 'GP/A', 'NCAV/MC'
                    ]
                    + self.indicators +
                    [
                        '부채비율', '매출총이익률', three_qoq_growth_indicators[0], three_yoy_growth_indicators[0],
                        three_indicators_status[0],
                        '영업이익률', three_qoq_growth_indicators[1], three_yoy_growth_indicators[1],
                        three_indicators_status[1],
                        '당기순이익률', three_qoq_growth_indicators[2], three_yoy_growth_indicators[2],
                        three_indicators_status[2]
                    ]

        )

    def __check_weekend(self, date_year, date_month, date_day):
        """
        주말인지 아닌지를 판단.
        :param date_year:
        :param date_month:
        :param date_day:
        :return:
        """
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
        """
        간혹가다가 리포트에서 값을 조회할 수 없는 회사들이 있음. 이럴때는 해당 컬럼값에 그냥 -1을 넣어주기로 에러 핸들링.
        :param report:
        :param condition:
        :return:
        """
        try:
            return int(report.loc[condition].iloc[0]['thstrm_amount'])
        except IndexError:
            return -1
        except ValueError:
            return -1

    def __calculate_quarter_data(self, index, df: pd.DataFrame, column_name):
        return df.iloc[index]["시가총액"] / (
                df.iloc[index - 3][column_name] + df.iloc[index - 2][column_name] +
                df.iloc[index - 1][column_name] + df.iloc[index][column_name])

    def __extract_s_rim_data(self):

        return pd.read_excel(
            "stock/crawling_data/net_worth_and_roe_list_for_s_rim.xlsx",
            usecols=["종목코드", "net_worth", "average_roe", "s-rim_value_1", "s-rim_value_2", "s-rim_value_3"],
            converters={"종목코드": str}
        )

    def __calculate_s_rim_data_per_marketcap(self, df_kospi_kosdaq: pd.DataFrame):
        for i in range(len(df_kospi_kosdaq.index.values.tolist())):
            df_kospi_kosdaq.loc[i, "S-RIM 적정주가"] = df_kospi_kosdaq.loc[i, "s-rim_value_1"] / df_kospi_kosdaq.loc[
                i, "상장주식수"]
            df_kospi_kosdaq.loc[i, "S-RIM -10%"] = df_kospi_kosdaq.loc[i, "s-rim_value_2"] / df_kospi_kosdaq.loc[
                i, "상장주식수"]
            df_kospi_kosdaq.loc[i, "S-RIM -20%"] = df_kospi_kosdaq.loc[i, "s-rim_value_3"] / df_kospi_kosdaq.loc[
                i, "상장주식수"]

        return df_kospi_kosdaq
