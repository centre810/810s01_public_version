# Definit le liste des couleurs du camembert sur la base de label de courants
def liste_couleurs_camembert (liste_label = []) :
    liste_couleurs_calendos = []

    for i in range(len(liste_label)) :
        if liste_label[i] == "Extrême gauche" :
            liste_couleurs_calendos.append("#cc0000")
        elif liste_label[i] == "droite" :
            liste_couleurs_calendos.append("#3c78d8")
        elif liste_label[i] == "Extrême droite" :
            liste_couleurs_calendos.append("#073763")
        elif liste_label[i] == "gauche" :
            liste_couleurs_calendos.append("#e6a3bf")
        elif liste_label[i] == "centre" :
            liste_couleurs_calendos.append("#9fc5e8")
        elif liste_label[i] == "vert" :
            liste_couleurs_calendos.append("#6aa84f")
        else :
            liste_couleurs_calendos.append("#111111")
    
    return liste_couleurs_calendos

# defini la liste de couleur des bar charts
# liste_valeurs_abscisse doit etre dans l'ordre d'apparition des candidats
def liste_couleurs_de_barres (dtf_source, nom_abscisse = "candidat", liste_valeurs_abscisse=[]) :
    liste_barres_couleurs = []
    for i in range(len(liste_valeurs_abscisse)) :
        if nom_abscisse != "courant" :
            courant = "divers"
            try :
                courant = dtf_source[dtf_source[nom_abscisse]==liste_valeurs_abscisse[i]].head(1).courant.iloc[0]
                # print(courant)
            except KeyError :
                print ("Impossible de trouver le courant")
                liste_barres_couleurs.append("#111111")
                continue
            if courant == "Extrême gauche" :
                liste_barres_couleurs.append("#cc0000")
            elif courant  == "droite" :
                liste_barres_couleurs.append("#3c78d8")
            elif courant  == "Extrême droite" :
                liste_barres_couleurs.append("#073763")
            elif courant  == "gauche" :
                liste_barres_couleurs.append("#e6a3bf")
            elif courant  == "centre" :
                liste_barres_couleurs.append("#9fc5e8")
            elif courant  == "vert" :
                liste_barres_couleurs.append("#6aa84f")
            else :
                liste_barres_couleurs.append("#111111")
    return liste_barres_couleurs

# defini la liste de couleur des bar charts
# liste_valeurs_abscisse doit etre dans l'ordre d'apparition des candidats
def liste_couleurs_de_barres_simple (liste_valeurs_abscisse=[]) :
    liste_barres_couleurs = []
    for i in range(len(liste_valeurs_abscisse)) :
            if liste_valeurs_abscisse[i] == "Extrême gauche" :
                liste_barres_couleurs.append("#cc0000")
            elif liste_valeurs_abscisse[i]  == "droite" :
                liste_barres_couleurs.append("#3c78d8")
            elif liste_valeurs_abscisse[i]  == "Extrême droite" :
                liste_barres_couleurs.append("#073763")
            elif liste_valeurs_abscisse[i]  == "gauche" :
                liste_barres_couleurs.append("#e6a3bf")
            elif liste_valeurs_abscisse[i]  == "centre" :
                liste_barres_couleurs.append("#9fc5e8")
            elif liste_valeurs_abscisse[i]  == "vert" :
                liste_barres_couleurs.append("#6aa84f")
            else :
                liste_barres_couleurs.append("#111111")
    return liste_barres_couleurs


# defini la liste de couleur des bar charts de media
# liste_valeurs_abscisse doit etre dans l'ordre d'apparition des candidats
def liste_couleurs_media (liste_valeurs_abscisse=[]) :
    liste_barres_couleurs = []
    for i in range(len(liste_valeurs_abscisse)) :
            if liste_valeurs_abscisse[i] == "Radio" :
                liste_barres_couleurs.append("#73338f")
            elif liste_valeurs_abscisse[i]  == "Chaînes TV généralistes" :
                liste_barres_couleurs.append("#0182e7")
            elif liste_valeurs_abscisse[i]  == "Chaînes TV infos" :
                liste_barres_couleurs.append("#222222")
            elif liste_valeurs_abscisse[i]  == "YouTube" :
                liste_barres_couleurs.append("#ff0000")
            else :
                liste_barres_couleurs.append("#111111")
    return liste_barres_couleurs