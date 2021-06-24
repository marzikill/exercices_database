import re

FILE = "/home/marzikill/Documents/Paul Lapie/Équipe/Philippe/EC/1G_Suites_E3C.tex"

class StreamDOM:
    def __init__(self):
        self.dom = {'section':'', 'subsection':'', 'subsubsection':'', 'paragraph\*':''}

    def update(self, line):
        for level in self.dom:
            if re.match(r'\\' + level, line):
                try:
                    self.dom[level] = re.search(r'\\' + level + r"\{([^\}]*)\}", line).group(1)
                except AttributeError:
                    print(line)

    def get_dom(self):
        return self.dom

    def __repr__(self):
        representation = [ f"{k}:{v}" for k, v in self.dom.items()]
        return "\n".join(representation)


class StreamEnvironment:
    def __init__(self, environement):
        self.env_start = r'\\begin{'+ environement + '}'
        self.env_end = r'\\end{'+ environement + '}'
        self.current = ''
        self.is_adding = False
        self.new_exo = False
        self.current_environment = []
        self.current_comments = []
        self.liste_environment = []
        self.liste_comments = []

    def update(self, line):
        # en premier : permet d'éviter d'ajouter le \begin{environment}
        if self.is_adding:
            self.current_environment.append(line)
        if re.search(self.env_start, line):
            self.is_adding = True
            self.new_exo = True
            self.add_comment_current(capture_group(re.search(r"\[([^\]]*)\]", line), 1))
        if re.search(self.env_end, line):
            # nested environments not supported
            # la dernière ligne ajoutée de l'exercice est \end{environement}
            self.current_environment.pop()
            self.liste_environment.append("".join(self.current_environment))
            self.current_environment = []

            self.liste_comments.append(" ".join(self.current_comments))
            self.current_comments = []
            self.is_adding = False

    def get_content(self):
        return self.liste_environment, self.liste_comments

    def new_exo_detected(self):
        r = self.new_exo
        self.new_exo = False
        return r

    def add_comment_current(self, comment):
        self.current_comments.append(comment)


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

    exercices_stream = StreamEnvironment("xca")
    structure_dom = StreamDOM()

    for line in content:
        structure_dom.update(line)
        exercices_stream.update(line)
        if exercices_stream.new_exo_detected():
             exercices_stream.add_comment_current(structure_dom.__repr__())
    return exercices_stream.get_content()

     
#     exo_list = []   # liste des exercices
#     exo = []        # liste des lignes d'un exercice
#     adding = False  # si on est en train d'ajouter à l'exercice courant
# 
#     current_section, current_subsection, current_subsubsection, current_paragraph = "", "", "", ""
#     for index_line in range(len(content)):
#         line = content[index_line]
#         if re.match(r"\\section", line):
#             current_section = re.search(r"\\section\{([^\}]*)\}", line).group(1)
#         if re.match(r"\\subsection", line):
#             current_subsection = re.search(r"\\subsection\{([^\}]*)\}", line).group(1)
#         if re.match(r"\\subsubsection", line):
#             current_subsubsection = re.search(r"\\subsubsection\{([^\}]*)\}", line).group(1)
#         if re.match(r"\\paragraph", line):
#             current_paragraph = re.search(r"\\paragraph\*\{([^\}]*)\}", line).group(1)
#         comment = f"{current_section }\n {current_subsection}\n  {current_subsubsection}\n   {current_paragraph}"
# 
#         # en premier : permet d'éviter d'ajouter le \begin{xca}
#         if adding:
#             exo.append(line)
#         if re.search(r'\\begin{xca}', line):
#             adding = True
#             # on se débarrasse de l'environnement EX
#             exo_title = capture_group(re.search(r"\[([^\]]*)\]", line), 1)
#             comment = f"{comment}\nTitre : {exo_title}"
#         # à la fin de l'exercice : on ajoute l'exercice à
#         # la liste des exercices et on arrête d'ajouter
#         # les lignes à l'exercice courant
#         if re.search(r'\\end{xca}', line):
#             # pb line 195 fichier philippe : nested xca environments
#             # non supportés
#             # la dernière ligne ajoutée de l'exercice est \end{xca}
#             exo.pop()
#             exo_list.append(("".join(exo), comment))
#             exo = []
#             adding = False
