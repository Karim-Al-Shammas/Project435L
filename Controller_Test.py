import json
import pytest
from app import app, db, Customer

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

def test_register_customer(client):
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }

    response = client.post('/register', json=data)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Customer registered successfully'

def test_register_duplicate_customer(client):
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }

    # Register the same customer twice
    client.post('/register', json=data)
    response = client.post('/register', json=data)

    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Username already taken'

def test_delete_customer(client):
    # Register a customer first
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }
    client.post('/register', json=data)

    # Delete the registered customer
    response = client.delete('/delete/john_doe')

    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Customer deleted successfully'

def test_delete_nonexistent_customer(client):
    response = client.delete('/delete/nonexistent_user')

    assert response.status_code == 404
    assert json.loads(response.data)['error'] == 'Customer not found'

def test_update_customer(client):
    # Register a customer first
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }
    client.post('/register', json=data)

    # Update the customer information
    updated_data = {
        'full_name': 'John Updated',
        'age': 31,
        'address': '456 New St',
        'gender': 'Male',
        'marital_status': 'Married'
    }
    response = client.put('/update/john_doe', json=updated_data)

    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Customer information updated successfully'

def test_get_all_customers(client):
    # Register a few customers
    clients_data = [
        {'full_name': 'Client 1', 'username': 'client1', 'age': 25, 'address': '123 Street', 'gender': 'Female', 'marital_status': 'Single'},
        {'full_name': 'Client 2', 'username': 'client2', 'age': 30, 'address': '456 Street', 'gender': 'Male', 'marital_status': 'Married'},
    ]

    for data in clients_data:
        client.post('/register', json=data)

    # Retrieve all customers
    response = client.get('/get_all_customers')

    assert response.status_code == 200
    assert len(json.loads(response.data)) == len(clients_data)

def test_get_customer(client):
    # Register a customer first
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }
    client.post('/register', json=data)

    # Retrieve the registered customer
    response = client.get('/get_customer/john_doe')

    assert response.status_code == 200
    assert json.loads(response.data)['username'] == 'john_doe'

def test_charge_wallet(client):
    # Register a customer first
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single'
    }
    client.post('/register', json=data)

    # Charge the customer's wallet
    charge_data = {'amount': 100.0}
    response = client.put('/charge_wallet/john_doe', json=charge_data)

    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Wallet charged with $100.0 successfully'

def test_deduct_wallet(client):
    # Register a customer first
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single',
        'wallet': 150.0
    }
    client.post('/register', json=data)

    # Deduct from the customer's wallet
    deduct_data = {'amount': 50.0}
    response = client.put('/deduct_wallet/john_doe', json=deduct_data)

    assert response.status_code == 200
    assert json.loads(response.data)['message'] == '$50.0 deducted from wallet successfully'

def test_deduct_insufficient_wallet(client):
    # Register a customer first
    data = {
        'full_name': 'John Doe',
        'username': 'john_doe',
        'age': 30,
        'address': '123 Main St',
        'gender': 'Male',
        'marital_status': 'Single',
        'wallet': 30.0
    }
    client.post('/register', json=data)

    # Attempt to deduct more than the wallet balance
    deduct_data = {'amount': 50.0}
    response = client.put('/deduct_wallet/john_doe', json=deduct_data)

    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Insufficient funds'
