import pandas as pd
import os
from gen_dataset_810 import mb_ds


# --------------------------------------------------------------------------------------
# Sur la base du dossier parent
# --------------------------------------------------------------------------------------
# Fonction speciale candidats
def get_full_histo_data (dossierparent, noprint = True) :
    try :
        dirliste = [x[0] for x in os.walk(dossierparent)]
    except :
        print("Impossible d'acceder au dossier parent")
        return
    dtf_resultat_v = pd.DataFrame()
    dtf_resultat_c = pd.DataFrame()

    if len(dirliste) > 1 :
        del dirliste[0]
    else :
        print("Impossible d'atteindre les sous-dossiers")

    cnt = 0

    for dossier in dirliste :
        dt_candidats = mb_ds()
        dtf_videos, dtf_chaines  = dt_candidats.get_full_data_candidat(folder = dossier+"/")
        if cnt == 0 :
            dtf_resultat_v = dtf_videos
            dtf_resultat_c = dtf_chaines
        else :
            dtf_resultat_v = dtf_resultat_v.append(dtf_videos, ignore_index=True)
            dtf_resultat_c = dtf_resultat_c.append(dtf_chaines, ignore_index=True)
        if not noprint :
            print("Recursion, "+ str(cnt)+", taille : "+str(dtf_resultat_v.shape[0]))
        cnt += 1

    return dtf_resultat_v, dtf_resultat_c


# --------------------------------------------------------------------------------------
# Créer une dataframe d'évolutions des indicateurs de chaînes entre deux dates
# --------------------------------------------------------------------------------------
# Récupérer le nombre d'abonnées pour une chaîne spécifique
def get_abo_a_date (dtf_histo_chaine, dateRqt) :
    try :
        nb_abo = dtf_histo_chaine[dtf_histo_chaine['dateRqt'] == dateRqt].iloc[0]['abonnesChaine']
    except :
        # print("Impossible de récupérer le nombre d'abonnés pour la date "+ str(dateRqt))
        nb_abo = 0
    return nb_abo

# Récupérer le nombre de vues pour une chaîne spécifique
def get_vues_a_date (dtf_histo_chaine, dateRqt) :
    try :
        nb_vues = dtf_histo_chaine[dtf_histo_chaine['dateRqt'] == dateRqt].iloc[0]['vuesChaine']
    except :
        # print("Impossible de récupérer le nombre de vues pour la date "+ str(dateRqt))
        nb_vues = 0
    return nb_vues

# Récupérer le nombre de vidéos pour une chaîne spécifique
def get_videos_a_date (dtf_histo_chaine, dateRqt) :
    try :
        nb_vids = dtf_histo_chaine[dtf_histo_chaine['dateRqt'] == dateRqt].iloc[0]['nbVideosChaine']
    except :
        # print("Impossible de récupérer le nombre de vidéos pour la date "+ str(dateRqt))
        nb_vids = 0
    return nb_vids

# Retourne le courant associé au candidat
def get_courant_candidat (dtf_histo_chaine) :
    try :
        courant = dtf_histo_chaine.iloc[0]['courant']
    except :
        print("Impossible de récupérer le courant")
        courant = "inconnu"
    return courant

# Génère un dtf qui pour chaque candidat
def make_dtf_evo_global(dtfchaineshisto, datedebut, datefin, base = 'candidat') :
    liste_evo_par_base = []
    for filtre in dtfchaineshisto[base].unique() : 
        # On récupère seulement les lignes qui concernent le candidat ou la chaîne
        dtf_filtre = dtfchaineshisto[dtfchaineshisto[base] == filtre]

        # On récupère le courant pour pouvoir colorer
        courant = get_courant_candidat(dtf_filtre)

        # On récupère les données relatives au nombre d'abonnées
        nb_abo_ini = get_abo_a_date(dtf_histo_chaine = dtf_filtre, dateRqt = datedebut)
        nb_abo_final = get_abo_a_date(dtf_histo_chaine = dtf_filtre, dateRqt = datefin)
        delta_abo = nb_abo_final - nb_abo_ini
        if delta_abo != 0 :
            diviseur = delta_abo
        else :
            diviseur = 1
        if nb_abo_ini > 0 :
            diviseur = nb_abo_ini
        taux_abo = (delta_abo/diviseur)

        # On récupère les données relatives au nombre de vues
        nb_vues_ini = get_vues_a_date(dtf_histo_chaine = dtf_filtre, dateRqt = datedebut)
        nb_vues_final = get_vues_a_date(dtf_histo_chaine = dtf_filtre, dateRqt = datefin)
        delta_vues = nb_vues_final - nb_vues_ini
        if delta_vues != 0 :
            diviseur = delta_vues
        else :
            diviseur = 1
        if nb_vues_ini > 0 :
            diviseur = nb_vues_ini
        taux_vues = (delta_vues/diviseur)

        # On récupère les données relatives au nombre de videos
        nb_videos_ini = get_videos_a_date(dtf_histo_chaine = dtf_filtre, dateRqt = datedebut)
        nb_videos_final = get_videos_a_date(dtf_histo_chaine = dtf_filtre, dateRqt = datefin)
        delta_videos = nb_videos_final - nb_videos_ini
        if delta_videos != 0 :
            diviseur = delta_videos
        else :
            diviseur = 1
        if nb_videos_ini > 0 :
            diviseur = nb_videos_ini
        taux_videos = (delta_videos/diviseur)

        # On ajoute toutes ces infos à une liste qui formera notre dataframe de retour
        liste_evo_par_base.append([datefin, filtre, courant, nb_abo_ini, nb_abo_final, delta_abo, taux_abo, nb_vues_ini, nb_vues_final, delta_vues, taux_vues, nb_videos_ini, nb_videos_final, delta_videos, taux_videos])

    df_evo = pd.DataFrame(liste_evo_par_base, columns=['dateRqt', base, 'courant', 'nbabo_intial', 'nbabo_final', 'nbabo_delta', 'nbabo_taux', 'nbvues_intial', 'nbvues_final', 'nbvues_delta', 'nbvues_taux', 'nbvideos_intial', 'nbvideos_final', 'nbvideos_delta', 'nbvideos_taux'])
    return df_evo
