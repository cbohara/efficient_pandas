import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

data = pd.read_csv('data/happy.csv', index_col=0)

data.sort_values(['Year', 'Happiness Score'], ascending=[True, False], inplace=True)


# describe() shows count, mean, min, max, std
# std measures how concentrated data is around the mean
# more concentrated = smaller std
data.describe()

# index = column to group by
# values = column to aggregate (defaults to mean aggregation)
year = pd.pivot_table(data, index='Year', values='Happiness Score')
region = pd.pivot_table(data, index='Region', values='Happiness Score')

# can specify other aggregate functions
sum_by_region = pd.pivot_table(data, index='Region', values='Happiness Score', aggfunc=[np.sum])

# pivot tables are useful for grouping by multiple columns
region_and_year = pd.pivot_table(data, index=['Region', 'Year'], values='Happiness Score')

# columns can be used as alternative to year as an alternative display
region_with_years_column = pd.pivot_table(data, index= 'Region', columns='Year', values='Happiness Score')
