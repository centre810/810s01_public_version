# Passer dans le shell OS la commande :
#       pip3 install airtable-python-wrapper
# Tuto suivi : https://pythonhowtoprogram.com/how-to-update-the-airtable-using-python3/
import os
from pprint import pprint
from airtable import Airtable

class atListe:

    # Initialise la connection a la base airtable passee en parametre
    def __init__(self, baseId, tableName,at_APIkey):
        self.base_id = baseId
        self.table_name = tableName
        self.at_APIkey = at_APIkey
        self.airtable = Airtable(baseId, tableName, at_APIkey)
        self.at_records = []

    # Recupere tous les elements de la liste airtable associee aux parametres du constructeur.
    def get_at_AllRecords(self):
        pages = self.airtable.get_all()
        self.at_records = pages
        return pages

    # Affiche le premier element de la liste airtable
    # Utile pour voir la tête des records Airtable
    def print_first_record(self):
        pages = self.airtable.get_iter(maxRecords=1)
        for page in pages:
            for record in page:
                pprint(record) 

    # Filtre les elements de airtable sur la base d'un nom de colonne et d'une valeur associee
    ## Pour les chaines de caracteres (texte, URL, choix unique) : On regarde si la valeur attendue est presente
    ## Pour les listes (colonne a valeur multiple): On regarde si la valeur attendue est presente dans la liste
    ## Sinon (pour les nombres) : On regarde si la valeur de la colonne est egale a la valeur attendue
    def filter_at_pages(self, colonne_name = "", colonne_value = "") : 
        # Initialise la liste qui sera retournee
        pages = []
        if colonne_name == "" or colonne_value == "" :
            pages = self.at_records
            return pages

        for page in self.at_records :
            # lorsqu'un champ est laisse vide dans la liste airtable, le dictionnaire associe a la ligne, ne contient pas la cle concernee
            # Du coup, il est preferable de tester des le debut l'existence de la cle pour la ligne concernee
            # On recupere le type de la colonne
            try :
                type_colonne = type(page['fields'][colonne_name])
            except KeyError :
                # print("La colonne demandee n'existe pas pour l'element "+ page['fields']['Name'])
                continue

            # Si string, chaine de caracteres
            if type_colonne is str :
                # print("colonne is string")
                try :
                    if page['fields'][colonne_name].find(colonne_value) != -1 :
                        pages.append(page)
                except KeyError :
                    print ("Impossible d'acceder a la valeur de "+colonne_name+" pour l'element "+page['fields']['Name'])
                    continue
            # Si liste
            elif type_colonne is list :
                # print("colonne is list")
                try :
                    if colonne_value in page['fields'][colonne_name]:
                        pages.append(page)
                except KeyError :
                    print ("Impossible d'acceder a la valeur de "+colonne_name+" pour l'element "+page['fields']['Name'])
                    continue
            # Sinon
            else :
                try :
                    if page['fields'][colonne_name] == colonne_value :
                        pages.append(page)
                except KeyError :
                    print ("Impossible d'acceder a la valeur de "+colonne_name+" pour l'element "+page['fields']['Name'])
                    continue

        return pages


