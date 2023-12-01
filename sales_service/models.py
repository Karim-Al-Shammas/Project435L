from Controller import db


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(20))
    price_per_item = db.Column(db.Float)
    description = db.Column(db.String(200))
    count_in_stock = db.Column(db.Integer)

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

class SaleHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_username = db.Column(db.String(50))
    good_name = db.Column(db.String(100))
    sale_price = db.Column(db.Float)