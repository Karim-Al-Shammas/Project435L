from Controller import db

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(20))
    price_per_item = db.Column(db.Float)
    description = db.Column(db.String(200))
    count_in_stock = db.Column(db.Integer)
