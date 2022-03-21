import pandas as pd

def clean_ordenes(df):
    df.drop_duplicates(subset=["num_order", "item_id"],
                                  keep='first',
                                  inplace=True,
                                  ignore_index=False)
    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%d %H:%M:%S')
    return df

def histograma (df,df2):
    df["total"] = (
                (df["price"] * df["qty_ordered"]) * ((100 - df["discount_percent"])/100))
    df = df.merge(df2, how='left', left_on='product_id', right_on='product_id')
    df = df.groupby("analytic_category").sum()
    df.sort_values(by="total", axis=0, ascending=True, inplace=True)

    return df

def scatter (df,df2):
    df["total"] = (
                (df["price"] * df["qty_ordered"]) * ((100 - df["discount_percent"])/100))
    df = df.merge(df2, how='left', left_on='product_id', right_on='product_id')
    df["name"] = df["name"].astype(str)
    df['created_at'].dt.date
    return df

def scatter_acum (df):
    df['created_at'] = df['created_at'].dt.date
    df['Month'] = pd.DatetimeIndex(df['created_at']).month
    df['Year'] = pd.DatetimeIndex(df['created_at']).year
    df["period"] = df["Year"].astype(str) + str("/") + df["Month"].astype(str)
    df["period"] = pd.to_datetime(df["period"], format='%Y/%m')

    df = df.groupby("period").sum()

    return df

