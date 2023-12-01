from Controller import db


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    age = db.Column(db.Integer)
    address = db.Column(db.String(255))
    gender = db.Column(db.String(10))
    marital_status = db.Column(db.String(20))
    wallet = db.Column(db.Float, default=0.0)