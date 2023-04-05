class Personne :
    #constructeur de la classe personne
    def __init__(self):
        self.__nom = ""
        self.__prenom = ""
        self.__email = ""
        
    
    # acceseurs et mutateurs
    def get_nom(self):
        return self.__nom
    
    def set_nom(self, nv_nom):
        self.__nom = nv_nom
        
    def get_prenom(self):
        return self.__prenom
    
    def set_prenom(self, nv_prenom):
        self.__prenom = nv_prenom
        
    def get_email(self):
        return self.__email
    
    def set_email(self, nv_email):
        self.__email = nv_email
    
    #méthode pour afficher les infos de la personne
    def Affiche(self):
        return [self.__nom, self.__prenom, self.__email]

        
