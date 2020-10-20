import requests
import pytest

access_token = requests.post("http://order-pizza-api.herokuapp.com/api/auth", json={
  "password": "test",
  "username": "test"
}).json()["access_token"]


data = {
  "Crust": "string",
  "Flavor": "string",
  "Order_ID": 0,
  "Size": "string",
  "Table_No": 0,
  "Timestamp": "string"
}


class TestPizzaApi:

    def test_get_success(self):
        response = requests.get("http://order-pizza-api.herokuapp.com/api/orders")
        assert response.status_code == 200
    
    
    def test_post_valid_order(self):
        response = requests.post("http://order-pizza-api.herokuapp.com/api/orders", json={
  "Crust": "string",
  "Flavor": "string",
  "Size": "string",
  "Table_No": 0
}, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 201
        assert set(response.json().keys()) == set(['Crust', 'Flavor', 'Order_ID', 'Size', 'Table_No', 'Timestamp'])

    
    def test_post_order_already_exists(self):
        response = requests.post("http://order-pizza-api.herokuapp.com/api/orders", json={
    "Crust": "NORMAL",
    "Flavor": "CHICKEN-FAJITA",
    "Size": "L",
    "Table_No": 3,
  }, headers={'Authorization': f'Bearer {access_token}'})
        assert response.status_code == 409
        assert set(response.json().keys()) == set(['detail', 'status', 'title', 'type'])
        assert response.json()["title"] == "Conflict"
        
    
    def test_delete_valid_order(self):
        response = requests.delete("http://order-pizza-api.herokuapp.com/api/orders/4")
        assert response.status_code == 200
        assert set(response.json().keys()) == set(['message'])
        assert response.json()["message"] == "Order deleted"

    
    def test_delete_order_does_not_exist(self):
        response = requests.delete("http://order-pizza-api.herokuapp.com/api/orders/5")
        assert response.status_code == 404
        assert set(response.json().keys()) == set(['detail', 'status', 'title', 'type'])
        assert response.json()["title"] == "Not Found"