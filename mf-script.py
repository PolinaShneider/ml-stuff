import random
import pandas as pd
import numpy as np

import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import MinMaxScaler
from als import implicit_als, implicit_als_cg

# -------------------------
# LOAD AND PREP THE DATA: https://medium.com/radon-dev/als-implicit-collaborative-filtering-5ed653ba39fe
# -------------------------

raw_data = pd.read_table('data/usersha1-artmbid-artname-plays.tsv')
# raw_data = raw_data.drop(raw_data.columns[1], axis=1)
raw_data.columns = ['user', 'artist', 'plays']

# Drop rows with missing values
data = raw_data.dropna()

# Convert artists names into numerical IDs
data['user_id'] = data['user'].astype("category").cat.codes
data['artist_id'] = data['artist'].astype("category").cat.codes

# Create a lookup frame so we can get the artist names back in
# readable form later.
item_lookup = data[['artist_id', 'artist']].drop_duplicates()
item_lookup['artist_id'] = item_lookup.artist_id.astype(str)

data = data.drop(['user', 'artist'], axis=1)

# Drop any rows that have 0 plays
data = data.loc[data.plays != 0]

# Create lists of all users, artists and plays
users = list(np.sort(data.user_id.unique()))
artists = list(np.sort(data.artist_id.unique()))
plays = list(data.plays)

# Get the rows and columns for our new matrix
rows = data.user_id.astype(int)
cols = data.artist_id.astype(int)

# Contruct a sparse matrix for our users and items containing number of plays
data_sparse = sparse.csr_matrix((plays, (rows, cols)), shape=(len(users), len(artists)))

# user_vecs, item_vecs = implicit_als(data_sparse, iterations=20, features=20, alpha_val=40)

alpha_val = 15
conf_data = (data_sparse * alpha_val).astype('double')
user_vecs, item_vecs = implicit_als_cg(conf_data, iterations=20, features=20)

# ------------------------------
# FIND SIMILAR ITEMS
# ------------------------------

# Let's find similar artists to Jay-Z.
# Note that this ID might be different for you if you're using
# the full dataset or if you've sliced it somehow.
item_id = 1

# Get the item row for Jay-Z
item_vec = item_vecs[item_id].T

# Calculate the similarity score between Mr Carter and other artists
# and select the top 10 most similar.
scores = item_vecs.dot(item_vec).toarray().reshape(1, -1)[0]
top_10 = np.argsort(scores)[::-1][:10]

artists = []
artist_scores = []

# Get and print the actual artists names and scores
for idx in top_10:
    artists.append(item_lookup.artist.loc[item_lookup.artist_id == str(idx)].iloc[0])
    artist_scores.append(scores[idx])

similar = pd.DataFrame({'artist': artists, 'score': artist_scores})

print('\n\nsimilar to item_id =', item_id, '\n\n', similar)

# Let's say we want to recommend artists for user with ID 2023
user_id = 3

# ------------------------------
# GET ITEMS CONSUMED BY USER
# ------------------------------

# Let's print out what the user has listened to
consumed_idx = data_sparse[user_id, :].nonzero()[1].astype(str)
consumed_items = item_lookup.loc[item_lookup.artist_id.isin(consumed_idx)]
print('\n\nconsumed_items by user_id =', user_id, '\n\n', consumed_items)


# ------------------------------
# CREATE USER RECOMMENDATIONS
# ------------------------------

def recommend(user_id, data_sparse, user_vecs, item_vecs, item_lookup, num_items=10):
    """Recommend items for a given user given a trained model

    Args:
        user_id (int): The id of the user we want to create recommendations for.

        data_sparse (csr_matrix): Our original training data.

        user_vecs (csr_matrix): The trained user x features vectors

        item_vecs (csr_matrix): The trained item x features vectors

        item_lookup (pandas.DataFrame): Used to map artist ids to artist names

        num_items (int): How many recommendations we want to return:

    Returns:
        recommendations (pandas.DataFrame): DataFrame with num_items artist names and scores

    """

    # Get all interactions by the user
    user_interactions = data_sparse[user_id, :].toarray()

    # We don't want to recommend items the user has consumed. So let's
    # set them all to 0 and the unknowns to 1.
    user_interactions = user_interactions.reshape(-1) + 1  # Reshape to turn into 1D array
    user_interactions[user_interactions > 1] = 0

    # This is where we calculate the recommendation by taking the
    # dot-product of the user vectors with the item vectors.
    rec_vector = user_vecs[user_id, :].dot(item_vecs.T).toarray()

    # Let's scale our scores between 0 and 1 to make it all easier to interpret.
    min_max = MinMaxScaler()
    rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1, 1))[:, 0]
    recommend_vector = user_interactions * rec_vector_scaled

    # Get all the artist indices in order of recommendations (descending) and
    # select only the top "num_items" items.
    item_idx = np.argsort(recommend_vector)[::-1][:num_items]

    artists = []
    scores = []

    # Loop through our recommended artist indicies and look up the actial artist name
    for idx in item_idx:
        artists.append(item_lookup.artist.loc[item_lookup.artist_id == str(idx)].iloc[0])
        scores.append(recommend_vector[idx])

    # Create a new dataframe with recommended artist names and scores
    recommendations = pd.DataFrame({'artist': artists, 'score': scores})

    return recommendations


# Let's generate and print our recommendations
recommendations = recommend(user_id, data_sparse, user_vecs, item_vecs, item_lookup)
print('\n\nrecommendations for user_id =', user_id, '\n\n', recommendations)




