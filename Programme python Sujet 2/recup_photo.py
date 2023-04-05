import mysql.connector



def recup_photo(nom):
    # Établissement de la connexion
    cnx = mysql.connector.connect(user='admin', password='sae302',
                                host='172.20.10.3', database='doss_etu')


    requete = "SELECT photo FROM etudiants WHERE nom = %s"
    values = (nom,)

    # Exécution de la requête
    cursor = cnx.cursor()
    cursor.execute(requete, values)

    # Récupération des données binaires du fichier
    data = cursor.fetchone()[0]

    # Écriture des données binaires dans un nouveau fichier
    with open(nom+'.png', 'wb') as f:
        f.write(data)

    # Fermeture de la connexion
    cnx.close()

   # print(nom+".png")
    return nom+".png"
