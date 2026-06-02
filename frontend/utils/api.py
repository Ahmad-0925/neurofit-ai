import requests

BASE_URL = "http://127.0.0.1:8000"

def signup(name: str, email: str, password: str):
    response = requests.post(f"{BASE_URL}/auth/signup", json={
        "name": name,
        "email": email,
        "password": password
    })
    return response

def login(email: str, password: str):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    return response

def get_profile(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile/", headers=headers)
    return response

def create_profile(token: str, data: dict):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/profile/", json=data, headers=headers)
    return response



def update_profile(token: str, data: dict):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{BASE_URL}/profile/", json=data, heagit statusders=headers)
    return response


def delete_profile(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/profile/", headers=headers)
    return response