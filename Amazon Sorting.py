import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
#reading the dataset
df_ = pd.read_csv("datasets/amazon_review.csv")
df = df_.copy()
df.head(20)
df.describe().T
df["overall"].value_counts()
"""
Rating     Vote
5.00000    3922
4.00000     527
1.00000     244
3.00000     142
2.00000      80

"""

df.sort_values("day_diff", ascending = False).head(20)
df["overall"].mean()
#4.5875



#time based weighted average


#reaching and observing quantiles for variable "day_diff".
#%10,%25,%50,%75.
df["day_diff"].max()
a = df["day_diff"].quantile(0.10)
#167
b = df["day_diff"].quantile(0.25)
#281
c = df["day_diff"].quantile(0.50)
#431
d = df["day_diff"].quantile(0.75)
#601

df.loc[df["day_diff"] <= 167, "overall"].mean() * 30 / 100 + \
df.loc[(df["day_diff"] > a) & (df["day_diff"] <= b), "overall"].mean() * 21 / 100 + \
df.loc[(df["day_diff"] > b) & (df["day_diff"] <= c), "overall"].mean() * 19 / 100 + \
df.loc[(df["day_diff"] > c) & (df["day_diff"] <= d), "overall"].mean() * 17 / 100 + \
df.loc[(df["day_diff"] > d) & (df["day_diff"] <= 1064), "overall"].mean() * 13 / 100
#functionalizing
def time_weighted_average(dataframe,w1 = 30,w2 = 21 ,w3 = 19, w4 = 17 ,w5 = 13):
   return dataframe.loc[dataframe["day_diff"] <= 167, "overall"].mean() * w1 / 100 + \
    dataframe.loc[(dataframe["day_diff"] > a) & (dataframe["day_diff"] <= b), "overall"].mean() * w2 / 100 + \
    dataframe.loc[(dataframe["day_diff"] > b) & (dataframe["day_diff"] <= c), "overall"].mean() * w3 / 100 + \
    dataframe.loc[(dataframe["day_diff"] > c) & (dataframe["day_diff"] <= d), "overall"].mean() * w4 / 100 + \
    dataframe.loc[(dataframe["day_diff"] > d) & (dataframe["day_diff"] <= 1064), "overall"].mean() * w5 / 100
time_weighted_average(df)
#4.6299

#normal average was 4.5875 so we made a considerable difference by using time weighted average.



#User Review Based Average

#we should focus on "helpful_yes".
df["helpful_yes"].describe().T
df["helpful_yes"].unique()

df.groupby("overall").agg({"reviewText":"count"})

#let's create a variable for observing "thumbs down".
df["helpful_no"] = df["total_vote"] - df["helpful_yes"]
df.head()


#average rating by up/down

def up_down_average(x,y):
   if x + y == 0:
      return 0
    return  x / (x + y)

up_down_average(20, 15)

#up_down_average rating

df["up_down_ratio"] = df.apply(lambda x: up_down_average(x["helpful_yes"], x["helpful_no"]), axis=1)

df["up_down_ratio"].max()
df.sort_values("overall").head(20)


#wilson lower bound
"""
with wilson lower bound we'll sort the reviews better.
"lower bound of Wilson score confidence interval for a Bernoulli parameter provides a way to sort a product based on positive and negative ratings."
"""


def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p i??in hesaplanacak g??ven aral??????n??n alt s??n??r?? WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ??r??n s??ralamas?? i??in kullan??l??r.

    - Not:
    E??er skorlar 1-5 aras??ndaysa 1-3 negatif, 4-5 pozitif olarak i??aretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde baz?? problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)
df.sort_values("wilson_lower_bound", ascending=False).head(20)

#         reviewerID        asin                          reviewerName       helpful                                         reviewText  overall                                            summary  unixReviewTime  reviewTime  day_diff  helpful_yes  total_vote  helpful_no  up_down_ratio  wilson_lower_bound
#2031  A12B7ZMXFI6IXY  B007WTAJTO                  Hyoun Kim "Faluzure"  [1952, 2020]  [[ UPDATE - 6/19/2014 ]]So my lovely wife boug...  5.00000  UPDATED - Great w/ Galaxy S4 & Galaxy Tab 4 10...      1367366400  2013-01-05       702         1952        2020          68        0.96634             0.95754
#3449   AOEAD7DPLZE53  B007WTAJTO                     NLee the Engineer  [1428, 1505]  I have tested dozens of SDHC and micro-SDHC ca...  5.00000  Top of the class among all (budget-priced) mic...      1348617600  2012-09-26       803         1428        1505          77        0.94884             0.93652
#4212   AVBMZZAFEKO58  B007WTAJTO                           SkincareCEO  [1568, 1694]  NOTE:  please read the last update (scroll to ...  1.00000  1 Star reviews - Micro SDXC card unmounts itse...      1375660800  2013-05-08       579         1568        1694         126        0.92562             0.91214


