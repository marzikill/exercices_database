from app import app, db
from app.models import Exercice
from flask import render_template, jsonify, request, get_template_attribute

@app.route('/')
@app.route('/index')
def index():

    # exosEC = Exercice.query.filter(Exercice.typologie.like("%EC%")).all()
    # contenu = []
    # for e in exosEC:
        # contenu.append(f"---Exercice {e.id}---<br>Contenu<br>{e.contenu}")
    # contenu = "<br>".join(contenu)
    return "Bonjour tout le monde. <a href='http://www.pisurquatre.xyz/recherche'> Rechercher un exercice </a>"

@app.route('/recherche/')
def recherche():
    liste_auteurs = Exercice.query.with_entities(Exercice.auteur).distinct().all()
    liste_auteurs = [e.auteur for e in liste_auteurs] 
    liste_typologies = Exercice.query.with_entities(Exercice.typologie).distinct().all()
    liste_typologies = [e.typologie for e in liste_typologies] 
    liste_niveaux = Exercice.query.with_entities(Exercice.niveau).distinct().all()
    liste_niveaux = [e.niveau for e in liste_niveaux] 
    return render_template("recherche.html",\
                           auteurs=liste_auteurs,\
                           niveaux=liste_niveaux,\
                           typologies=liste_typologies)

@app.route('/recherche/api', methods=['POST'])
def recherche_api():
    dict_to_htmltable = get_template_attribute('table.html', 'table')
    # On filtre les champs prédéterminés
    exercices = Exercice.query.filter_by(auteur=request.form['auteur'],\
                                         niveau=request.form['niveau'],
                                         typologie=request.form['typologie'])
    # On filtre selon le contenu
    if request.form['contenu']:
        exercices = exercices.filter(Exercice.contenu.like(f"%{request.form['contenu']}%"))
    # On filtre selon le commentaire
    # On test si une requête sur le commentaire. Si il n'est pas renseigné dans la base de données
    # alors on perd toutes les recherches
    if request.form['commentaire']:
        exercices = exercices.filter(Exercice.commentaire.like(f"%{request.form['commentaire']}%"))
    return dict_to_htmltable(exercices.all())

    # Débogage divers et varié
    # return str(len(exercices.all()))
    # return "".join(e for e in exercices.all())
    # return jsonify( {k:v for k, v in request.form.items()} )
