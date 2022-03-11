import json


class api_parameters :

    # Initialise mes parametres preferes contenu dans le fichier de config .json
    def __init__(self, nom_fichier = "./config/APIs_paramz.json"):
        # On charge le fichier json en memoire
        json_settings = self.get_paramfile(config_file = nom_fichier)
        
        # Le fichier de config doit au moins contenir la cle de l'API
        try :
            self.airtable_api_key = json_settings["AirTable API key"]
        except KeyError :
            print("Impossible de trouver la clé API AirTable")
            self.airtable_api_key = ""

        # L'ID de la base
        try :
            self.airtable_base_id = json_settings["AirTable base ID"]
        except KeyError :
            print("Impossible de trouver l'ID de la base AirTable")
            self.airtable_base_id = ""

        # Le nom de la table candidats
        try :
            self.airtable_candidat_table_name = json_settings["AirTable candidat table Name"]
        except KeyError :
            print("Impossible de trouver le nom de la table AirTable des candidats")
            self.airtable_candidat_table_name = ""

        
        # Le nom de la table partis
        try :
            self.airtable_parti_table_name = json_settings["AirTable parti table Name"]
        except KeyError :
            print("Impossible de trouver le nom de la table AirTable des partis")
            self.airtable_parti_table_name = ""

        # Le nom de la table du csa
        try :
            self.airtable_csa_table_name = json_settings["AirTable csa table Name"]
        except KeyError :
            print("Impossible de trouver le nom de la table AirTable du CSA")
            self.airtable_csa_table_name = ""

        # YOUTUBE API PARAMETERS REMOVED


    # Recupere les parametres graphiques du fichier de config sous la forme d'un dictionnaire
    def get_paramfile(self, config_file = "/config/airtable_paramz.json") :
        # read file
        with open(config_file, 'r') as myfile:
            data=myfile.read()
        # parse file
        obj = json.loads(data)
        return obj