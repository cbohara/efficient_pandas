import pandas as pd

pd.set_option('display.max_columns', None)

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('data/users.dat', sep='::', header=None, names=unames, engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('data/ratings.dat', sep='::', header=None, names=rnames, engine='python')

mnames = ['movie_id', 'title', 'genre']
movies = pd.read_table('data/movies.dat', sep='::', header=None, names=mnames, engine='python')

# pandas infers which columns to use as the merge (or join) keys based on overlapping names
data = pd.merge(pd.merge(ratings, users), movies)

# index = groupby
# columns = aggregate by gender
# calculate the mean rating for each title by gender
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')

# filter out movies with less than 250 reviews
# first generate series with key as title and value as number of reviews
ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title.index[ratings_by_title >= 250]

# select rows on the index
mean_ratings = mean_ratings.loc[active_titles]

# sort by the female column in desc order
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)

# find the greatest difference between male and female ratings for a movie
mean_ratings['diff'] = abs(mean_ratings['M'] - mean_ratings['F'])
gender_diff = mean_ratings.sort_values(by='title')

gender_diff.to_csv('data/gender_diff.csv')