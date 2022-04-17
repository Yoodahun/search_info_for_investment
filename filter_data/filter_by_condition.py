import pandas as pd


def filtering_data_that_market_cap_under_thirty_percent(data: pd.DataFrame):
    """
    코스피, 코스닥의 종목에서 시가총액 30%이하의 종목으로 필터함.
    이 때, 기업소재지가 외국, 스팩주, 우선주, 최신거래일에 거래량이 0인 종목은 제거함.
    :param data:
    :return: DataFrame
    """

    # 외국 주식 드랍
    data.drop(
        data[data["종목코드"].str.startswith("9")].index,
        inplace=True
    )

    # 스팩 주식 드랍
    data.drop(
        data[data["종목명"].str.contains("스팩")].index,
        inplace=True
    )
    # 우선주 드랍
    data.drop(
        data[data["종목명"].str.endswith(("우", "우B", "우C"))].index,
        inplace=True
    )

    # 직전 거래일의 거래량이 0인 경우는 어떠한 이유에서 거래정지가 되어있을 확률이 높음
    data.drop(
        data[data["거래량"] == 0].index,
        inplace=True
    )
    return data[data["시가총액"] <= data["시가총액"].quantile(q=0.3)].sort_values(by=["시가총액"], ascending=True)


def filtering_low_pbr_and_per(pbr: float, per: float, df: pd.DataFrame):
    pbr_condition_1 = df['PBR'] >= 0.2
    pbr_condition_2 = df['PBR'] <= pbr
    per_condition_1 = df['PER'] > 0
    per_condition_2 = df['PER'] <= per

    df.drop(
        df[ df["연도"] != "2021-12-30"].index,
        inplace=True
    )

    df = df[ (pbr_condition_1 & pbr_condition_2)]
    df = df[(per_condition_1 & per_condition_2) ]

    return ("LOW_PBR_AND_PER",
            df.sort_values(by=['PER', 'PBR', '종목코드', '연도'], ascending=[True, True, False, False]).reset_index(drop=True)
            )


def filtering_low_pbr_and_high_gpa(pbr: float, df: pd.DataFrame):
    pbr_condition_1 = df['PBR'] >= 0.2
    pbr_condition_2 = df['PBR'] <= pbr
    per_condition_1 = df['PER'] > 0
    # gpa_condition = df['GP/A'].quantile(q=gpa)

    df.drop(
        df[ df["연도"] != "2021-12-30"].index,
        inplace=True
    )

    df = df[ (pbr_condition_1 & pbr_condition_2) & per_condition_1 ]

    return ("LOW_PBR_AND_HIGH_GPA",
            df.sort_values(by=['PBR', 'GP/A', '종목명', '연도'], ascending=[True, False, False, False]).reset_index(
                drop=True)
            )


def filtering_high_ncav_cap_and_gpa(df: pd.DataFrame):
    net_income_condition = df['당기순이익'] > 0
    liabilities_condition = df['부채비율'] < 200.0
    ncav_condition = df['NCAV/MK'] > 0.0

    df.drop(
        df[ df["연도"] != "2021-12-30"].index,
        inplace=True
    )

    df = df[ncav_condition & net_income_condition & liabilities_condition]
    return ("고NCAV_GPA_저부채비율",
            df.sort_values(by=['NCAV/MK', 'GP/A', '종목명', '연도'], ascending=[False, False, False, False]).reset_index(
                drop=True)
            )


def filtering_value_factor(df: pd.DataFrame):
    """
    PBR, PER, PCR, PSR의 합게 점수값이 낮은 순.
    :param df:
    :return:
    """
    df.drop(
        df[ df["연도"] != "2021-12-30"].index,
        inplace=True
    )

    df["PBR rank"] = df["PBR"].rank(ascending=True)
    df["PER rank"] = df["PER"].rank(ascending=True)
    df["PCR rank"] = df["PCR"].rank(ascending=True)
    df["PSR rank"] = df["PSR"].rank(ascending=True)

    df["4 Total Value score"] = df["PBR rank"] + df["PER rank"] + df["PCR rank"] + df["PSR rank"]

    return ("HIGH_SCORE_Four_value",
            df.sort_values(by=['4 Total Value score', '종목명', '연도'], ascending=[True, False, False]).reset_index(
                drop=True)
            )
