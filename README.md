# Introduction 
Ce repo contient une partie epuree du code utilise par [810](https://810.fr) pour realiser ses etudes du suivi de la campagne Presidentielle 2022 sur YouTube.

L'architecture du projet suit la forme suivante :
![image architecture projet](https://raw.githubusercontent.com/centre810/810s01_public_version/main/images/archi_projet.png)

1. Un module Python permet de recuperer la liste des chaines a etudier, dans AirTable
2. Une fois la liste chargee en memoire, un module Python questionne les API publiques de YouTube pour recuperer les statistiques des chaines et des videos. Ces donnees sont enregistree dans un fichier .json par chaine.
3. Un module Python permet de transformer tous ces fichiers .json en deux dataframe. Le premiers liste l'ensemble des chaines YouTube et leur statistiques. Le second dataframe liste l'ensemble des videos de toutes les chaines.
4. On cree ensuite des fichiers Jupyter Notebook pour etudier les differentes statistiques.
5. Les etudes detaillees des donnees realisees par [810](https://810.fr) sont publiees sur le site https://810.fr. Les donnees sont exportee dans des formats .json specifique pour mettre a jour les donnees sur le site evenement [s01.810.fr](https://s01.810.fr). Toutes les mises a jour sont publiees sur Twitter, sur le compte [@810huitdix](https://twitter.com/810huitdix)

Les elements 1 a 4 sont decrits en details ci-apres.





# Dossiers et fichiers
## Data_output
C'est le dossier ou seront les generes les fichiers utilises p
