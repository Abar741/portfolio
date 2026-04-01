from app.extensions import db


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    percentage = db.Column(db.Integer)
    icon = db.Column(db.String(100))