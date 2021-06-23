from app import app, db
from app.models import Exercice

print(Exercice.query.filter(Exercice.typologie.like("%EC%")).all())
