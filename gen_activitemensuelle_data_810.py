import pandas as pd
import datetime


# Fonction utiles pour tous les tableaux ci-apres
# Retourne les videos pour un mois donnees
def vidz_filtree_par_mois(subdtf, mois_moins_un = 13, annee = 2022) : 
    if mois_moins_un == 13 :
        print("mois invalide")
    elif mois_moins_un < 11 :
        videos_du_mois = subdtf[subdtf['dateVideo'] > datetime.datetime(annee, (mois_moins_un+1), 1, 0, 0, 0)]
        videos_du_mois = videos_du_mois[videos_du_mois['dateVideo'] < datetime.datetime(annee, (mois_moins_un+2), 1, 0, 0, 0)]
    else :
        videos_du_mois = subdtf[subdtf['dateVideo'] > datetime.datetime(annee, (mois_moins_un+1), 1, 0, 0, 0)]
        videos_du_mois = videos_du_mois[videos_du_mois['dateVideo'] < datetime.datetime(annee + 1, 1, 1, 0, 0, 0)]
    return videos_du_mois

# Affichage standard : Filtre les données (dataframes) en fonctions des courants associés
def un_dtf_par_courant(subdtf) :
    videos_xd = subdtf[subdtf['courant'] == "Extrême droite"]
    videos_reste = subdtf[subdtf['courant'] != "Extrême droite"]
    videos_xg = subdtf[subdtf['courant'] == "Extrême gauche"]
    videos_reste = videos_reste[videos_reste['courant'] != "Extrême gauche"]
    videos_d = subdtf[subdtf['courant'] == "droite"]
    videos_reste = videos_reste[videos_reste['courant'] != "droite"]
    videos_g = subdtf[subdtf['courant'] == "gauche"]
    videos_reste = videos_reste[videos_reste['courant'] != "gauche"]
    videos_c = subdtf[subdtf['courant'] == "centre"]
    # Ca va sûrement faire rager, mais dans le code, les chaîne d'Emmanuel Macron sont associées au courant "Centre", en tant que dsecendant du Modem
    # Dans nos rapports HTML, on fait généralement référence à la "majorité"
    videos_reste = videos_reste[videos_reste['courant'] != "centre"]
    videos_v = subdtf[subdtf['courant'] == "vert"]
    videos_reste = videos_reste[videos_reste['courant'] != "vert"]
    return videos_xd, videos_xg, videos_d, videos_g, videos_c, videos_v, videos_reste

# Permet de retourner differentes indicateurs relartifs a un DTF
def _valeur_recherchee(indicateur, inputdtf) :
    if indicateur == "duree" :
        resultat = inputdtf["dureeVideo"].sum().total_seconds() / 60
    elif indicateur == 'vues' :
        resultat = inputdtf["vuesVideo"].sum()
    elif indicateur == "likes" :
        resultat = inputdtf["likesVideo"].sum()
    elif indicateur == "comz" :
        resultat = inputdtf['comzVideo'].sum()
    else :
        # Par defaut on retourne le nombre de lignes du DTF, i.e nbVideos
        resultat = inputdtf.shape[0]

    return resultat

# Permet de dumper nos tableaux dans le format attendu pour notre site https://s01.810.fr
def dump_synthese_courants(dtf_synth_courant, nomfichier) :
    liste_a_dumper = []
    for index, row in dtf_synth_courant.iterrows():
        liste_a_dumper.append({"\"Mois\"" : "\""+ str(row["Mois"]) + "\"", "\"Majorité\"" : row["Majorite"], "\"Droite\"" : row["Droite"], "\"Gauche\"" : row["Gauche"], "\"Verts\"" : row["Verts"], "\"Extrême Droite\"" : row["Extreme droite"], "\"Extrême Gauche\"" : row["Extreme gauche"]})

    liste_en_geustr = str(liste_a_dumper)
    liste_en_geustr = liste_en_geustr.replace("'","")
    with open(nomfichier, "w") as text_file:
        text_file.write(liste_en_geustr)

    return

# Affiche un suivi mensuel de l'activité des courants sur YouTube
# i.e : nombre de vidéos postées par mois par les différentes chaînes
#--------------------------------------------------------------------
def ligne_suivi_mensuelle(subdtf_videos, indicateur = "nb videos", annee = 2022) :

    liste_valeurs = []
    for i in range(12) :  
        videos_du_mois = vidz_filtree_par_mois(subdtf = subdtf_videos, mois_moins_un = i, annee=annee)
        valeur_recherchee = _valeur_recherchee(indicateur=indicateur, inputdtf=videos_du_mois)
        liste_valeurs.append(valeur_recherchee)
    # Creation d'un dictionnaire temporaire pour pouvoir transformer mes deux series en dataFrame
    
    return liste_valeurs

# Permet de créer un dataframe global, avec les indicateurs relatifs aux différents courants
# On peut ainsi dumper le dataframe dans un CSV, pour pouvoir l'utiliser dans "datawrapper.de",
#  qui nous permettra d'afficher des graphs web sur le site https://810.fr
def make_synthese_nbvideo_par_courant(dtsource, indicateur = "nb videos", annee = 2022) :
    videos_xd, videos_xg, videos_d, videos_g, videos_c, videos_v, videos_reste = un_dtf_par_courant(subdtf=dtsource)
    # CREATION AXE ABSCISSE
    x_date = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

    nomcourant_xd = "Extreme droite"
    lst_res_xd = ligne_suivi_mensuelle(subdtf_videos=videos_xd, indicateur = indicateur, annee = annee)
    nomcourant_xg = "Extreme gauche"
    lst_res_xg = ligne_suivi_mensuelle(subdtf_videos=videos_xg, indicateur = indicateur, annee = annee)
    nomcourant_d = "Droite"
    lst_res_d = ligne_suivi_mensuelle(subdtf_videos=videos_d, indicateur = indicateur, annee = annee)
    nomcourant_g = "Gauche"
    lst_res_g = ligne_suivi_mensuelle(subdtf_videos=videos_g, indicateur = indicateur, annee = annee)
    nomcourant_c = "Majorite"
    lst_res_c = ligne_suivi_mensuelle(subdtf_videos=videos_c, indicateur = indicateur, annee = annee)
    nomcourant_v = "Verts"
    lst_res_v = ligne_suivi_mensuelle(subdtf_videos=videos_v, indicateur = indicateur, annee = annee)


    tmp_d_globalresults = {'Mois' : x_date, nomcourant_xd : lst_res_xd, nomcourant_xg : lst_res_xg, nomcourant_d : lst_res_d, nomcourant_g : lst_res_g, nomcourant_c : lst_res_c, nomcourant_v : lst_res_v}
    dtf_globalresults = pd.DataFrame(tmp_d_globalresults)

    return dtf_globalresults

########################################################################
#   Définition de fonctions similaires mais pour faire les dump de 
#       fichiers relatifs aux candidats et candidates
########################################################################
def dump_synthese_candidats_v0(dtf_synth_candidat, nomfichier) :
    liste_a_dumper = []
    cnt = 0
    for index, row in dtf_synth_candidat.iterrows():
        liste_a_dumper.append({"\"indexMois\"" : "\""+ str(cnt) + "\"", "\"mois\"" : "\""+ str(row["Mois"]) + "\"", "\"zemmour\"" : row["Eric Zemmour"], "\"macron\"" : row["Emmanuel Macron"], "\"melenchon\"" : row["Jean-Luc Mélenchon"], "\"pecresse\"" : row["Valérie Pécresse"], "\"jadot\"" : row["Yannick Jadot"], "\"hidalgo\"" : row["Anne Hidalgo"], "\"lassalle\"" : row["Jean Lassalle"]})
        cnt += 1
    liste_en_geustr = str(liste_a_dumper)
    liste_en_geustr = liste_en_geustr.replace("'","")
    with open(nomfichier, "w") as text_file:
        text_file.write(liste_en_geustr)

    return

def make_synthese_nbvideo_par_candidat(dtsource, indicateur = "nb videos", liste_candidats =[], annee = 2022) :
    # CREATION AXE ABSCISSE
    x_date = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

    tmp_d_globalresults = {'Mois' : x_date}

    for candidat in liste_candidats :
        subdtf_candidat = dtsource[dtsource['candidat'] == candidat]
        performance_candidat = ligne_suivi_mensuelle(subdtf_videos=subdtf_candidat, indicateur = indicateur, annee=annee)
        tmp_d_globalresults[candidat] = performance_candidat

    dtf_globalresults = pd.DataFrame(tmp_d_globalresults)

    return dtf_globalresults

# Fonction qui retourne une liste de dtf, 1 par mois, elle prend 2 parametres
#    - Le dataframe global a casser en sous dataframe
#    - Une liste de dictionnaire de moi
# Elle retourne une liste de dictionnaire de dataframe avec les mois associes
def un_dtf_par_mois (dtfglobal, list_dict_dates) :
    liste_dtf_par_mois = []
    for mois in list_dict_dates :
        mois_courant = mois["mois"]
        date_debut = mois["dates"]["datemin"]
        date_fin = mois["dates"]["datemax"]
        dtf_videos_du_mois = dtfglobal[dtfglobal["dateVideo"] > date_debut]
        dtf_videos_du_mois = dtf_videos_du_mois[dtf_videos_du_mois["dateVideo"] < date_fin]
        liste_dtf_par_mois.append({"mois" : mois_courant, "dataframe" : dtf_videos_du_mois})
    return liste_dtf_par_mois

# Permet de récupérer toutes les vidéos d'un ou d'une candidate sur une période de temps donné
def get_candidat_subdtf(dtfglobal, candidat, datemin, datemax) :
    candidat_global_dtf = dtfglobal[dtfglobal["candidat"] ==  candidat]
    videos_can = candidat_global_dtf[candidat_global_dtf['dateVideo'] > datemin]
    videos_can = videos_can[videos_can['dateVideo'] < datemax]
    return videos_can