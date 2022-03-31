import pandas as pd
import matplotlib.pyplot as plt


# Transforme une colonne de listes en colonne d'une seule dimension avec toutes les valeurs
# Permet de faire des stats en volume d'occurences rapidement.
# Thanks : https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
def listcol_to_1dcol(series) :
    return pd.Series(x for _list in series for x in _list)

# Dumper un fichier json dans le format attendu par https://s01.810.fr
def dump_tags_json(toptags, nomfichier) :
    
    liste_a_dumper = []

    for i, v in toptags.items():
        text_line = {"\"label\"" : "\"" + i + "\"", "\"value\"" : v}
        liste_a_dumper.append(text_line)
    
    liste_en_geustr = str(liste_a_dumper)
    liste_en_geustr = liste_en_geustr.replace("'","")
    with open(nomfichier, "w") as text_file:
        text_file.write(liste_en_geustr)

    return

# Liste les top tags à partir d'un DTF de vidéos passé en paramètre, "dtfv"
# Un paramètre "liste_exceptions" nous permet de filtrer les tags dont nous ne voudrions pas.
def liste_top_tags_de_chaines (dtfv, colonne = '', valeur = '', top = 50, titre = '', color = '', liste_exceptions = [], graph = 'oui') :
    if valeur == '' :
        videos_chaine = dtfv
    else : 
        videos_chaine = dtfv[dtfv[colonne] == valeur]
    toptags = listcol_to_1dcol(videos_chaine['liste_tags']).value_counts()
    # print("Taille toptags avant except : " + str(toptags.size))
    if liste_exceptions != [] :
        for exception in liste_exceptions :
            try:
                toptags = toptags.drop(exception)
                # print("Taille toptags après except : " + str(toptags.size))
            except :
                print("impossible de dropper "+ exception)
    toptags = toptags.sort_values(ascending = False).head(top)
    toptags = toptags.sort_values(ascending = True)
    if graph == 'oui' :
        if len(toptags > 0) :
            if color == '' :
                plt.barh(toptags.index,toptags.values)
            else :
                l_color = [color] * top
                plt.barh(toptags.index,toptags.values, color = l_color)
            if titre == '' :
                plt.title('Top ' + str(top) + ' tags de '+valeur)
            else :
                plt.title(titre)
            plt.ylabel('Tags')
            plt.xlabel("Nombre d'occurrences")
            plt.show()
        else :
            print("Aucun tags trouvés sur les vidéos sélectionnées")
    return toptags

# Fait un dataframe d'une serie
def turnserie_intodtf(nomcolonne, serie_data) :
    return pd.DataFrame(columns=[nomcolonne], data=serie_data) 

#---------------------------------------------------------------------------------------------
# Instaloader charge les hashtag sous forme de string. Cette fonction permet de creer
# un dataframe chaque hashtag a une ligne associe a son post et a son organisme
#---------------------------------------------------------------------------------------------
def create_hashtagliste_dataframe(subdtf) :
    output_list = []
    initial_dtf = subdtf
    for ind in initial_dtf.index :
        compte = initial_dtf['titreVideo'][ind]
        date_post = initial_dtf['dateVideo'][ind]
        str_hashtags = initial_dtf['liste_tags'][ind]
        nb_likes = initial_dtf['likesVideo'][ind]
        if str_hashtags != '[]' :
            # res = str_hashtags.strip("][ ").split(',')
            for i in range(len(str_hashtags)) :
                res_clean = str_hashtags[i].replace(" ", "")
                res_clean = res_clean.replace("'", "")
                res_clean = "#" + res_clean
                output_list.append([compte, date_post, res_clean, nb_likes])
        else :
            output_list.append([compte, date_post, "None"])
    output_dtf = pd.DataFrame(output_list, columns=['NomO', 'dateP', 'hashtag', 'nbLikes'])
    return output_dtf

# Fonction qui retourne une liste de dtf, 1 par mois, elle prend 2 parametres
#    - Le dataframe global a casser en sous dataframe
#    - Une liste de dictionnaire de moi
# Elle retourne une liste de dictionnaire de dataframe avec les mois associes
def nb_tags_par_mois (listedtfmois, toptagsglobal, lst_except=[]) :
    listemois = []
    for rang in listedtfmois :
        listemois.append(rang['mois'])
    dtftags_par_mois = pd.DataFrame(columns=listemois, index=toptagsglobal.index)
    # print(dtftags_par_mois.index)
    for tag in toptagsglobal.index :
        for dtf in listedtfmois :
            mois_courant = dtf["mois"]
            mois_dtf = dtf['dataframe']
            toptags = liste_top_tags_de_chaines(dtfv = mois_dtf, liste_exceptions = lst_except, graph='non')
            try :
                occurences_mois = toptags[tag]
            except KeyError :
                occurences_mois = 0
            
            dtftags_par_mois.loc[tag][mois_courant] = occurences_mois
    return dtftags_par_mois

# Fonction qui retourne une liste de dtf, 1 par mois, elle prend 2 parametres
#    - Le dataframe global a casser en sous dataframe
#    - Une liste de dictionnaire de moi
# Elle retourne une liste de dictionnaire de dataframe avec les mois associes
def part_tags_par_mois (listedtfmois, toptagsglobal, lst_except=[]) :
    listemois = []
    for rang in listedtfmois :
        listemois.append(rang['mois'])
    dtftags_par_mois = pd.DataFrame(columns=listemois, index=toptagsglobal.index)
    # print(dtftags_par_mois.index)
    for tag in toptagsglobal.index :
        for dtf in listedtfmois :
            mois_courant = dtf["mois"]
            mois_dtf = dtf['dataframe']
            toptags = liste_top_tags_de_chaines(dtfv = mois_dtf, liste_exceptions = lst_except, graph='non')
            maxtags_mois = toptags.max()
            try :
                occurences_mois = toptags[tag]
                taux_mois = (occurences_mois/maxtags_mois)*100
            except KeyError :
                occurences_mois = 0
                taux_mois = 0
            
            dtftags_par_mois.loc[tag][mois_courant] = taux_mois
    return dtftags_par_mois

# Ajoute une colonne a un dataframe sur la base du delta de deux des autres colonnes
def gen_delta(dtfsource, colfin, coldeb, nomcol) :
    list_res = []
    dtfres = dtfsource
    for i, row in dtfsource.iterrows():
        try :
            deltacol = row[colfin] - row[coldeb]
            list_res.append(deltacol)
        except :
            print("impossible d'acceder a "+colfin+" ou "+coldeb)
            return
    dtfres[nomcol] = list_res
    return dtfres

# Permet d'estimer la part de vidéos disposant d'un tag
def taux_de_tags_des_videos(dtfv, candidat = '', graph = 'oui') : 
    if candidat == '':
        videos_chaine = dtfv
    else :
        videos_chaine = dtfv[dtfv["candidat"] == candidat]
    nombre_total_videos_chaine = videos_chaine.shape[0]
    exploded_df = videos_chaine.explode('liste_tags')
    videos_sans_tags = exploded_df[exploded_df['liste_tags'].isnull()]
    nb_videos_sans_tags = videos_sans_tags.shape[0]
    videos_avec_tags = exploded_df[exploded_df['liste_tags'].notnull()]
    videos_avec_tags_dedupliquee = videos_avec_tags[~videos_avec_tags.index.duplicated(keep='first')]
    nb_videos_avec_tags = videos_avec_tags_dedupliquee.shape[0]

    # print(str(nb_videos_avec_tags) + " vidéos postées par " + candidat + " depuis 2020 disposaient de tags YouTube")
    # print(str(nb_videos_sans_tags) + " vidéos postées par " + candidat + " depuis 2020 NE disposaient PAS de tags YouTube")
    # pourcentage_videos_pompidou_sans_tags = nb_videos_sans_tags/nombre_total_videos_chaine
    # print(str(int(pourcentage_videos_pompidou_sans_tags*100))+"% vidéos postées depuis 2020 par le Centre Pompidou n'avait pas de tags")

    if nombre_total_videos_chaine > 0 :
        taux_videos_avectags = (nb_videos_avec_tags/nombre_total_videos_chaine)*100
        taux_videos_sanstags = (nb_videos_sans_tags/nombre_total_videos_chaine)*100
    else :
        taux_videos_avectags = 0
        taux_videos_sanstags = 0

    if graph == 'oui' :
        fig = plt.figure(figsize = (10,7))
        plt.pie([videos_sans_tags.shape[0], videos_avec_tags_dedupliquee.shape[0]], labels = ["sans tags", "avec tags"], autopct="%1.1f%%", colors=["#f2cb26", "#00a154"], explode = (0.005,0.005))
        plt.title("Videos de " + candidat, size = 14)
        plt.show()

    return taux_videos_avectags, taux_videos_sanstags

# Fonction qui retourne le taux de videos taggees par mois
#    - Le dataframe global a casser en sous dataframe
#    - Une liste de dictionnaire de moi
# Elle retourne une liste de dictionnaire de dataframe avec les mois associes
def taux_tags_par_mois (listedtfmois) :
    listemois = []
    for rang in listedtfmois :
        listemois.append(rang['mois'])
    dtftags_par_mois = pd.DataFrame(columns=listemois, index=['avec tags', 'sans tags'])
    # print(dtftags_par_mois.index)
    for dtf in listedtfmois :
        mois_courant = dtf["mois"]
        mois_dtf = dtf['dataframe']
        taux_avec_tags, taux_sans_tags = taux_de_tags_des_videos(dtfv=mois_dtf, graph='non')
        
        dtftags_par_mois.loc['avec tags'][mois_courant] = taux_avec_tags
        dtftags_par_mois.loc['sans tags'][mois_courant] = taux_sans_tags
    return dtftags_par_mois