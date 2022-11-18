import numpy as np
import pandas as pd
import psycopg2
import copy
import matplotlib.pyplot as plt
from main import MF

# article: https://albertauyeung.github.io/2017/04/23/python-matrix-factorization.html/

R = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [1, 0, 0, 4],
    [0, 1, 5, 4],
])

select_query = "SELECT data.user_id, ARRAY_AGG( data.item_id ORDER BY data.user_id, data.item_id ) entities FROM (SELECT * FROM dataprocessing_items items JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id UNION ALL SELECT * FROM dataprocessing_items items JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id ) as data GROUP BY data.user_id ORDER BY data.user_id LIMIT 2 OFFSET 459";
all_entities_query = "SELECT id FROM public.dataprocessing_items ORDER BY id;"
unique_items = set()
user_data = {}
unique_users = []

try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="analytics_db")

    cursor = connection.cursor()
    cursor.execute(select_query)
    entities = cursor.fetchall()

    cursor.execute(all_entities_query)
    all_entities = cursor.fetchall()

    for idx, el in enumerate(all_entities):
        unique_items.add(el[0])

    for user_id, items in entities:
        unique_items.update(items)
        user_data[user_id] = items




except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)
finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

unique_items = sorted(unique_items)
R = np.zeros([len(user_data), len(unique_items)], dtype=np.float64)

for user, elems in user_data.items():
    res = []
    unique, counts = np.unique(elems, return_counts=True)
    user_data[user] = dict(zip(unique, counts))

for index, key in enumerate(user_data.keys()):
    unique_users.append(key)
    for elem_idx, elem in enumerate(unique_items):
        if elem in user_data[key]:
            R[index][elem_idx] = user_data[key][elem]

raw_R = copy.deepcopy(R)

mf = MF(R, K=2, alpha=0.15, beta=0.01, iterations=20)
training_process = mf.train()
print()
# print("P x Q:")
matrix = mf.full_matrix()
# print(mf.full_matrix())


k = 5

result = mf.full_matrix()
for row_idx, row in enumerate(result):
    print()
    x = row
    indices = np.argpartition(x, -k)[-k:]
    print("prediction for user", unique_users[row_idx])
    top_k = indices[np.argsort(x[indices])][::-1]
    res = map(lambda x: unique_items[x], top_k)
    print(list(res))


x = [x for x, y in training_process]
y = [y for x, y in training_process]
plt.figure(figsize=((16,4)))
plt.plot(x, y)
plt.xticks(x, x)
plt.xlabel("Iterations")
plt.ylabel("Mean Square Error")
plt.grid(axis="y")