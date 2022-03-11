# Auteur : MBR pour 810
# Licence : CC BY-NC-SA 4.0
# Reference de la librairie utilisee : https://pypi.org/project/youtube-transcript-api/
#                       Installee depuis le terminal de visual code via : pip install youtube_transcript_api
######################################################################################################
# Description
######################################################################################################
# Sur la base d'un fichier CSV formatté par les scripts de requêtage YouTube, va récupérer les fichiers de transcripts des vidéos listées
# Tous les transcripts sont mis dans le dossier "output_ts"

from youtube_transcript_api import YouTubeTranscriptApi
import json
import pandas as pd
import re
from pathlib import Path

# Dossier source
dossier_source = "./temp_files/"
# Dossier cible
dossier_cible = "./data_sources/transcripts_videos/"
# Modifier le nom du fichier avec le fichier souhaité
nom_fichier = "liste_de_video_pour_transcript_analyse.csv"

######################################################################################################
# QUELQUES FONCTIONS DE TRAITEMENT
######################################################################################################

# dump YouTube Transcript dans un fichier
# Paramètres : nom du fichier output + contenu transcript à écrire
def dump_dans_fichier(nomfichier = '', nomsousdossier = "", transcript = {}):
    nomjson = dossier_cible + nomsousdossier+"/"+ nomfichier+".json"
    with open(nomjson, 'w') as mefile:
        json.dump(transcript, mefile, indent=4)
        print('file dumped')
    return

# Utiliser le nom du candidat pour faire un nom de dossier propre
def nettoyer_nom_candidat (nom = '') :
    clean_name = re.sub(r"[^a-zA-Z0-9]","",nom)
    return clean_name

# Parcourir le dataframe issue du CSV pour aller requêter les transcripts 
#                                   et les dumper un à un dans des fichiers .json
def get_videos_transcripts(dtf) :
    for index, row in dtf.iterrows():
        # Récupération des éléments nécessaire à créer l'architecture de fichier
        # Récupération de l'ID de la vidéo pour pouvoir utiliser la YT API
        try :
            video_id = row['vid_id']
        except KeyError :
            print("Impossible d'accéder au video id sur la ligne : ")
            print(row)
            continue

        # Récupération du nom du candidat pour créer un sous-dossier s'il n'existe pas déjà
        try :
            candidat = row['candidat']
            # On enleve tous les caractères spéciaux du nom, même les accents
            clean_candidat = nettoyer_nom_candidat(nom = candidat)
            # Si le dossier associé n'existe pas, on le crée
            Path(dossier_cible + "/" + clean_candidat).mkdir(parents=True, exist_ok=True)
        except KeyError :
            print("Impossible d'accéder au nom du candidat id sur la ligne : ")
            print(row)
            continue

        # On vérifie qu'on n'a pas déjà le transcript de la vidéo : 
        fichieracreer = Path(dossier_cible + clean_candidat+"/"+ video_id+".json")
        if Path.is_file(fichieracreer) :
            print("Le transcript de la vidéo " + video_id + "est déjà là. Dossier : " + clean_candidat)
            continue
        else : 
            # Récupération et dump du transcript associé
            try :
                yt_transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr'])
                dump_dans_fichier(nomfichier=video_id, nomsousdossier = clean_candidat, transcript=yt_transcript)
            except :
                print("Impossible d'accéder au fichier de sous-titre pour la vidéo " + video_id)
                continue
    return

######################################################################################################
# FIN DES FONCTIONS DE TRAITEMENT, DEBUT DU MAIN
######################################################################################################

fichier = dossier_source + nom_fichier
df_source = pd.read_csv(fichier)
get_videos_transcripts (df_source)

print("Fini !")