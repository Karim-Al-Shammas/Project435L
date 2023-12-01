from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# SQLite Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jad:jad@localhost:5432/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Customer Model
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

@app.route('/register', methods=['POST'])
def register_customer():
    data = request.json
    username = data.get('username')

    existing_customer = Customer.query.filter_by(username=username).first()

    if existing_customer:
        return jsonify({'error': 'Username already taken'}), 400

    new_customer = Customer(
        full_name=data['full_name'],
        username=data['username'],
        age=data['age'],
        address=data['address'],
        gender=data['gender'],
        marital_status=data['marital_status']
    )

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'message': 'Customer registered successfully'})

@app.route('/delete/<username>', methods=['DELETE'])
def delete_customer(username):
    customer = Customer.query.filter_by(username=username).first()

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})
    else:
        return jsonify({'error': 'Customer not found'}), 404

@app.route('/update/<username>', methods=['PUT'])
def update_customer(username):
    customer = Customer.query.filter_by(username=username).first()

    if customer:
        data = request.json
        for key, value in data.items():
            setattr(customer, key, value)
        db.session.commit()
        return jsonify({'message': 'Customer information updated successfully'})
    else:
        return jsonify({'error': 'Customer not found'}), 404

@app.route('/get_all_customers', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    result = [{'id': customer.id, 'full_name': customer.full_name, 'username': customer.username,
               'age': customer.age, 'address': customer.address, 'gender': customer.gender,
               'marital_status': customer.marital_status, 'wallet': customer.wallet} for customer in customers]
    return jsonify(result)

@app.route('/get_customer/<username>', methods=['GET'])
def get_customer(username):
    customer = Customer.query.filter_by(username=username).first()

    if customer:
        result = {'id': customer.id, 'full_name': customer.full_name, 'username': customer.username,
                  'age': customer.age, 'address': customer.address, 'gender': customer.gender,
                  'marital_status': customer.marital_status, 'wallet': customer.wallet}
        return jsonify(result)
    else:
        return jsonify({'error': 'Customer not found'}), 404

@app.route('/charge_wallet/<username>', methods=['PUT'])
def charge_wallet(username):
    customer = Customer.query.filter_by(username=username).first()

    if customer:
        data = request.json
        amount = data.get('amount', 0)
        customer.wallet += amount
        db.session.commit()
        return jsonify({'message': f'Wallet charged with ${amount} successfully'})
    else:
        return jsonify({'error': 'Customer not found'}), 404

@app.route('/deduct_wallet/<username>', methods=['PUT'])
def deduct_wallet(username):
    customer = Customer.query.filter_by(username=username).first()

    if customer:
        data = request.json
        amount = data.get('amount', 0)
        if customer.wallet < amount:
            return jsonify({'error': 'Insufficient funds'}), 400
        else:
            customer.wallet -= amount
            db.session.commit()
            return jsonify({'message': f'${amount} deducted from wallet successfully'})
    else:
        return jsonify({'error': 'Customer not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)