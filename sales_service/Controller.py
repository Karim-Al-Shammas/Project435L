from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jad:jad@localhost:5432/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

# Define your SaleHistory model for historical purchases
class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(20))
    price_per_item = db.Column(db.Float)
    description = db.Column(db.String(200))
    count_in_stock = db.Column(db.Integer)

class Customer(db.Model):

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


# Define your API routes
@app.route('/sales/display_goods', methods=['GET'])
def display_goods():
    goods_list = Goods.query.with_entities(Goods.name, Goods.price_per_item).all()
    goods_json = [{"name": name, "price": price} for name, price in goods_list]
    return jsonify({"goods": goods_json})

@app.route('/sales/get_goods_details/<good_name>', methods=['GET'])
def get_goods_details(good_name):
    good = Goods.query.filter_by(name=good_name).first()

    if good:
        return jsonify({
            "name": good.name,
            "category": good.category,
            "price_per_item": good.price_per_item,
            "description": good.description,
            "count_in_stock": good.count_in_stock
        })
    else:
        return jsonify({"error": "Good not found"}), 404

@app.route('/sales/sale', methods=['POST'])
def make_sale():
    data = request.json

    customer_username = data.get('customer_username')
    good_name = data.get('good_name')

    # Check if the customer and good exist
    customer = Customer.query.filter_by(username=customer_username).first()
    good = Goods.query.filter_by(name=good_name).first()

    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if not good:
        return jsonify({"error": "Good not found"}), 404

    # Check if the customer has enough money and the good is available
    if customer.wallet_balance >= good.price_per_item and good.count_in_stock > 0:
        # Deduct money from customer wallet
        customer.wallet_balance -= good.price_per_item

        # Decrease the count of the purchased good from the database
        good.count_in_stock -= 1

        # Save the sale history
        sale_history = SaleHistory(
            customer_username=customer_username,
            good_name=good_name,
            sale_price=good.price_per_item
        )

        db.session.add(sale_history)
        db.session.commit()

        return jsonify({"message": "Sale successful"}), 201
    else:
        return jsonify({"error": "Insufficient funds or item out of stock"}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5004)
