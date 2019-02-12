import tushare as ts
from pandas import DataFrame
import datetime


class Market(object):
    token = "54efe7f2981634c22978029c817f9baf859c8b3a81c913da384445ae"
    pro = None

    def __init__(self):
        ts.set_token(self.token)
        self.pro = ts.pro_api()

    def get_online_data(self) -> list:
        today = datetime.datetime.now().strftime("%Y%m%d")
        if len(self.pro.trade_cal(exchange='', start_date=today, end_date=today, is_open="1")) == 0:
            return {}
        else:
            df: DataFrame = ts.get_today_all()
            df = df[["code",
                     "name",
                     "changepercent",
                     "trade",
                     "open",
                     "high",
                     "low",
                     "volume",
                     "turnoverratio",
                     "amount"]]
            df["trade"] = today
            return df.to_dict(orient="record")

    def get_daily_data(self, dt: str) -> list:
        if len(self.pro.trade_cal(exchange="", start_date=dt, end_date=dt, is_open="1")) == 0:
            return {}
        else:
            daily: DataFrame = self.pro.daily(trade_date=dt)
            adj: DataFrame = self.pro.adj_factor(ts_code="", trade_date=dt)
            df = daily.merge(adj, left_on=["ts_code", "trade_date"],
                             right_on=["ts_code", "trade_date"],
                             suffixes=("_x", "_y"), how="inner")
            df["code"] = [d[0:6] for d in df.ts_code]
            return df.to_dict(orient="record")

    def get_last_trade_day(self, dt: str) -> str:
        st = (datetime.datetime.strptime(dt, "%Y%m%d") + datetime.timedelta(days=-20)).strftime("%Y%m%d")
        df = self.pro.trade_cal(exchange='', start_date=st, end_date=dt, is_open="1")
        return list(df.cal_date)[-2]

    def get_trade_day(self, start: str, end: str) -> list:
        df = self.pro.trade_cal(exchange='', start_date=start, end_date=end, is_open="1")
        return list(df.cal_date)


if __name__ == '__main__':
    market = Market()
    print(len(market.get_daily_data("20190104")))  # 20170705
