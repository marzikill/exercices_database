import re

def capture_group(research, i):
    # Si la recherche renvoit une sélection
    if research:
        return research.group(1)
    # au lieu de renvoyer None
    else:
        return ""

class StreamDOM:
    def __init__(self):
        self.dom = ['section', 'subsection', 'subsubsection', 'paragraph\*']
        self.content = ['']*len(self.dom)

    def update(self, line):
        for level_i in range(len(self.dom)):
            if re.match(r'\\' + self.dom[level_i], line):
                # On met à jour contenu du niveau concerné
                self.content[level_i] = re.search(r'\\' + self.dom[level_i] + r"\{([^\}]*)\}", line).group(1)
                # On réinitialise les sous-niveaux lorsqu'un élément
                # de niveau supérieur est rencontré
                for level_j in range(level_i + 1, len(self.dom)):
                    self.content[level_j] = ''


    def get_dom(self):
        return {k:v for k, v in zip(self.dom, self.content)}

    def __repr__(self):
        representation = [ f"{k}:{v}" for k, v in zip(self.dom, self.content)]
        return "\n".join(representation)


class StreamEnvironment:
    def __init__(self, environement):
        self.env_start = r'\\begin{'+ environement + '}'
        self.env_end = r'\\end{'+ environement + '}'
        self.is_adding = False
        self.new_exo = False
        # On pourrait refactoriser ce morceau
        self.current_environment = []
        self.current_comments = []
        self.liste_environment = []
        self.liste_comments = []

    def update(self, line):
        # en premier : permet d'éviter d'ajouter le \begin{environment}
        if self.is_adding:
            self.current_environment.append(line)
        if re.search(self.env_start, line):
            # quand le début d'un nouvel exercice est détecté, on se
            # met à ajouter les lignes. On signale que l'on a détecté
            # le début d'un exercice, puis, on ajoute si présent le
            # commentaire associé à l'exercice.
            self.is_adding = True
            self.new_exo = True
            self.add_comment_current(capture_group(re.search(r"\[([^\]]*)\]", line), 1))
        if re.search(self.env_end, line):
            # nested environments not supported
            # la dernière ligne ajoutée de l'exercice est \end{environement}
            self.current_environment.pop()

            # on ajoute l'exercice courant et on réinitialise l'exercice courant.
            self.liste_environment.append("".join(self.current_environment))
            self.current_environment = []

            # on ajoute le commentaire courant et on réinitialise le commentaire courant.
            self.liste_comments.append(" ".join(self.current_comments))
            self.current_comments = []
            self.is_adding = False

    def get_content(self):
        return self.liste_environment, self.liste_comments

    def new_exo_detected(self):
        # Renvoit et consomme si un nouvel exercice a été détecté
        r = self.new_exo
        self.new_exo = False
        return r

    def add_comment_current(self, comment):
        # ajoute un commentaire au commentaire courant de l'exercice courant.
        self.current_comments.append('\\n' + comment)
