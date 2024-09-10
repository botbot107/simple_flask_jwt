import requests
import json
import db

keycloak_url = 'http://192.168.91.128:8080/auth/admin/realms/yourrealm/clients'
access_token = 'your_admin_access_token'

import mysql.connector
import json

def get_access_token():
    token_url = 'http://192.168.91.128:8080/auth/realms/yourrealm/protocol/openid-connect/token'
    payload = {
        'grant_type': 'password',
        'client_id': 'flask-app',
        'username': 'admin',
        'password': 'admin'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Failed to obtain access token: {response.json()}")
        response.raise_for_status()


# Get the access token
try:
    access_token = get_access_token()
    print(f"Access Token: {access_token}")
except Exception as e:
    print(f"An error occurred: {e}")
access_token = 'qouUApHSHJiG9wYiJLeLozZiCmKIuEvE'
def export_clients_to_json():
    clients = db.get_clients_from_db()
    with open('clients.json', 'w') as f:
        json.dump(clients, f, indent=4)

def import_clients_to_keycloak():
    with open('clients.json', 'r') as f:
        clients = json.load(f)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    for client in clients:
        response = requests.post(keycloak_url, headers=headers, json=client)
        if response.status_code == 201:
            print(f"Client {client['user_name']} created successfully.")
        else:
            print(f"Failed to create client {client['user_name']}: {response.text}")

export_clients_to_json()
import_clients_to_keycloak()
