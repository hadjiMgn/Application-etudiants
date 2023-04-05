from personne import Personne

class Etudiant(Personne):
    #constructeur de la classe etudiant
    def __init__(self):
        Personne.__init__(self)
        self.__annee = 0
        self.__matiere = ""
        self.__photo = ""
        self.__mdp = ""
        self.__infos_etu = {}
    
    #acceseurs et mutateurs
    def get_annee(self):
        return self.__annee
    
    def set_annee(self, nv_annee):
        self.__annee = nv_annee
        
    def get_matiere(self):
        return self.__matiere
    
    def set_matiere(self, nv_matiere):
        self.__matiere = nv_matiere
        
    def get_photo(self):
        return self.__photo
    
    def set_photo(self, nv_photo):
        self.__photo = nv_photo

    def get_mdp(self):
        return self.__mdp

    def set_mdp(self, nv_mdp):
        self.__mdp = nv_mdp

    def get_infos_etu(self):
        return self.__infos_etu

    def set_infos_etu(self, nv_infos_etu):
        self.__infos_etu = nv_infos_etu
      
    #méthode pour afficher les infos d'un étudiant
    def Affiche(self):
        liste_personne = Personne.Affiche(self)
        return [liste_personne[0], liste_personne[1], liste_personne[2], self.__annee, self.__matiere, self.__photo, self.__mdp]
    

