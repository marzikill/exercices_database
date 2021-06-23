import os
import regex
# from extract_items import *

def find_iter_tex_files(root_dir, niveau):
    matching_re = r'\/Niveau\/Chap\s*\d*\s*-\s*([\p{L}\s]*)\/(.*)\/([\w\s-]*\.tex)$'.replace("Niveau", niveau)
    for root, dirs, files in os.walk(root_dir + niveau):
        for f in files:
            full_path = root + '/' + f
            match = regex.findall(matching_re, full_path)
            if match:
                chapitre, classification, nom = match[0]
                if regex.match("Cours", classification):
                    yield chapitre, ["Cours"], full_path
                elif regex.match("Exercices", classification):
                    sujet = regex.sub("Exercices/\\d+[\w\s]*-\s*", '', classification)
                    yield chapitre, [ "Exercice", sujet ], full_path
                else:
                    pass
