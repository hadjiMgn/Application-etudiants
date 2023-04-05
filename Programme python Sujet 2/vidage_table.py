import mysql.connector

try:
    connection_params = {
    'host': "172.20.10.3",
    'user': "admin",
    'password': "sae302",
    'database': "doss_etu"
}
except mysql.connector.Error as e:
    print("Exception : ", e)
else:
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute("SET FOREIGN_KEY_CHECKS = 0;")
            c.execute("truncate table etudiants;")
            c.execute("truncate table moy_gen;")
            c.execute("truncate table notes;")
            c.execute("truncate table profs;")
            c.execute("SET FOREIGN_KEY_CHECKS = 1;")
            
        db.commit()
        db.close()