from app import db

class Exercice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    niveau = db.Column(db.String(64))
    chapitre = db.Column(db.String(128))
    sujet = db.Column(db.String)
    contenu = db.Column(db.String)
    commentaire = db.Column(db.String)
    typologie = db.Column(db.String)
    difficulte = db.Column(db.Integer)
    annee = db.Column(db.Integer)
    auteur = db.Column(db.String(64))

    def __repr__(self):
        return f'<Exercice {self.id}>\n{self.contenu}'

