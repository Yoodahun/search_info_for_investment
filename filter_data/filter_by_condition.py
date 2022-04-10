import pandas as pd


def filtering_data_that_market_cap_under_thirty_percent(data: pd.DataFrame):
    """
    코스피, 코스닥의 종목에서 시가총액 30%이하의 종목으로 필터함.
    이 때, 스팩주, 우선주, 최신거래일에 거래량이 0인 종목은 제거함.
    :param data:
    :return: DataFrame
    """

    # 스팩 주식 드랍
    data.drop(
        data[data["종목명"].str.contains("스팩")].index,
        inplace=True
    )
    #우선주 드랍
    data.drop(
        data[data["종목명"].str.endswith(("우", "우B", "우C"))].index,
        inplace=True
    )

    #거래량이 0인 경우는 어떠한 이유에서 거래정지가 되어있을 확률이 높음
    data.drop(
        data[data["거래량"] == 0].index,
        inplace=True
    )
    return data[data["시가총액"] <= data["시가총액"].quantile(q=0.3)].sort_values(by=["시가총액"], ascending=True)
