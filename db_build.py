from app import app, db
from app.models import Exercice
import extractors.extract_philippe as ph
import extractors.extract_fanny as fa
from extractors.extract_florian import *
from extractors.walk_files_florian import *

################################
# Extraction exercices Florian #
################################

auteur = "Florian Picard"
root_dirs = {2019: "/home/marzikill/Documents/Paul Lapie/Archives 2019-2020/", 2020:  "/home/marzikill/Documents/Paul Lapie/"}
# root_dir = "/home/marzikill/Documents/Paul Lapie/Archives 2019-2020/"
niveaux = {2:"Secondes", 1:"Premières", 0:"Terminales"}
for annee, root_dir in root_dirs.items():
    # selectionne_niveau = niveaux[1]
    for niveau in niveaux.values():
        all_tex_files= find_iter_tex_files(root_dir, niveau)
        for (chapitre, type_materiel, chemin) in all_tex_files:
            if type_materiel[0] == "Exercice":
                exo_liste = Fichier(chemin) 
                try:
                    data = exo_liste.tex_extract_content_to_str()
                    # print("Fichier {} traité avec succès".format(type_materiel[1]))
                except AssertionError:
                    # due à un problème de parsing
                    print("Échec du traitement de {} : problème de parsing".format(type_materiel[1]))
                    print(chemin)
                except AttributeError:
                    # due à un fichier non correctement formaté 
                    print("Échec du traitement de {} : pas un fichier d'exercices".format(type_materiel[1]))
                except EOFError:
                    print("Fuck you")
                    print(chemin)
                for exercice_str in data:
                    e = Exercice(niveau=niveau[:-1],\
                                 chapitre=chapitre,\
                                 sujet=type_materiel[1],\
                                 contenu=exercice_str,\
                                 typologie="exercice",\
                                 annee=annee,\
                                 auteur=auteur)
                    db.session.add(e)
print("Fin de l'ajout des fichiers de Florian")

##############################
# Extraction exercices Fanny #
##############################

auteur = "Fanny Buffet Delmas"
root_dirs = {2020: "/home/marzikill/Documents/Paul Lapie/Équipe/Fanny"}
niveaux = {2:"Seconde", 1:"Première"}
for annee, root_dir in root_dirs.items():
    for niveau in niveaux.values():
       if niveau == "Seconde":
           fichier = fa.SECONDES
       else:
           fichier = fa.PREMIERES
       content, planches_index, planches_titres = fa.decoupe(fichier)
       for numero_planche in range(len(planches_titres)):
           titre = planches_titres[numero_planche]
           exo_liste = fa.exo_liste_planche(numero_planche, content, planches_index)
           for numero_exercice in range(len(exo_liste)):
               e = Exercice(niveau=niveau,\
                            sujet=titre,\
                            contenu=fa.exercice(numero_exercice, exo_liste),\
                            typologie="exercice",\
                            annee=annee,\
                            auteur=auteur)
               db.session.add(e)
print("Fin de l'ajout des fichiers de Fanny")

#################################
# Extraction exercices Philippe #
#################################

auteur = "Philippe Camus"
data = ph.get_exos(ph.FILE)
for (contenu, commentaire) in data:
    # e = Exercice(db, {"niveau":"Première",
    #                   "chapitre":"Suites",
    #                   "contenu":contenu,
    #                   "commentaire":commentaire,
    #                   "type":"EC",
    #                   "annee":2020,
    #                   "auteur":"Philippe Camus"})
    e  = Exercice(contenu=contenu,\
                  commentaire=commentaire,\
                  auteur=auteur,\
                  niveau="Première",\
                  typologie="EC",\
                  annee=2020)
    db.session.add(e)
print("Fin de l'ajout des fichiers de Philippe")

##########
# Commit #
##########
db.session.commit()
print("Exercices ajoutés à la base de donnée")
