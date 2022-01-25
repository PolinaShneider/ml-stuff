import psycopg2

from train import calculate_distance

all_entities_select_Query = "SELECT id FROM public.dataprocessing_items ORDER BY id;"
rpd_grouped_features_select_Query = "SELECT wiei.workprogram_id, ARRAY_AGG( wiei.entity_id ORDER BY wiei.workprogram_id, wiei.entity_id ) features FROM (SELECT wo.workprogram_id, di.id as entity_id FROM public.dataprocessing_items di JOIN public.workprogramsapp_outcomesofworkprogram wo on di.id = wo.item_id JOIN public.workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id WHERE we.expertise_status = 'AC' ) as wiei GROUP BY wiei.workprogram_id ORDER BY wiei.workprogram_id LIMIT 1000;"


def normalize(own_features, all_features):
    res = []
    for i in range(len(all_features)):
        if all_features[i] in own_features:
            res.append(1)
        else:
            res.append(0)
    return res


try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="analytics_db")

    cursor = connection.cursor()
    cursor.execute(all_entities_select_Query)
    entities = cursor.fetchall()

    cursor.execute(rpd_grouped_features_select_Query)
    rpd_features = cursor.fetchall()
    print("Selecting rows from mobile table using cursor.fetchall")
    vector = {}
    all_features = set()

    print("Print each row and it's columns values")
    for row in rpd_features:
        rpd_id = row[0]
        features = row[1]
        all_features.update(features)

    for row in rpd_features:
        rpd_id = row[0]
        features = row[1]
        vector[rpd_id] = normalize(features, sorted(all_features))

    calculate_distance(vector)
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
