import pandas as pd


def make_table(x):
    x['date'] = x['sleep']['dateOfSleep']
    x['type'] = x['sleep']['type']
    x['minutesAsleep'] = x['sleep']['minutesAsleep']
    return x


df = pd.read_json('postman_json/sleep-dateRange.json')
df = df.apply(make_table, axis=1)

# One series (sleep)
print(df.describe())
print(df.head(1))

print('hello')
