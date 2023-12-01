from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jad:jad@localhost:5432/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your Goods model in models.py
class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(20))
    price_per_item = db.Column(db.Float)
    description = db.Column(db.String(200))
    count_in_stock = db.Column(db.Integer)

# Define your API routes


@app.route('/inventory/add_goods', methods=['POST'])
def add_goods():
    data = request.json

    new_goods = Goods(
        name=data['name'],
        category=data['category'],
        price_per_item=data['price_per_item'],
        description=data['description'],
        count_in_stock=data['count_in_stock']
    )

    db.session.add(new_goods)
    db.session.commit()

    return jsonify({"message": "Goods added successfully"}), 201


@app.route('/inventory/deduct_goods/<goods_id>', methods=['DELETE'])
def deduct_goods(goods_id):
    goods = Goods.query.get(goods_id)

    if goods:
        if goods.count_in_stock > 0:
            goods.count_in_stock -= 1
            db.session.commit()
            return jsonify({"message": "Goods deducted successfully"}), 200
        else:
            return jsonify({"error": "No items available in stock"}), 400
    else:
        return jsonify({"error": "Goods not found"}), 404


@app.route('/inventory/update_goods/<goods_id>', methods=['PATCH'])
def update_goods(goods_id):
    goods = Goods.query.get(goods_id)
    if goods:
        data = request.json

        # Update fields related to a specific item
        if 'name' in data:
            goods.name = data['name']
        if 'category' in data:
            goods.category = data['category']
        if 'price_per_item' in data:
            goods.price_per_item = data['price_per_item']
        if 'description' in data:
            goods.description = data['description']
        if 'count_in_stock' in data:
            goods.count_in_stock = data['count_in_stock']

        db.session.commit()

        return jsonify({"message": "Goods updated successfully"}), 200
    else:
        return jsonify({"error": "Goods not found"}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5003)
