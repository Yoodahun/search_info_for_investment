from array import array
import pandas as pd

def filtering_transaction_amount(sheet_name, df:pd.DataFrame):
    df = df[df["거래금액"] <= 60000]

    return sheet_name, df.sort_values(by=["전용면적(평)"], ascending=False)