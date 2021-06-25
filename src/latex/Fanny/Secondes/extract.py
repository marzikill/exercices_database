import re

fichier = open("./exercices_2nde_fanny.tex", "r")
content = fichier.readlines()
planches_index = []
planches_titres = []

for index_line in range(len(content)):
    line = content[index_line]
    if re.search("Planche", line):
        titre = re.search(r'Planche[^:]*:([^\}]*)', line)
        planches_index.append(index_line)
        planches_titres.append(titre.group(1))

# for i in range(len(planches_index) - 1):
#     debut = planches_index[i]
#     fin = planches_index[i + 1] - 1
#     outplanche = open("./planches/"+ str(i) + " - " + planches_titres[i], "w")
#     for line in content[debut:fin]:
#         if re.search(r'\\newpage', line):
#             break
#         outplanche.write(line + "\n")
#     outplanche.close()

def get_exos(starting_index, ending_index, content):
    exo_list = []
    exo = []
    adding = False
    for i in range(starting_index, ending_index):
        if re.search(r'\\begin{EX}', content[i]):
            adding = True
        if adding:
            exo.append(content[i])
        if re.search(r'\\end{EX}', content[i]):
            exo_list.append(exo)
            exo = []
            adding = False
    return exo_list

fichier.close()

