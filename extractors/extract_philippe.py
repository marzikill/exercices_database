import re

FILE = "/home/marzikill/Documents/Paul Lapie/Équipe/Philippe/EC/1G_Suites_E3C.tex"

def capture_group(research, i):
    if research:
        return research.group(1)
    else:
        return ""

def get_exos(fichier):
    # prend un fichier d'exercices EC de Philippe :
    # renvoit : la liste des (exercices:str, commentaires:str).
    # les commentaires associés à une exercice sont de la forme  :
    # "section sous section soussousection paragraph titre exercice"
    fichier = open(fichier, "r")
    content = fichier.readlines()

     
    exo_list = []   # liste des exercices
    exo = []        # liste des lignes d'un exercice
    adding = False  # si on est en train d'ajouter à l'exercice courant

    current_section, current_subsection, current_subsubsection, current_paragraph = "", "", "", ""
    for index_line in range(len(content)):
        line = content[index_line]
        if re.match(r"\\section", line):
            current_section = re.search(r"\\section\{([^\}]*)\}", line).group(1)
        if re.match(r"\\subsection", line):
            current_subsection = re.search(r"\\subsection\{([^\}]*)\}", line).group(1)
        if re.match(r"\\subsubsection", line):
            current_subsubsection = re.search(r"\\subsubsection\{([^\}]*)\}", line).group(1)
        if re.match(r"\\paragraph", line):
            current_paragraph = re.search(r"\\paragraph\*\{([^\}]*)\}", line).group(1)
        comment = f"{current_section }\n {current_subsection}\n  {current_subsubsection}\n   {current_paragraph}"

        # en premier : permet d'éviter d'ajouter le \begin{xca}
        if adding:
            exo.append(line)
        if re.search(r'\\begin{xca}', line):
            adding = True
            # on se débarrasse de l'environnement EX
            exo_title = capture_group(re.search(r"\[([^\]]*)\]", line), 1)
            comment = f"{comment}\nTitre : {exo_title}"
        # à la fin de l'exercice : on ajoute l'exercice à
        # la liste des exercices et on arrête d'ajouter
        # les lignes à l'exercice courant
        if re.search(r'\\end{xca}', line):
            # pb line 195 fichier philippe : nested xca environments
            # non supportés
            # la dernière ligne ajoutée de l'exercice est \end{xca}
            exo.pop()
            exo_list.append(("".join(exo), comment))
            exo = []
            adding = False
    return exo_list
