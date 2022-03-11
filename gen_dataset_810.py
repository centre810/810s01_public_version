# Classe de traitement des fichiers json pour en faire des Listes de chaines ou des listes de videos

import json
# importer les librairies pour travailler sur les dossiers et fichiers // source : https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
from os import listdir
from os.path import isfile, join
# importer datetime pour typer les donnees de dates des chaines et des videos
import datetime
import pandas as pd
import math
# necessaire pour les projection 
import random
# necessaire pour la conversion de la duree de la video Youtube
import isodate

# Transforme une colonne de listes en colonne d'une seule dimension avec toutes les valeurs
# Permet de faire des stats en volume d'occurences rapidement.
# Thanks : https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173
def listcol_to_1dcol(series) :
    return pd.Series(x for _list in series for x in _list)



# ----------------------------------------------------------
# Objet DataSets associe a ma fonction de requetage Youtube
# ----------------------------------------------------------
class mb_ds :

    def __init__(self) :
        self.dataset = None
        self.datachaines = None
        self.datavideos = None

    # ---------------------------------------------------
    # Load Files in memory
    # ---------------------------------------------------
    def get_files_dt(self, folder) :
        myfolder = folder
        #Recupere la liste des fichiers dans le dossier folder 
        onlyfiles = [f for f in listdir(myfolder) if isfile(join(myfolder, f))]
        # print(onlyfiles)

        data_set = []
        data = None
        for filen in onlyfiles :
            with open(myfolder+filen, 'r') as f:
                # print(f)
                data = json.load(f)
                data_set.append(data)

        del data

        print('Imported '+str(len(data_set))+' channel data')

        self.dataset = data_set

        return

    # --------------------------------------------------------------------------------------
    # Load full data in two dataFrames : One for stats by channel / One for stats by videos
    # --------------------------------------------------------------------------------------
    # Fonction speciale candidats
    def get_full_data_candidat(self, folder):
        self.get_files_dt(folder)

        # Puisque veut faire des data frame, il va falloir que je reagrege les donnees des videos sous la forme d'une seule ligne comme dans un tableau Excel
        dataset_chaines = []
        dataset_videos = []
        cnt = 0

        if self.dataset is not None :
            for datachaine in self.dataset :
                yt_associatedVideosData = None
                yt_channelName = ''
                cnt += 1
                # J'imagine que la fonction pop est mieux pour la portabilite du code, mais les elements que je recupere formellement sont ceux que j'ai defini moi meme dans les modules Python
                try :
                    dateRqt = datachaine['dateRequete']
                except KeyError :
                    dateRqt = '1970/01/01'
                try :
                    candidat = datachaine['candidat']
                except KeyError :
                    candidat = 'Undefined'
                try : 
                    parti = datachaine['parti']
                except KeyError :
                    parti = 'Undefined'
                try :
                    courant = datachaine['courant']
                except KeyError :
                    courant = 'Undefined'
                try :
                    channeldata = datachaine['YoutubeChannel'].popitem()
                except KeyError :
                    channeldata = 'corrupted data'

                if channeldata != 'corrupted data':
                    # L'element 0 de cette liste est l'id de la chaine
                    try :
                        yt_channelName = channeldata[1]['channel_info']['title']
                    except KeyError :
                        yt_channelName = 'Unknown'
                    try :
                        chaine_publishedAt = channeldata[1]['channel_info']['publishedAt']
                        chaine_publishedAt = chaine_publishedAt[0:chaine_publishedAt.find('T')]
                        yt_dateCreationChaine = datetime.date(int(chaine_publishedAt[0:4]), int(chaine_publishedAt[5:7]), int(chaine_publishedAt[8:10]))
                    except KeyError :
                        yt_dateCreationChaine = datetime.datetime(1970, 1, 1)
                    try :
                        yt_country = channeldata[1]['channel_info']['country']
                    except KeyError :
                        # En cas de doute, on set la chaine en FR
                        yt_country = 'FR'
                    try :
                        yt_globalChannelStats = channeldata[1]['channel_info']['statistics']
                    except KeyError :
                        yt_globalChannelStats = None
                    try :
                        yt_channel_categories = channeldata[1]['channel_info']['channelcategories']
                    except KeyError :
                        yt_channel_categories = None
                        # yt_channel_categories = []
                    try :
                        yt_associatedVideosData = channeldata[1]['video_data']
                    except KeyError :
                        yt_associatedVideosData is None

                    if yt_globalChannelStats is not None :
                            # Pour l'instant on ne prend pas la country
                            try :
                                yt_vuesChaines = int(yt_globalChannelStats['viewCount'])
                            except KeyError :
                                yt_vuesChaines = 0
                            try :
                                yt_abonnes = int(yt_globalChannelStats['subscriberCount'])
                            except KeyError :
                                yt_abonnes = 0
                            try :
                                yt_vidcount = int(yt_globalChannelStats['videoCount'])
                            except KeyError :
                                yt_vidcount = 0
                            # 21-3-13 : Ajout de country apres date creation chaine / Avant vue chaine
                            dataset_chaines.append([dateRqt, candidat, parti, courant, yt_channelName, yt_dateCreationChaine, yt_country, yt_channel_categories, yt_vuesChaines, yt_abonnes, yt_vidcount])

                    if yt_associatedVideosData is not None :
                        try :
                            sorted_vids = sorted(yt_associatedVideosData.items(), key = lambda item: int(item[1]['viewCount']), reverse = True)
                        except KeyError :
                            print('Probleme avec chaine : ' + yt_channelName)

                        # On recupere les informations de notre liste triee
                        for vid in sorted_vids:
                            try :
                                vid_title = vid[1]['title']
                            except KeyError :
                                vid_title = 'Unknown'
                            try :
                                vid_id = vid[1]['vidid']
                            except KeyError :
                                vid_id = 'Unknown'
                            try :
                                video_publishedAt = vid[1]['publishedAt']
                                # video_publishedAt = video_publishedAt[0:chaine_publishedAt.find('T')]
                                # vid_datepub = datetime.date(int(video_publishedAt[0:4]), int(video_publishedAt[5:7]), int(video_publishedAt[8:10]))
                                # 21-3-12 :
                                vid_datepub = datetime.datetime(int(video_publishedAt[0:4]), int(video_publishedAt[5:7]), int(video_publishedAt[8:10]), int(video_publishedAt[11:13]), int(video_publishedAt[14:16]), int(video_publishedAt[14:16]))

                            except KeyError :
                                vid_datepub = datetime.datetime(1970, 1, 1)
                            # 21-5-3
                            try :
                                video_tag_list = vid[1]['tags']
                            except KeyError :
                                video_tag_list = None
                            try :
                                video_livebroadcast = vid[1]['livebroadcast']
                            except :
                                video_livebroadcast = "none"
                            try : 
                                vid_views = int(vid[1]['viewCount'])
                            except KeyError :
                                vid_views = 0
                            try : 
                                vid_likes = int(vid[1]['likeCount'])
                            except KeyError :
                                vid_likes = 0
                            try :
                                vid_dislikes = int(vid[1]['dislikeCount'])
                            except KeyError :
                                vid_dislikes = 0
                            try :
                                vid_favcount = int(vid[1]['favoriteCount'])
                            except KeyError :
                                vid_favcount = 0
                            try : 
                                vid_comments = int(vid[1]['commentCount'])
                            except KeyError :
                                vid_comments = 0
                            try :
                                vid_duration = isodate.parse_duration(vid[1]['duration'])
                            except KeyError :
                                vid_duration = pd.Timedelta('0 days 00:00:00')
                            dataset_videos.append([dateRqt, candidat, parti, courant, yt_channelName, vid_title, vid_id, vid_datepub, video_tag_list, video_livebroadcast, vid_views, vid_likes, vid_dislikes, vid_favcount, vid_comments, vid_duration])

                else :
                    print('Corrupted data on '+str(cnt)+'th element. channel >> '+str(datachaine))
                    continue     
        else :
            print('Instancier le dataset dans le bon dossier avant de generer les deux dataFrames')

        df_chaine = pd.DataFrame(dataset_chaines, columns=['dateRqt', 'candidat', 'parti', 'courant', 'chaine', 'dateCreationChaine', 'pays', 'categorieschaine','vuesChaine','abonnesChaine','nbVideosChaine'])
        df_video = pd.DataFrame(dataset_videos, columns=['dateRqt', 'candidat', 'parti', 'courant', 'chaine','titreVideo', 'vid_id', 'dateVideo', 'liste_tags', 'livebroadcast', 'vuesVideo', 'likesVideo','dislikesVideo', 'favVideo', 'comzVideo', 'dureeVideo'])

        self.datavideos = df_video
        self.datachaines = df_chaine

        return df_video, df_chaine


    # --------------------------------------------------------------------------------------
    # Load full data in two dataFrames : One for stats by channel / One for stats by videos
    # --------------------------------------------------------------------------------------
    # Fonction speciale partis
    def get_full_data_parti(self, folder):
        self.get_files_dt(folder)

        # Puisque veut faire des data frame, il va falloir que je reagrege les donnees des videos sous la forme d'une seule ligne comme dans un tableau Excel
        dataset_chaines = []
        dataset_videos = []
        cnt = 0

        if self.dataset is not None :
            for datachaine in self.dataset :
                yt_associatedVideosData = None
                yt_channelName = ''
                cnt += 1
                # J'imagine que la fonction pop est mieux pour la portabilite du code, mais les elements que je recupere formellement sont ceux que j'ai defini moi meme dans les modules Python
                try :
                    dateRqt = datachaine['dateRequete']
                except KeyError :
                    dateRqt = '1970/01/01'
                try : 
                    parti = datachaine['parti']
                except KeyError :
                    parti = 'Undefined'
                try :
                    courant = datachaine['courant']
                except KeyError :
                    courant = 'Undefined'
                try :
                    channeldata = datachaine['YoutubeChannel'].popitem()
                except KeyError :
                    channeldata = 'corrupted data'

                if channeldata != 'corrupted data':
                    # L'element 0 de cette liste est l'id de la chaine
                    try :
                        yt_channelName = channeldata[1]['channel_info']['title']
                    except KeyError :
                        yt_channelName = 'Unknown'
                    try :
                        chaine_publishedAt = channeldata[1]['channel_info']['publishedAt']
                        chaine_publishedAt = chaine_publishedAt[0:chaine_publishedAt.find('T')]
                        yt_dateCreationChaine = datetime.date(int(chaine_publishedAt[0:4]), int(chaine_publishedAt[5:7]), int(chaine_publishedAt[8:10]))
                    except KeyError :
                        yt_dateCreationChaine = datetime.datetime(1970, 1, 1)
                    try :
                        yt_country = channeldata[1]['channel_info']['country']
                    except KeyError :
                        # En cas de doute, on set la chaine en FR
                        yt_country = 'FR'
                    try :
                        yt_globalChannelStats = channeldata[1]['channel_info']['statistics']
                    except KeyError :
                        yt_globalChannelStats = None
                    try :
                        yt_channel_categories = channeldata[1]['channel_info']['channelcategories']
                    except KeyError :
                        yt_channel_categories = None
                        # yt_channel_categories = []
                    try :
                        yt_associatedVideosData = channeldata[1]['video_data']
                    except KeyError :
                        yt_associatedVideosData is None

                    if yt_globalChannelStats is not None :
                            # Pour l'instant on ne prend pas la country
                            try :
                                yt_vuesChaines = int(yt_globalChannelStats['viewCount'])
                            except KeyError :
                                yt_vuesChaines = 0
                            try :
                                yt_abonnes = int(yt_globalChannelStats['subscriberCount'])
                            except KeyError :
                                yt_abonnes = 0
                            try :
                                yt_vidcount = int(yt_globalChannelStats['videoCount'])
                            except KeyError :
                                yt_vidcount = 0
                            # 21-3-13 : Ajout de country apres date creation chaine / Avant vue chaine
                            dataset_chaines.append([dateRqt, parti, courant, yt_channelName, yt_dateCreationChaine, yt_country, yt_channel_categories, yt_vuesChaines, yt_abonnes, yt_vidcount])

                    if yt_associatedVideosData is not None :
                        try :
                            sorted_vids = sorted(yt_associatedVideosData.items(), key = lambda item: int(item[1]['viewCount']), reverse = True)
                        except KeyError :
                            print('Probleme avec chaine : ' + yt_channelName)

                        # On recupere les informations de notre liste triee
                        for vid in sorted_vids:
                            try :
                                vid_title = vid[1]['title']
                            except KeyError :
                                vid_title = 'Unknown'
                            try :
                                video_publishedAt = vid[1]['publishedAt']
                                # video_publishedAt = video_publishedAt[0:chaine_publishedAt.find('T')]
                                # vid_datepub = datetime.date(int(video_publishedAt[0:4]), int(video_publishedAt[5:7]), int(video_publishedAt[8:10]))
                                # 21-3-12 :
                                vid_datepub = datetime.datetime(int(video_publishedAt[0:4]), int(video_publishedAt[5:7]), int(video_publishedAt[8:10]), int(video_publishedAt[11:13]), int(video_publishedAt[14:16]), int(video_publishedAt[14:16]))

                            except KeyError :
                                vid_datepub = datetime.datetime(1970, 1, 1)
                            # 21-5-3
                            try :
                                video_tag_list = vid[1]['tags']
                            except KeyError :
                                video_tag_list = None
                            try :
                                video_livebroadcast = vid[1]['livebroadcast']
                            except :
                                video_livebroadcast = "none"
                            try : 
                                vid_views = int(vid[1]['viewCount'])
                            except KeyError :
                                vid_views = 0
                            try : 
                                vid_likes = int(vid[1]['likeCount'])
                            except KeyError :
                                vid_likes = 0
                            try :
                                vid_dislikes = int(vid[1]['dislikeCount'])
                            except KeyError :
                                vid_dislikes = 0
                            try :
                                vid_favcount = int(vid[1]['favoriteCount'])
                            except KeyError :
                                vid_favcount = 0
                            try : 
                                vid_comments = int(vid[1]['commentCount'])
                            except KeyError :
                                vid_comments = 0
                            try :
                                vid_duration = isodate.parse_duration(vid[1]['duration'])
                            except KeyError :
                                vid_duration = pd.Timedelta('0 days 00:00:00')
                            dataset_videos.append([dateRqt, parti, courant, yt_channelName, vid_title, vid_datepub, video_tag_list, video_livebroadcast, vid_views, vid_likes, vid_dislikes, vid_favcount, vid_comments, vid_duration])

                else :
                    print('Corrupted data on '+str(cnt)+'th element. channel >> '+str(datachaine))
                    continue     
        else :
            print('Instancier le dataset dans le bon dossier avant de generer les deux dataFrames')

        df_chaine = pd.DataFrame(dataset_chaines, columns=['dateRqt', 'parti', 'courant', 'chaine', 'dateCreationChaine', 'pays', 'categorieschaine','vuesChaine','abonnesChaine','nbVideosChaine'])
        df_video = pd.DataFrame(dataset_videos, columns=['dateRqt', 'parti', 'courant', 'chaine','titreVideo','dateVideo', 'liste_tags', 'livebroadcast', 'vuesVideo', 'likesVideo','dislikesVideo', 'favVideo', 'comzVideo', 'dureeVideo'])

        self.datavideos = df_video
        self.datachaines = df_chaine

        return df_video, df_chaine

    # --------------------------------------------------------------------------------------
    # Retourne la moyenne de vues des videos d'une chaine (max=50) au dataFrame des chaine
    # --------------------------------------------------------------------------------------
    # get mean views of channel
    # Possibilite de borner sur une periode en date
    # Possibilite de ne prendre que le top
    def get_mean_views_channel (self, channel, datemin = datetime.datetime(1970,1,1,0,0,0), datemax = datetime.datetime(2100, 1, 1, 23, 59, 59), top=0) :
        df_chan = self.datavideos[self.datavideos['chaine'] == channel]
        if (datemin == datetime.datetime(1970,1,1, 0, 0, 0) and datemax == datetime.datetime(2100, 1, 1, 23, 59, 59)) :
            if top != 0 :
                df_chan = df_chan.sort_values(by = ['vuesVideo'], ascending = False).head(top)
            meanV = df_chan['vuesVideo'].mean()
        elif datemax == datetime.datetime(2100, 1, 1, 23, 59, 59) :
            df_chan_datemin = df_chan[df_chan['dateVideo'] > datemin]
            if top != 0 :
                df_chan = df_chan.sort_values(by = ['vuesVideo'], ascending = False).head(top)
            meanV = df_chan_datemin['vuesVideo'].mean()
        else : 
            df_chan_datemax = df_chan[df_chan['dateVideo'] < datemax]
            if top != 0 :
                df_chan = df_chan.sort_values(by = ['vuesVideo'], ascending = False).head(top)
            meanV = df_chan_datemax['vuesVideo'].mean()
        return meanV



################################################################################################################
# Verifier toutes les fonctions apres cette ligne, vu que certaines des cles initiales ont disparu
################################################################################################################



    # ----------------------------------------------------------------------------------------------------
    # Retourne la moyenne de vues des videos d'une chaine (max=50) ou d'un secteur sur le mois d'une date
    # ----------------------------------------------------------------------------------------------------
    # fonction qui retourne la mean value d'un secteur ou d'une chaine sur un mois
    def vid_month_meanview(self, secteur='', channel='', structure='', isnot=False, date=datetime.datetime.now, wo_struct = '', top=0) :
        meanV = 0
        df = self.datavideos
        if isnot is False :
            if secteur !='' :
                df = df[df['secteur'] == secteur]
                if wo_struct != '' :
                    df = df[df['structure'] != wo_struct]
            elif channel != '' :
                df = df[df['chaine'] == channel]
            elif structure != '' :
                df = df[df['structure'] == structure]
        else :
            if secteur !='' :
                df = df[df['secteur'] != secteur]
            elif channel != '' :
                df = df[df['chaine'] != channel]
            elif structure != '' :
                df = df[df['structure'] != structure]
        datemin = datetime.datetime(date.year, date.month, 1, 0, 0, 0)

        # Au dela de 12 mois, on augmente l'annee
        if date.month < 12 :
            datemax = datetime.datetime(date.year, date.month + 1, 1, 0, 0, 0)
        else :
            datemax = datetime.datetime(date.year + 1, date.month, 1, 0, 0, 0)

        df = df[df['dateVideo'] >= datemin]
        df = df[df['dateVideo'] < datemax]
        if top == 0 :
            meanV = df['vuesVideo'].mean()
        else :
            df = df.sort_values(by=['vuesVideo'], ascending=False).head(top)
            meanV = df['vuesVideo'].mean()
        return meanV
    
    # ----------------------------------------------------------------------------------------------------
    # Nombre de video sur une periode donnee en fonction des parametres
    # ----------------------------------------------------------------------------------------------------
    # Retourne le nombre de videos sur une periode donnee
    def nbvid_period (self, secteur='', chaine='', datemin=datetime.datetime(1970, 1, 1, 0, 0, 0), datemax=datetime.datetime(2100, 1, 1, 0, 0, 0)) :
        dv = self.datavideos
        if secteur != '' :
            dv = dv[dv['secteur'] == secteur]
        if chaine != '' :
            dv = dv[dv['chaine'] == chaine]
        if datemin != datetime.datetime(1970, 1, 1, 0, 0, 0) :
            dv = dv[dv['dateVideo'] > datemin]
        dv = dv[dv['dateVideo'] < datemax]
        return dv.shape[0]

    # ----------------------------------------------------------------------------------------------------
    # Nombre de videos postees par une chaine sur un mois
    # Modifié pour les élections 6/12/21
    # TO KEEP même si cheum
    # ----------------------------------------------------------------------------------------------------
    def videos_du_mois (self, subdtf, date=datetime.datetime.now) :
        datemin = datetime.datetime(date.year, date.month, 1, 0, 0, 0)

        # Au dela de 12 mois, on augmente l'annee
        if date.month < 12 : 
            datemax = datetime.datetime(date.year, date.month + 1, 1, 0, 0, 0)
        else :
            datemax = datetime.datetime(date.year + 1, date.month, 1, 0, 0, 0)

        df = subdtf[subdtf['dateVideo'] >= datemin]
        df = df[df['dateVideo'] < datemax]

        return df

    # ----------------------------------------------------------------------------------------------------
    # Nombre de vues cumulees par une chaine sur un mois
    # Modifié pour les élections 6/12/21
    # TO KEEP même si cheum
    # ----------------------------------------------------------------------------------------------------
    def nbvues_mois (self, subdtf, date=datetime.datetime.now) :
        datemin = datetime.datetime(date.year, date.month, 1, 0, 0, 0)

        # Au dela de 12 mois, on augmente l'annee
        if date.month < 12 : 
            datemax = datetime.datetime(date.year, date.month + 1, 1, 0, 0, 0)
        else :
            datemax = datetime.datetime(date.year + 1, date.month, 1, 0, 0, 0)

        df = subdtf[subdtf['dateVideo'] >= datemin]
        df = df[df['dateVideo'] < datemax]

        vues_cumulees = df["vuesVideo"].sum()

        return vues_cumulees


    # ----------------------------------------------------------------------------------------------------
    # Liste des videos postees par un secteur sur un mois
    # Modifié pour les élections 6/12/21
    # TO KEEP même si cheum
    # ----------------------------------------------------------------------------------------------------
    def vid_minutes_mois (self, subdtf, courant='', date=datetime.datetime.now) :
        dc = subdtf
        
        duree_par_chaine = []

        for chaine in dc['chaine'].unique() :
            # print (chaine)
            subchaine = dc[dc['chaine'] == chaine]



            # print(subchaine.shape[0])
            nbv = dc["dureeVideo"].sum().total_seconds() / 60
            # print(nbv)
            duree_par_chaine.append([chaine, nbv])

        df_nbvchaine = pd.DataFrame(duree_par_chaine, columns=['chaine', 'minutes'])
        return df_nbvchaine


    # ---------------------------------------------------------------------------------------------------
    # Retourne les tops vues pour une duree
    # ---------------------------------------------------------------------------------------------------
    # coef en parametre 
    def vid_duree_meanview(self, secteur='', channel='', structure='', dureemin=pd.Timedelta('0 days 00:00:00'), dureemax=pd.to_timedelta('3 days 00:00:00'), wo_struct = '', top=0, isnot=False) :
        meanV = 0
        df = self.datavideos
        if isnot is False :
            if secteur !='' :
                df = df[df['secteur'] == secteur]
                if wo_struct != '' :
                    df = df[df['structure'] != wo_struct]
            elif channel != '' :
                df = df[df['chaine'] == channel]
            elif structure != '' :
                df = df[df['structure'] == structure]
        else :
            if secteur !='' :
                df = df[df['secteur'] != secteur]
            elif channel != '' :
                df = df[df['chaine'] != channel]
            elif structure != '' :
                df = df[df['structure'] != structure]
        
        # Enelever des data les videos pour lesquelles on n'a pas eu de duration :
        df = df[df['dureeVideo'] != pd.to_timedelta('0 days 00:00:00')]
        # print('avant transfo : '+ str(df.shape[0]))
        df = df[df['dureeVideo'] >= dureemin]
        # print('apres datemin : '+ str(df.shape[0]))
        df = df[df['dureeVideo'] < dureemax]

        # print('apres datemax : '+ str(df.shape[0]))

        df = df.sort_values(by=['vuesVideo'], ascending=False)
        if top == 0 :
            meanV = df['vuesVideo'].mean()
        else :
            df = df.head(top)
            meanV = df['vuesVideo'].mean()
        return meanV

    # ---------------------------------------------------------------------------------------------------
    # Retourne les tops vues pour une duree
    # ---------------------------------------------------------------------------------------------------
    # coef en parametre 
    def df_vid_duree(self, secteur='', channel='', structure='', dureemin=pd.Timedelta('0 days 00:00:00'), dureemax=pd.to_timedelta('3 days 00:00:00'), wo_struct = '', isnot=False) :
        meanV = 0
        df = self.datavideos
        if isnot is False :
            if secteur !='' :
                df = df[df['secteur'] == secteur]
                if wo_struct != '' :
                    df = df[df['structure'] != wo_struct]
            elif channel != '' :
                df = df[df['chaine'] == channel]
            elif structure != '' :
                df = df[df['structure'] == structure]
        else :
            if secteur !='' :
                df = df[df['secteur'] != secteur]
            elif channel != '' :
                df = df[df['chaine'] != channel]
            elif structure != '' :
                df = df[df['structure'] != structure]
        
        # Enelever des data les videos pour lesquelles on n'a pas eu de duration :
        df = df[df['dureeVideo'] != pd.to_timedelta('0 days 00:00:00')]
        # print('avant transfo : '+ str(df.shape[0]))
        df = df[df['dureeVideo'] >= dureemin]
        # print('apres datemin : '+ str(df.shape[0]))
        df = df[df['dureeVideo'] < dureemax]

        # print('apres datemax : '+ str(df.shape[0]))

        df = df.sort_values(by=['vuesVideo'], ascending=False)
        
        return df

    # ----------------------------------------------------------------------------------------------------
    # Nombre de vues cumulees par une chaine sur un mois
    # Modifié pour les élections 6/12/21
    # TO KEEP même si cheum
    # ----------------------------------------------------------------------------------------------------
    def temps_cumule_mois (self, subdtf, date=datetime.datetime.now) :
        datemin = datetime.datetime(date.year, date.month, 1, 0, 0, 0)

        # Au dela de 12 mois, on augmente l'annee
        if date.month < 12 : 
            datemax = datetime.datetime(date.year, date.month + 1, 1, 0, 0, 0)
        else :
            datemax = datetime.datetime(date.year + 1, date.month, 1, 0, 0, 0)

        df = subdtf[subdtf['dateVideo'] >= datemin]
        df = df[df['dateVideo'] < datemax]

        temps_cumule = df["dureeVideo"].sum()
        total_minutes = temps_cumule.total_seconds() / 60

        return total_minutes

    
