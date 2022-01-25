import psycopg2

all_entities_select_Query = "SELECT id FROM dataprocessing_items ORDER BY id;"
all_rpds_select_Query = "SELECT id FROM workprogramsapp_workprogram"
approved_rpd_outcomes_select_Query = "SELECT workprogram_id, item_id FROM dataprocessing_items di " \
                                     "JOIN workprogramsapp_outcomesofworkprogram wo on di.id = wo.item_id " \
                                     "where wo.workprogram_id in " \
                                     "(SELECT work_program_id FROM workprogramsapp_expertise we " \
                                     "WHERE we.expertise_status = 'AC' ) " \
                                     "ORDER BY workprogram_id;"

rpd_outcomes_by_id_select_Query = "SELECT workprogram_id, item_id FROM dataprocessing_items di " \
                                  "JOIN workprogramsapp_outcomesofworkprogram wo on di.id = wo.item_id " \
                                  "where wo.workprogram_id in " \
                                  "(SELECT work_program_id FROM workprogramsapp_expertise we " \
                                  "WHERE we.expertise_status = 'AC' ) " \
                                  "ORDER BY workprogram_id;"

rpd_outcomes_vector_select_Query = "SELECT id, " \
                                   "CASE " \
                                   "WHEN id in (" \
                                   "SELECT id " \
                                   "FROM dataprocessing_items di " \
                                   "WHERE di.id in ( " \
                                   "SELECT wo.item_id " \
                                   "FROM workprogramsapp_outcomesofworkprogram wo " \
                                   "JOIN workprogramsapp_expertise we on we.work_program_id = wo.workprogram_id " \
                                   "WHERE we.expertise_status = 'AC' " \
                                   "AND wo.workprogram_id = (%s)" \
                                   ")" \
                                   ") THEN 1 " \
                                   "ELSE 0 " \
                                   "END feature " \
                                   "FROM dataprocessing_items " \
                                   "ORDER BY id;"

try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="analytics_db")
    cursor = connection.cursor()
    postgreSQL_select_entities_Query = all_rpds_select_Query
    postgreSQL_select_Query = rpd_outcomes_vector_select_Query

    cursor.execute(postgreSQL_select_entities_Query)
    print("Selecting rows from mobile table using cursor.fetchall")
    vector = {}
    records = cursor.fetchall()

    print("Print each row and it's columns values")
    for row in records:
        rpd_id = row[0]
        vector[rpd_id] = []
        cursor.execute(postgreSQL_select_Query, (rpd_id,))
        data = cursor.fetchall()
        for item in data:
            vector[rpd_id].append(item[1])
    print(vector)
except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
