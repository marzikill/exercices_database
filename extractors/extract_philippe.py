from pathlib import Path
from extractors import StreamDOM, StreamEnvironment

FILE = Path(__file__).parent.parent / "src/latex/Philippe/Premières/EC/1G_Suites_E3C.tex"

def get_exos(fichier):
    # prend un fichier d'exercices EC de Philippe :
    # renvoit : la liste des (exercices:str, commentaires:str).
    # les commentaires associés à une exercice sont de la forme  :
    # "titre exercice section sous section soussousection paragraph"
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
