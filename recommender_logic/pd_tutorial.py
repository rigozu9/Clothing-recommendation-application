import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


s = pd.Series([1, 3, 5, np.nan, 6, 8])
# print(s)

dates = pd.date_range("20130101", periods=6)
# print(dates)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
# print(df)

df2 = pd.DataFrame(
    {
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    }
)
# print(df2)
# print(df2.dtypes)
# print(df.head(3))

# print(df.index)
# print(df.columns)

# print(df.to_numpy())

# print(df.describe())

# print(df.T)

# print(df.sort_index(axis=1, ascending=False))
# print(df.sort_values(by="B"))

# print(df["A"])
# print(df.A)

# print(df[["B", "A"]])

# print(df[1:2])

# print(df["20130102":"20130103"])

# print(df)
# print(df.loc[dates[1]])

# print(df.loc[:, ["A", "B"]])

# print(df.loc["20130102":"20130104", ["A", "B"]])

# print(df.loc[dates[0], "A"])
# print(df.at[dates[0], "A"])

# print(df)
# print(df.iloc[3])
# print(df.iloc[3:5, 0:2])
# print(df.iloc[[1, 2, 4], [0, 2]])
# print(df.iloc[1:3, :])
# print(df.iloc[:, 1:3])
# print(df.iloc[1, 1])

# print(df[df["A"] > 0])
# print(df[df > 0])

df2 = df.copy()
df2["E"] = ["one", "one", "two", "three", "four", "three"]
# print(df2)

# print(df2[df2["E"].isin(["two", "four"])])

s1 = pd.Series(
   [1, 2, 3, 4, 5, 6],
   index=pd.date_range("20130102", periods=6))

# print(s1)
df["F"] = s1
# print(df)

df.at[dates[0], "C"] = 0
# print(df)

df.iat[0, 1] = 0
# print(df)

df.loc[:, "D"] = np.array([5] * len(df))
# print(df)

df2 = df.copy()
df2[df2 > 0] = -df2
# print(df2)

df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ["E"])
df1.loc[dates[0] : dates[1], "E"] = 1
# print(df1)

# print(df1.dropna(how="any"))
# print(df1.fillna(value=5))
# print(pd.isna(df1))

# print(df.mean())
# print(df.mean(axis=1))

s = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates).shift(2)
# print(s)

# print(df.sub(s, axis="index"))

# print(df.agg(lambda x: np.mean(x) * 5.6))

# print(df.transform(lambda x: x * 101.2))

s = pd.Series(np.random.randint(0, 7, size=10))
# print(s)

# print(s.value_counts())

s = pd.Series(["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"])
# print(s.str.lower())

df = pd.DataFrame(np.random.randn(10, 4))
# print(df)

pieces = [df[:3], df[3:7], df[7:]]
# print(pieces)
# print(pd.concat(pieces))

left = pd.DataFrame({"key": ["foo", "foo"], "lval": [1, 2]})
right = pd.DataFrame({"key": ["foo", "foo"], "rval": [4, 5]})
# print(left)
# print(right)

# print(pd.merge(left, right, on="key"))

left = pd.DataFrame({"key": ["foo", "bar"], "lval": [1, 2]})
right = pd.DataFrame({"key": ["foo", "bar"], "rval": [4, 5]})
# print(left)
# print(right)

# print(pd.merge(left, right, on="key"))

df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)

# print(df)
# print(df.groupby("A")[["C", "D"]].sum())
# print(df.groupby(["A", "B"]).sum().shape)

arrays = [
   ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
   ["one", "two", "one", "two", "one", "two", "one", "two"],
]

index = pd.MultiIndex.from_arrays(arrays, names=["first", "second"])

df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=["A", "B"])

df2 = df[:4]

# print(df2)
stacked = df2.stack()
# print(stacked)
# print(stacked.unstack(0))

df = pd.DataFrame(
    {
        "A": ["one", "one", "two", "three"] * 3,
        "B": ["A", "B", "C"] * 4,
        "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 2,
        "D": np.random.randn(12),
        "E": np.random.randn(12),
    }
)

# print(df)
# print(pd.pivot_table(df, values="D", index=["A", "B"], columns=["C"]))

rng = pd.date_range("1/1/2012", periods=100, freq="s")

ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)

# print(ts.resample("5Min").sum())

rng = pd.date_range("3/6/2012 00:00", periods=5, freq="D")

ts = pd.Series(np.random.randn(len(rng)), rng)

# print(ts)

ts_utc = ts.tz_localize("UTC")

# print(ts_utc)

df = pd.DataFrame(
    {"id": [1, 2, 3, 4, 5, 6], "raw_grade": ["a", "b", "b", "a", "a", "e"]}
)

df["grade"] = df["raw_grade"].astype("category")

# print(df["grade"])

new_categories = ["very good", "good", "very bad"]

df["grade"] = df["grade"].cat.rename_categories(new_categories)
# print(df)

df["grade"] = df["grade"].cat.set_categories(
    ["very bad", "bad", "medium", "good", "very good"]
)

# print(df["grade"])
# print(df.sort_values(by="grade"))

# print(df.groupby("grade", observed=False).size())

plt.close("all")

ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
ts = ts.cumsum()
ts.plot()
# plt.show()

df = pd.DataFrame(
    np.random.randn(1000, 4), index=ts.index, columns=["A", "B", "C", "D"]
)

df = df.cumsum()

plt.figure()

df.plot()

plt.legend(loc='best')

# plt.show()

df = pd.DataFrame(np.random.randint(0, 5, (10, 5)))

# df.to_csv("foo.csv")

# print(pd.read_csv("foo.csv"))

df.to_excel("foo.xlsx", sheet_name="Sheet1")
# print(pd.read_excel("foo.xlsx", index_col=None, na_values=["NA"]))
