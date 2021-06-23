import re

SECONDES = "/home/marzikill/Documents/Paul Lapie/Équipe/Fanny/Secondes/exercices_2nde_fanny.tex"
PREMIERES = "/home/marzikill/Documents/Paul Lapie/Équipe/Fanny/Premières/exercices1ere_fanny.tex"

def decoupe(fichier):
    # prend un fichier d'exercices de Fanny :
    # renvoit :
    # le contenu du fichier, sous forme de liste
    # la liste des indexes de début de planche d'exercice
    # la liste des titres des planches d'exercices
    fichier = open(fichier, "r")
    content = fichier.readlines()
    planches_index = []
    planches_titres = []

    for index_line in range(len(content)):
        line = content[index_line]
        # Fanny définit le titre de ses planches dans une
        # variable dev, utilisée sur plusieurs planches successives
        # (mais pas systématiquement)
        if re.match(r'\\def\\dev', line):
            current_titre = re.search(r'Large([^\}]*)', line)
        # Toutes les planches ont pour titre .* Planche .*
        if re.search("Planche", line):
            titre = re.search(r'Planche[^:]*:([^\}]*)', line)
            planches_index.append(index_line)
            # Si le titre est une référence vers un titre
            # définit plus tôt, c'est celui-ci qu'on utilise
            if re.search("dev", titre.group(1)):
                # ... dans le fichier des premières
                planches_titres.append(current_titre.group(1))
            else:
                # S'il est hard-codé c'est lui qu'on prend
                planches_titres.append(titre.group(1))
        if re.search(r'\\end{document}', line):
            planches_index.append(index_line - 1)
    return content, planches_index, planches_titres

def get_exos(starting_index, ending_index, content):
    exo_list = []
    exo = []
    adding = False
    for i in range(starting_index, ending_index):
        # On détecte le début d'un exercice à l'aide
        # de l'environnement EX : on se met à ajouter
        # toutes les lines à l'exercice courant
        if re.search(r'\\begin{EX}', content[i]):
            adding = True
            # on se débarrasse de l'environnement EX
            content[i] = re.sub(r'\\begin{EX}', " ", content[i])
        # à la fin de l'exercice : on ajoute l'exercice à
        # la liste des exercices et on arrête d'ajouter
        # les lignes à l'exercice courant
        if re.search(r'\\end{EX}', content[i]):
            # on se débarrasse de l'environnement EX
            content[i] = re.sub(r'\\end{EX}', " ", content[i])
            exo.append(content[i])
            exo_list.append(exo)
            exo = []
            adding = False
        if adding and re.search(r'\S', content[i]):
            exo.append(content[i])
    return exo_list

def exo_liste_planche(i, content, planches_index):
    return get_exos(planches_index[i], planches_index[i + 1], content)

def exercice(i, exo_list):
    return "".join(exo_list[i])
