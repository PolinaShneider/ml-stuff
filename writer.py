import csv
import psycopg2
import numpy as np

select_query = "SELECT data.user_id, ARRAY_AGG( data.item_id ORDER BY data.user_id, data.item_id ) entities FROM (SELECT * FROM dataprocessing_items items JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id UNION ALL SELECT * FROM dataprocessing_items items JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id ) as data GROUP BY data.user_id ORDER BY data.user_id";
# select_query = "SELECT data.user_id, ARRAY_AGG(data.item_id ORDER BY data.user_id, data.item_id) entities FROM (SELECT * FROM dataprocessing_items items JOIN workprogramsapp_prerequisitesofworkprogram prerequisites on items.id = prerequisites.workprogram_id JOIN workprogramsapp_workprogram program on program.id = prerequisites.workprogram_id JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id JOIN dataprocessing_user users on editors.user_id = users.id WHERE last_name like '%' || authors || '%' UNION ALL SELECT * FROM dataprocessing_items items JOIN workprogramsapp_outcomesofworkprogram outcomes on items.id = outcomes.item_id JOIN workprogramsapp_workprogram program on program.id = outcomes.workprogram_id JOIN workprogramsapp_workprogram_editors editors on program.id = editors.workprogram_id JOIN dataprocessing_user users on editors.user_id = users.id WHERE last_name like '%' || authors || '%' ) as data GROUP BY data.user_id ORDER BY data.user_id"

unique_items = set()
user_data = {}

try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="analytics_db")

    cursor = connection.cursor()
    cursor.execute(select_query)
    entities = cursor.fetchall()
    print("Selecting rows from mobile table using cursor.fetchall")
    vector = {}
    all_features = set()

    print("Print each row and it's columns values")
    for row in entities:
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

with open('./data/output.tsv', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['user', 'entity', 'count'])
    for user, elems in user_data.items():
        res = []
        unique, counts = np.unique(elems, return_counts=True)
        user_data[user] = dict(zip(unique, counts))

        for items in user_data[user].items():
            tsv_writer.writerow([user, items[0], items[1]])