# importations
from kivy.app import App
import shutil
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from Etudiant import Etudiant
from Prof import Prof
import mysql.connector
from hashlib import sha512
import random
from get_bina import get_binary_data
from recup_photo import recup_photo

    
#Classe qui gère la fenêtre de connexion
class Connexion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    # déclaration des variables
    my_text = StringProperty("")
    email = ObjectProperty(None)
    passwd = ObjectProperty(None)
    log = ObjectProperty(None)
    vision = ObjectProperty(None)
    bvn= ObjectProperty(None)
    
    
    
class SecondWindow(Screen):
    pass


#Classe pour gérer la fenêtre d'inscription pour un étudiant
class InscriptionEtu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #initialisation des variables 
    nom = ObjectProperty(None)
    prenom = ObjectProperty(None)
    email = ObjectProperty(None)
    annee = ObjectProperty(None)
    matiere = ObjectProperty(None)
    photo = ObjectProperty(None)
    mdp = ObjectProperty(None)
    file_path= ObjectProperty(None)
    erreur = ObjectProperty(None)
    

#Classe qui gère la fenêtre d'inscription pour un prof
class InscriptionProf(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verif_prof = True
        self.verif_email_prof = True

    nom = ObjectProperty(None)
    prenom = ObjectProperty(None)
    email = ObjectProperty(None)
    mdp = ObjectProperty(None)
    erreur = ObjectProperty(None)
    
   
    
class EtuHome(Screen):
    bvn = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ProfHome(Screen):
    bvn = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        


class ImgEtu(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
     #Va renvoyer le chemin de l'image sélectionée   
    def selected(self, filechooser):
        if filechooser:
            self.multiselect = False
            #print(type(filechooser))
            self.ids.img.source = filechooser[0]
            self.path_photo = filechooser[0]
            

    

class WindowManager(ScreenManager):
    pass


class sae(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #initialisation des variables globales
        self.can_connect = False
        self.whos_connect = ""
        self.is_etu = False
        self.is_prof = False
        self.verif_etu = True
        self.verif_email_etu = True
        self.specialisation = ""
        
    #instanciations 
    e = Etudiant()
    p = Prof()

    

    #Permet de remplacer les backslash par deux backslash pour eviter des erreurs
    def remplacer_backslash(self,chaine):
        return chaine.replace("\\\\", "\\")

    #Permet de remplacer les backslash et d'affecter le chemin au self.e.photo
    def recup_chemin(self, path, selection):
        selected_file_path = selection[0]
        self.root.get_screen("ImgEtu").ids.img.source= selected_file_path
        #print(self.remplacer_backslash(selected_file_path))
        self.e.set_photo(self.remplacer_backslash(selected_file_path))
        


    #Méthode lorsque la connexion est acceptée
    def accept(self):
        self.root.get_screen("Connexion").ids.my_text = "Connexion Réussie !"
        self.root.get_screen("Connexion").ids.log.background_color=(0, 0, 0.4, 0.4)

    #Méthode lorsque la connexion est refusée
    def refuse(self):
        self.root.get_screen("Connexion").ids.my_text = "Connexion Refusée !"
        self.root.get_screen("Connexion").ids.log.background_color=(0.6, 0, 0, 1)

    def reset_color(self):
        self.root.get_screen("Connexion").ids.my_text = ""
        self.root.get_screen("Connexion").ids.log.border=(8, 8, 8, 8)

    #Méthode pour cahcer ou afficher le mot de passe
    def toggle_password_visibility(self, checkbox):
        if self.root.get_screen("Connexion").ids.passwd.text == "":
            return
        if checkbox.active:
            self.root.get_screen("Connexion").ids.passwd.password = False
            self.root.get_screen("Connexion").ids.vision.text = "Masquer le mot de passe"
        else:
            self.root.get_screen("Connexion").ids.passwd.password = True
            self.root.get_screen("Connexion").ids.vision.text = "Afficher le mot de passe"

    #Méthode pour authentifier un utilisateur lors de la tentative de connexion
    def connex(self):
        lst_etu = []
        lst_prof = []
        self.whos_connect = ""
        self.is_etu = False
        self.is_prof = False

        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            #requête pour obtenir chaque mail et mdp étudiant de la bdd
            request = """select email, mdp from etudiants;"""
            #requête pour obtenir chaque mail et mdp prof de la bdd
            request2 = """select email, mdp from profs;"""
            #requête pour obtenir l'id de l'étudiant
        
        with mysql.connector.connect(**connection_params) as db :
            with db.cursor() as c:
                c.execute(request)
                rq = c.fetchall()
                c.execute(request2)
                rq2 = c.fetchall()
            db.commit()
            db.close()

        #parcourt chaque mail et mdp étudiant
        for element in rq :
            mail = element[0]
            pwd = element[1]

            #ajoute les mails et mdp étudiant à une liste
            mlpswd = [mail, pwd]
            lst_etu.append(mlpswd)

        #parcourt chaque mail et mdp prof
        for element in rq2:
            mail = element[0]
            pwd = element[1]

            #ajoute les mails et mdp prof dans une liste
            mlpswd = [mail, pwd]
            lst_prof.append(mlpswd)    
        
        #variable mail2 prend pour valeur le mail entré par l'utilisateur lors de la connexion
        mail2 = self.root.get_screen("Connexion").ids.email.text
        #variable mail2 prend pour valeur le mdp entré par l'utilisateur lors de la connexion
        pwd2 = self.root.get_screen("Connexion").ids.passwd.text

        pwd2_crypt = sha512(pwd2.encode()).hexdigest()
        
        

        #teste si le mail et le mdp entrée par l'utilisateur correspond à une paire mail mdp de la BDD
        for elem in lst_etu:
            if elem[0] == mail2 and elem[1] == pwd2_crypt:
                self.can_connect = True
                self.is_etu = True
                self.whos_connect = "etu"

        for elem in lst_prof:
            if elem[0] == mail2 and elem[1] == pwd2_crypt:
                self.can_connect = True
                self.is_prof = True
                self.whos_connect = "prof"
        
        #si c'est le cas : CONNEXION + changement d'écran
        if self.can_connect and self.is_etu:
            self.accept()
            self.root.get_screen("Connexion").manager.current = "EtuHome"
            self.reset_color()
        
        elif self.can_connect and self.is_prof:
            self.accept()
            self.root.get_screen("Connexion").manager.current = "ProfHome"
            self.reset_color()
        #si ce n'est pas le cas : CONNEXION REFUSEE
        else:
            self.refuse()
    
    

    def recup_matieres_notes(self):
        infos_etu = []
        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            if self.whos_connect == "etu":
                #requête pour obtenir chaque mail et mdp étudiant de la bdd
                request = """select matiere, moyenne from etu_resume where email = %s;"""
                request2 = """select nom, prenom, email, annee, spe, photo from etudiants where email = %s;"""
            
            elif self.whos_connect == "prof":
                #requête pour obtenir chaque mail et mdp prof de la bdd
                request = """select email, matiere, moyenne from etu_resume;"""
                request2 = """select nom, prenom, email, annee, spe, photo from etudiants;"""
        
        with mysql.connector.connect(**connection_params) as db :
            with db.cursor() as c:
                if self.whos_connect == "etu":
                    c.execute(request, (self.root.get_screen("Connexion").ids.email.text,))
                    rq = c.fetchall()
                    c.execute(request2, (self.root.get_screen("Connexion").ids.email.text,))
                    rq2 = c.fetchall()
                elif self.whos_connect == "prof":
                    c.execute(request)
                    rq = c.fetchall()
                    c.execute(request2)
                    rq2 = c.fetchall()
            db.commit()
            db.close()
               
                

        if self.whos_connect == "etu":    
            notes = {"Reseau": rq[0][1], "Telecom": rq[1][1], "Maths" : rq[2][1], "Programmation" : rq[3][1], "Anglais" : rq[4][1], rq2[0][4] : rq[5][1]}

            infos_etu = {"Nom": rq2[0][0], "Prenom": rq2[0][1], "Email" : rq2[0][2], "Annee" : rq2[0][3], "Photo" : rq2[0][5], "notes": notes}

            
            

        elif self.whos_connect == "prof":
            infos_etu = []
            rq_list = []
            rq2_list = []

            #transforme la liste de tuples en une liste de liste
            for note in rq:
                rq_list.append([note[0], note[1], note[2]])

            for elem in rq2:
                rq2_list.append([elem[0], elem[1], elem[2], elem[3], elem[4]])




            #ajoute à une liste les dictionnaires contenant les infos des étudiants
            for elem in rq2:
                infos = {"Nom": elem[0], "Prenom": elem[1], "Email" : elem[2], "Annee" : elem[3], "Spe" : elem[4], "Photo" : elem[5], "Notes": None}
                infos_etu.append(infos)



            for i in range(len(infos_etu)):
                notes = {}
                for y in range(len(rq_list)):
                    
                    if infos_etu[i]['Email'] == rq_list[y][0]:
                        notes[rq_list[y][1]] = rq_list[y][2]

                infos_etu[i]["Notes"] = notes
        
        self.e.set_infos_etu(infos_etu)
       

        

    def reinitialise_champs_connexion(self):
        self.root.get_screen("Connexion").ids.email.text = ""
        self.root.get_screen("Connexion").ids.passwd.text = ""


    def reset_connexion(self):
        self.reinitialise()



    #Méthode pour la création d'un compte étudiant
    def enregistrement_etudiant(self):
        #ajout des informations de l'étudiant
        self.e.set_nom(self.root.get_screen("InscriptionEtu").ids.nom.text)
        self.e.set_prenom(self.root.get_screen("InscriptionEtu").ids.prenom.text)
        self.e.set_email(self.root.get_screen("InscriptionEtu").ids.email.text)
        self.e.set_annee(self.root.get_screen("InscriptionEtu").ids.annee.text)
        self.e.set_matiere(self.root.get_screen("InscriptionEtu").ids.matiere.text)
        mdp_crypt = sha512(self.root.get_screen("InscriptionEtu").ids.mdp.text.encode()).hexdigest()
        self.e.set_mdp(mdp_crypt)
        

        
        
        
        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            #envoie des données de l'étudiant vers la BDD
            request = """insert into etudiants(nom,prenom,annee,spe,photo,email,mdp) values(%s,%s,%s,%s,%s,%s,%s)"""
            params = (self.e.get_nom(), self.e.get_prenom(), self.e.get_annee(), self.e.get_matiere(), get_binary_data(self.e.get_photo()), self.e.get_email(), self.e.get_mdp())

            #ajout dans la table 'moy_gen'
            request2 = """insert into moy_gen(nom,prenom,mail_etu) values(%s,%s,%s)"""
            params2 = (self.e.get_nom(), self.e.get_prenom(), self.e.get_email())

        with mysql.connector.connect(**connection_params) as db :
            with db.cursor() as c:
                c.execute(request,params)
                c.execute(request2,params2)
            db.commit()
            db.close()

    #Méthode pour vérifier que tous les champs du formulaire sont remplis
    def verif_formulaire_etu(self):
        #initialisation à True de la variable verif à chaque vérification 
        self.verif_etu = True
        #si un seul des champs n'est pas rempli 
        if self.root.get_screen("InscriptionEtu").ids.nom.text == "" or self.root.get_screen("InscriptionEtu").ids.prenom.text == "" or self.root.get_screen("InscriptionEtu").ids.email.text == "" or self.root.get_screen("InscriptionEtu").ids.annee.text == "Séléctionnez votre année d'étude" or self.root.get_screen("InscriptionEtu").ids.matiere.text == "Séléctionnez une matière" or self.root.get_screen("InscriptionEtu").ids.mdp.text == "" or self.root.get_screen("InscriptionEtu").ids.img.text == "Séléctionnez votre image":
            #envoi d'un message d'erreur
            self.root.get_screen("InscriptionEtu").ids.erreur.text = "Veuillez remplir tous les champs du formulaire."
            #variable verif à False
            self.verif_etu = False
        
    #Méthode pour vérifier que le mail entré par l'utilisateur n'est pas déjà utilisé
    def verif_mail_etu(self):
        #initialisation de la variable de verif à True
        self.verif_email_etu = True
        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            #requête pour obtenir les mails des etudiants et des profs
            request = """select email from etudiants;"""
            request2 = """select email from profs;"""

        with mysql.connector.connect(**connection_params) as db :
            with db.cursor() as c:
                c.execute(request)
                rq = c.fetchall()
                c.execute(request2)
                rq2 = c.fetchall()
            db.commit()
            db.close()

            #parcours de chaque mail, si le mail existe dans la BDD : variable de verif passe à FALSE
            for elem in rq:
                 if elem[0] == self.root.get_screen("InscriptionEtu").ids.email.text:
                    self.verif_email_etu = False
            
            #parcours de chaque mail, si le mail existe dans la BDD : variable de verif passe à FALSE
            for elem in rq2:
                if elem[0] == self.root.get_screen("InscriptionEtu").ids.email.text:
                    self.verif_email_etu = False
    
    #Méthode d'envoie d'un message d'erreur si le mail est déjà utilisé
    def same_mail_etu(self):
        self.root.get_screen("InscriptionEtu").ids.erreur.text = "Ce mail est déjà utilisé"
                
    
    #Méthode pour le else après la condition if dans le fichier kv
    def inactif(self):
        pass

    #Méthode pour réinitialiser les champs du formulaire
    def reinitialise_form_etu(self):
        self.root.get_screen("InscriptionEtu").ids.nom.text = ""
        self.root.get_screen("InscriptionEtu").ids.prenom.text = ""
        self.root.get_screen("InscriptionEtu").ids.email.text = ""
        self.root.get_screen("InscriptionEtu").ids.annee.text = "Séléctionnez votre année d'étude"
        self.root.get_screen("InscriptionEtu").ids.matiere.text = "Séléctionnez une matière"
        self.root.get_screen("InscriptionEtu").ids.mdp.text = ""
        self.root.get_screen("InscriptionEtu").ids.erreur.text = ""
        self.root.get_screen("InscriptionEtu").ids.img.text = "Séléctionnez votre image"



    #Méthode pour envoyer des notes lors de l'insription d'un étudiant
    def envoie_notes(self):
        #récupère le mail et la spé de l'étudiant
        email = self.e.get_email()
        spe = self.e.get_matiere()
        

        #liste de toutes les matières de l'étudiant
        matieres = ["Maths", "Programmation", "Réseau", "Télécom", "Anglais", spe]

        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            with mysql.connector.connect(**connection_params) as db :
                    with db.cursor() as c:
                        for i in range(0, len(matieres)):

                            #envoie des données de l'étudiant vers la BDD
                            request = """insert into notes(mail_etu, matiere, note) values(%s,%s,%s)"""
                            params = (email, matieres[i], round(random.uniform(0, 20) * 4) / 4) 
                            c.execute(request,params)
                            db.commit()
                    db.close()

    
    def copy_file(self, instance):
        file_path = self.file_path.text
        shutil.copy(file_path, "C:\\Users\\Hatim\\Desktop\\test")


    def envoi_blob(self,fichier) :
        
        filename=self.selected(fichier)
        with open(filename,'rb') as f:
            data = f.read()
        self.e.set_photo= str(data)
    
        
    def go_back(self, instance):
        self.manager.current = "main"

    def same_mail_etu(self):
        self.root.get_screen("InscriptionEtu").ids.erreur.text = "Ce mail est déjà utilisé"

    
    
    
    
    def enregistrement_prof(self):
        self.p.set_nom(self.root.get_screen("InscriptionProf").ids.nom.text)
        self.p.set_prenom(self.root.get_screen("InscriptionProf").ids.prenom.text)
        mdp_crypt = sha512(self.root.get_screen("InscriptionProf").ids.mdp.text.encode()).hexdigest()
        self.p.set_mdp(mdp_crypt)
        self.p.set_email(self.root.get_screen("InscriptionProf").ids.email.text)
       
        
        
        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            request = """insert into profs(nom,prenom,email,mdp) values(%s,%s,%s,%s)"""
            params = (self.p.get_nom(), self.p.get_prenom(), self.p.get_email(), self.p.get_mdp())

        with mysql.connector.connect(**connection_params) as db :
            with db.cursor() as c:
                c.execute(request,params)
            db.commit()
            db.close()

    def verif_formulaire_prof(self):
        self.verif_prof = True
        if self.root.get_screen("InscriptionProf").ids.nom.text == "" or self.root.get_screen("InscriptionProf").ids.prenom.text == "" or self.root.get_screen("InscriptionProf").ids.email.text == "" or self.root.get_screen("InscriptionProf").ids.mdp.text == "":
            self.root.get_screen("InscriptionProf").ids.erreur.text = "Veuillez remplir tous les champs du formulaire."
            self.verif_prof = False
        
    def verif_mail_prof(self):
        self.verif_email_prof = True
        try:
            connection_params = {
            'host' : "172.20.10.3",
            'user' : "admin",
            'password' : "sae302",
            'database' : "doss_etu"
            }
        except mysql.connector.Error as e:
            print("Exception : ", e)
        else:
            request = """select email from etudiants;"""
            request2 = """select email from profs;"""

        with mysql.connector.connect(**connection_params) as db :
            with db.cursor() as c:
                c.execute(request)
                rq = c.fetchall()
                c.execute(request2)
                rq2 = c.fetchall()
            db.commit()
            db.close()

            for elem in rq:
                 if elem[0] == self.root.get_screen("InscriptionProf").ids.email.text:
                    self.verif_email_prof = False
            
            for elem in rq2:
                if elem[0] == self.root.get_screen("InscriptionProf").ids.email.text:
                    self.verif_email_prof = False

    


    
    def reinitialise_form_prof(self):
        self.root.get_screen("InscriptionProf").ids.nom.text = ""
        self.root.get_screen("InscriptionProf").ids.prenom.text = ""
        self.root.get_screen("InscriptionProf").ids.email.text = ""
        self.root.get_screen("InscriptionProf").ids.mdp.text = ""
        self.root.get_screen("InscriptionProf").ids.erreur.text = ""
    
    
    def same_mail_prof(self):
        self.root.get_screen("InscriptionProf").ids.erreur.text = "Ce mail est déjà utilisé"
    
    def inactif(self):
        pass


    def selected(self, filename):
        try:
            self.ids.img.source= filename[0]
            return(filename[0])
        except:
            pass
    def envoi_blob(self,fichier) :
        
        filename=self.selected(fichier)
        with open(filename,'rb') as f:
            data = f.read()
        self.e.set_photo=data
    
        
    def go_back(self, instance):
        self.manager.current = "main"










        


    def build(self):
        pass
    
    def page_infos_etu(self):
        inf = self.e.get_infos_etu()
        nom=inf["Nom"]
        prenom=inf["Prenom"]
        annee=inf["Annee"]
        mail=inf["Email"]
        math=round(inf["notes"]["Maths"],2)
        reseau=round(inf["notes"]["Reseau"],2)
        telecom=round(inf["notes"]["Telecom"],2)
        prog=round(inf["notes"]["Programmation"],2)
        anglais=round(inf["notes"]["Anglais"],2)
        name_specialite = list(inf["notes"].keys())[5]
        specialite = round(inf["notes"][name_specialite],2)
        self.root.get_screen("EtuHome").ids.bvn.text=str(nom+" "+prenom)
        self.root.get_screen("EtuHome").ids.annee.text=str(annee)
        self.root.get_screen("EtuHome").ids.mail.text=str(mail)
        self.root.get_screen("EtuHome").ids.math.text=str(math)
        self.root.get_screen("EtuHome").ids.reseau.text=str(reseau)
        self.root.get_screen("EtuHome").ids.prog.text=str(prog)
        self.root.get_screen("EtuHome").ids.telecom.text=str(telecom)
        self.root.get_screen("EtuHome").ids.anglais.text=str(anglais)
        self.root.get_screen("EtuHome").ids.name_specialite.text=name_specialite
        self.root.get_screen("EtuHome").ids.specialite.text=str(specialite)
        self.root.get_screen("EtuHome").ids.photo.source=recup_photo(nom)
        moy = round(((math+reseau+telecom+prog+anglais+specialite)/6),2)
        self.root.get_screen("EtuHome").ids.moyenne.text= str(moy)
        

        

        




    def page_infos_prof(self):
        name = self.root.get_screen("ProfHome").ids.selection.text
        inf = self.e.get_infos_etu()
        trouver = False
        
        for i in range(0, len(inf)):
            if name == inf[i]["Nom"]:
                trouver = True
                mail=inf[i]["Email"]
                annee=inf[i]["Annee"]
                nom=inf[i]["Nom"]
                prenom=inf[i]["Prenom"]
                math=round(inf[i]["Notes"]["Maths"],2)
                reseau=round(inf[i]["Notes"]["Réseau"],2)
                telecom=round(inf[i]["Notes"]["Télécom"],2)
                prog=round(inf[i]["Notes"]["Programmation"],2)
                anglais=round(inf[i]["Notes"]["Anglais"],2)
                spe = inf[i]["Spe"]
                self.specialisation = inf[i]["Spe"]
                special = round(inf[i]["Notes"][spe],2)
                
                self.root.get_screen("ProfHome").ids.name_math.text="Maths"
                self.root.get_screen("ProfHome").ids.name_reseau.text="Réseau"
                self.root.get_screen("ProfHome").ids.name_prog.text="Programmation"
                self.root.get_screen("ProfHome").ids.name_telecom.text="Télécom"
                self.root.get_screen("ProfHome").ids.name_anglais.text="Anglais"
                self.root.get_screen("ProfHome").ids.name_spe.text=spe
                self.root.get_screen("ProfHome").ids.matiere.values = ["Maths", "Réseau", "Programmation", "Anglais", "Télécom", spe]

                self.root.get_screen("ProfHome").ids.math.text=str(math)
                self.root.get_screen("ProfHome").ids.reseau.text=str(reseau)
                self.root.get_screen("ProfHome").ids.prog.text=str(prog)
                self.root.get_screen("ProfHome").ids.telecom.text=str(telecom)
                self.root.get_screen("ProfHome").ids.anglais.text=str(anglais)
                self.root.get_screen("ProfHome").ids.special.text=str(special)
                self.root.get_screen("ProfHome").ids.photo.source=recup_photo(nom)
                self.root.get_screen("ProfHome").ids.mail.text=mail
                self.root.get_screen("ProfHome").ids.annee.text=annee
                self.root.get_screen("ProfHome").ids.prenom.text=prenom

        if not trouver:
            if self.root.get_screen("ProfHome").ids.selection.text == "":
                self.root.get_screen("ProfHome").ids.error.text = "Entrez le nom d'un étudiant"
            else:
                self.root.get_screen("ProfHome").ids.error.text = "Cet étudiant n'est pas présent dans la base de données"
        else:
            self.root.get_screen("ProfHome").ids.error.text = ""

    def reset_infos(self):
        self.root.get_screen("ProfHome").ids.photo.source = ""

        self.root.get_screen("ProfHome").ids.math.text=""
        self.root.get_screen("ProfHome").ids.reseau.text=""
        self.root.get_screen("ProfHome").ids.prog.text=""
        self.root.get_screen("ProfHome").ids.telecom.text=""
        self.root.get_screen("ProfHome").ids.anglais.text=""
        self.root.get_screen("ProfHome").ids.special.text = ""

        self.root.get_screen("ProfHome").ids.name_math.text=""
        self.root.get_screen("ProfHome").ids.name_reseau.text=""
        self.root.get_screen("ProfHome").ids.name_prog.text=""
        self.root.get_screen("ProfHome").ids.name_telecom.text=""
        self.root.get_screen("ProfHome").ids.name_anglais.text=""
        self.root.get_screen("ProfHome").ids.name_spe.text=""
        self.root.get_screen("ProfHome").ids.matiere.values = []
        self.root.get_screen("ProfHome").ids.annee.text = ""
        self.root.get_screen("ProfHome").ids.mail.text = ""
        self.root.get_screen("ProfHome").ids.prenom.text = ""
        self.root.get_screen("ProfHome").ids.note_error.text = ""




    def reset_page_prof(self):
        self.root.get_screen("ProfHome").ids.error.text = ""
        self.root.get_screen("ProfHome").ids.selection.text = ""
        self.root.get_screen("ProfHome").ids.photo.source = ""
        
        self.root.get_screen("ProfHome").ids.math.text = ""
        self.root.get_screen("ProfHome").ids.reseau.text = ""
        self.root.get_screen("ProfHome").ids.prog.text = ""
        self.root.get_screen("ProfHome").ids.telecom.text = ""
        self.root.get_screen("ProfHome").ids.anglais.text = ""
        self.root.get_screen("ProfHome").ids.special.text=""
        self.root.get_screen("ProfHome").ids.note_mod.text=""
        self.root.get_screen("ProfHome").ids.annee.text = ""
        self.root.get_screen("ProfHome").ids.mail.text = ""
        self.root.get_screen("ProfHome").ids.prenom.text = ""
        self.root.get_screen("ProfHome").ids.note_error.text = ""

        self.root.get_screen("ProfHome").ids.name_math.text=""
        self.root.get_screen("ProfHome").ids.name_reseau.text=""
        self.root.get_screen("ProfHome").ids.name_prog.text=""
        self.root.get_screen("ProfHome").ids.name_telecom.text=""
        self.root.get_screen("ProfHome").ids.name_anglais.text=""
        self.root.get_screen("ProfHome").ids.name_spe.text=""
        self.root.get_screen("ProfHome").ids.matiere.text="Séléctionnez la matière"
        self.root.get_screen("ProfHome").ids.matiere.values = []


    def change_text(self):
        chemin = self.e.get_photo().split("\\")

        self.root.get_screen("InscriptionEtu").ids.img.text = chemin[-1]


    def modify_note(self):
        to_modify =  self.root.get_screen("ProfHome").ids.matiere.text
        
        try:
            if 0 <= float(self.root.get_screen("ProfHome").ids.note_mod.text) <= 20 and self.root.get_screen("ProfHome").ids.note_mod.text != "":
                if to_modify == "Maths":
                    self.root.get_screen("ProfHome").ids.math.text = self.root.get_screen("ProfHome").ids.note_mod.text
                elif to_modify == "Réseau":
                    self.root.get_screen("ProfHome").ids.reseau.text = self.root.get_screen("ProfHome").ids.note_mod.text
                elif to_modify == "Programmation":
                    self.root.get_screen("ProfHome").ids.prog.text = self.root.get_screen("ProfHome").ids.note_mod.text
                elif to_modify == "Anglais":
                    self.root.get_screen("ProfHome").ids.anglais.text = self.root.get_screen("ProfHome").ids.note_mod.text
                elif to_modify == "Télécom":
                    self.root.get_screen("ProfHome").ids.telecom.text = self.root.get_screen("ProfHome").ids.note_mod.text
                else:
                    if to_modify == "Cybersécurité" or to_modify == "IA":
                        self.root.get_screen("ProfHome").ids.special.text = self.root.get_screen("ProfHome").ids.note_mod.text
                        
                    else:
                         self.root.get_screen("ProfHome").ids.note_error.text = "Veuillez choisir une matière"
            else:
                self.root.get_screen("ProfHome").ids.note_error.text = "Veuillez entrer une note comprise entre 0 et 20"
            
        except ValueError:
            self.root.get_screen("ProfHome").ids.note_error.text = "Veuillez entrer une note comprise entre 0 et 20"



        else:
            if 0 <= float(self.root.get_screen("ProfHome").ids.note_mod.text) <= 20 and self.root.get_screen("ProfHome").ids.note_mod.text != "":
                try:
                    connection_params = {
                    'host' : "172.20.10.3",
                    'user' : "admin",
                    'password' : "sae302",
                    'database' : "doss_etu"
                    }
                except mysql.connector.Error as e:
                    print("Exception : ", e)
                else:
                    request = """update notes set note = %s where mail_etu = %s and matiere = %s;"""
                    params = (round(float(self.root.get_screen("ProfHome").ids.note_mod.text),2), self.root.get_screen("ProfHome").ids.mail.text, to_modify)

                with mysql.connector.connect(**connection_params) as db :
                    with db.cursor() as c:
                        c.execute(request,params)
                    db.commit()
                    db.close()

           






if __name__ == "__main__":
    sae().run()
