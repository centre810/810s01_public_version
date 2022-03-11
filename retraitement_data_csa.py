import pandas as pd
import re

# Auteur : Maximo Rose
# Website : https://maximorose.eu
# Merci a tous ceux qui ont depose du contenu sur le web pour m'aider a faire ca. Merci a Google pour ses API haut de gamme et la qulite de leurs services
# Thanks to all of you who put contents on the web. I'll try to quote most of you

# module d'expressions regulieres pour nettoyer les chaines de caracteres
import re
# module cree en suivant ce site : https://pythonhowtoprogram.com/how-to-update-the-airtable-using-python3/
from a_at_loader_810 import atListe
from a_load_paramz_810 import api_parameters


my_parameters = api_parameters()


###################################################
# INIT AIRTABLE PARAMETERS
###################################################
at_APIkey = my_parameters.airtable_api_key 
at_baseId = my_parameters.airtable_base_id 
# On va chercher la table des candidats
at_tableName = my_parameters.airtable_csa_table_name 
#Recuperation de la table AT en memoire
myAirtable = atListe(at_baseId, at_tableName, at_APIkey)
#Recuperation d'une liste finie de records
at_csa_candidats = myAirtable.get_at_AllRecords()


##################################################################
# INIT CSA dataframe sur la base des fichiers passés en paramètres
##################################################################
# Initialise le dataframe des temps de paroles du CSA, issues de leurs relevés publiés
def init_csa_dataframe (lst_fichiers = []) :
    if lst_fichiers == [] :
        print("Le liste de fichiers en paramètres est vide")
        print("FONCTION INTERROMPUE")
        return
    
    cnt = 0
    nb_col_ref = 0

    for nomfichier in lst_fichiers :
        tmp_dtf = pd.read_csv(nomfichier)

        if cnt == 0 :
            nb_col_ref = tmp_dtf.shape[1]
            output_dtf = tmp_dtf
        
        else :
            if tmp_dtf.shape[1] != nb_col_ref :
                print("Le fichier "+nomfichier+ " n'a pas autant de colonnes que les autres fichiers")
                print("VERIFIER LE FICHIER")
                continue
            
            output_dtf = output_dtf.append(tmp_dtf, ignore_index = True)
        
        cnt += 1
    
    print("Données CSA importées - "+ str(output_dtf.shape[0]) + " lignes")
    
    return output_dtf


# Fonction qui filtre les données du CSA seulement sur les candidats présents dans notre liste AirTable
# Puis elle y accole nos information de parti et de courant
def create_filtered_csa_dtf(dtfcsa) :
    dtf_ouput = pd.DataFrame()
    # Concaténer les databases : la liste airtable de référence et les données du CSA
    for record in at_csa_candidats :
        candidat = record['fields']['Name']
        parti = record['fields']['parti']
        courant = record['fields']['Courant']
        dtf_candidat = dtfcsa[dtfcsa['intervenant'] == candidat]
        dtf_candidat.insert(1, 'courant', courant)
        dtf_candidat.insert(1, 'parti', parti)
        dtf_ouput = dtf_ouput.append(dtf_candidat, ignore_index = True)
    
    return dtf_ouput



# Retourne le temps somme pour un subdtf
def somme_temps (subdtf) :
    total_minutes = 0
    for index, row in subdtf.iterrows() :
        str_time = row['duree'].split(':')
        temps_minutes = int(str_time[0])*60 + int(str_time[1]) + int(str_time[2])/30
        total_minutes += temps_minutes
    
    return total_minutes

# Creer Nouveau dataset pour traitement plus aise
def dtf_temps_antenne_minutes_candidats (dtfcsa) :
    lst_result = []
    for candidat in dtfcsa.intervenant.unique() :
        subdtf = dtfcsa[dtfcsa['intervenant'] == candidat]
        temps_total = somme_temps(subdtf=subdtf)

        try :
            courant = subdtf.courant.unique()[0]
        except :
            print("Impossible d'accéder au courant du candidat " + candidat)
            continue

        try :
            parti = subdtf.parti.unique()[0]
        except :
            print("Impossible d'accéder au parti du candidat " + candidat)
            continue

        lst_result.append([candidat, courant, parti, temps_total])


    dfres = pd.DataFrame(lst_result, columns=['intervenant','courant','parti', 'minutes'])
    dfres = dfres.sort_values(by = ['minutes'], ascending=False)

    return dfres